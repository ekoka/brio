# coding=utf-8

import datetime
import bcrypt
import uuid

#from wtforms import (Form, validators, Field, HiddenField, TextField,
#                     PasswordField, BooleanField, SelectField, TextAreaField,
#                     SelectMultipleField, StringField, validators as vld)
from sqlalchemy import (Table, Column, Integer, String, Unicode, DateTime, 
                        Date, Numeric, Boolean, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import mapper, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from brio.startup import db
from .junctures import Juncture

class User(Juncture):

    __tablename__='users'
    __mapper_args__ = dict(polymorphic_identity=__tablename__)
    #__mapper_args__ = dict(polymorphic_identity=u'users')

    user_id = Column(Integer, ForeignKey('junctures.juncture_id'), 
                     primary_key=True)
    first_name = Column(Unicode)
    last_name = Column(Unicode)
    email = Column(Unicode, unique=True)
    status = Column(Unicode)
    _password = Column('password', Unicode)
    token = Column(Unicode)
    failed_attempts = Column(Integer)
    #auth_key = Column(Unicode, nullable=True)
    #auth_key_expire = Column(DateTime, nullable=True)
    lang = Column(Unicode, default=u'en')
    passkey = Column(Unicode)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = encrypt_password(password)

    def new_token(self, token=None):
        self.token = token or uuid.uuid4().hex.decode('utf8')

    def authenticate(self, password):
        # password must be an unicode object
        password = password.encode('utf-8')
        return self.password==bcrypt.hashpw(
            password, self.password.encode('utf-8')).decode('utf-8')

    def authorize(self, roles, params=None):
        # if no roles were specified, green light
        if len(roles)==0:
            return True

        self_roles = set(r.name for r in self.roles)
        # if the only role specified is an AuthorizationExclusion and user
        # isn't listed, green light
        if len(roles) == 1:
            try:
                if not roles[0].excludes(self_roles):
                    return True
                return False
            except AttributeError:
                pass

        # if user's roles intersect with authorized roles, green light
        if bool(self_roles.intersection(roles)):
            return True

        # if OwnershipAuthorization is required and user is owner, green light
        for r in roles:
            try:
                return r.owned_by(self.user_id, params)
            except AttributeError:
                pass

        ## if  applies for LimitedAccessAuthorization, green light
        #for r in roles:
        #    try:
        #        return r.is_allowed(self_roles)
        #    except AttributeError:
        #        pass

        # is resource explicitly green lit (useful in combination with 
        # `expects_user` when authorization is controlled from within 
        # the resource).
        return '*' in roles

class UserAuthKey(db.Base):
    __tablename__='user_auth_keys'

    tenant_id = Column(None, ForeignKey('tenants.tenant_id'))
    key = Column(Unicode, primary_key=True)
    user_id = Column(None, ForeignKey('users.user_id'))
    expire_func = lambda: datetime.datetime.utcnow() + datetime.timedelta(days=60)
    expire = Column(DateTime, nullable=True, default=expire_func)

    # relationships
    user = relationship('User', backref='authkeys')


def encrypt_password(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    pwhash = bcrypt.hashpw(password, salt)
    # return in unicode
    return pwhash.decode('utf-8')

editable_fields = [
    'first_name', 'last_name', 'telephone1', 'telephone2', 'fax', 
    'address1', 'address2', 'city', 'province', 'country', 'postal_code', 
    'company',]


class OwnershipAuthorization(object):

    def __init__(self, owner_identifier='id'):
        #TODO: Raise an exception here if owner_identifier is None or empty
        self.owner_identifier = owner_identifier

    def owned_by(self, owner_id, params):
        if owner_id is not None:
            # sometimes the value arrives as a string when you expect an int
            # and vice versa.
            converter = type(owner_id)
            try:
                return owner_id == converter(params.get(self.owner_identifier))
            except AttributeError:
                raise Exception(
                    'Method OwnershipAuthorization.owned_by() '
                    'expects third argument (params) to be a dict.')
        return False

def authorize_owner(owner_identifier):
    return OwnershipAuthorization(owner_identifier)

class LimitedAccessAuthorization(object):
    def __init__(self, roles):
        self.roles = roles

    def is_allowed(roles):
        return bool(roles.intersection(self.roles) or '*' in self.roles)

def limited_access(roles):
    if not isinstance(roles, list):
        roles = [roles]
    return LimitedAccessAuthorization(roles)

class AuthorizationExclusion(object):
    def __init__(self, *roles):
        self.roles = roles

    def excludes(self, *roles):
        # roles in params intersect with excluded roles
        return bool(set(self.roles).intersection(roles)) 

def exclude_roles(*roles):
    return AuthorizationExclusion(*roles)


u_r = users_roles_table = Table(
    'users_roles', db.Base.metadata,
    Column('tenant_id', None, ForeignKey('tenants.tenant_id', 
            ondelete='cascade'), primary_key=True),
    Column('user_id', None, ForeignKey('users.user_id', ondelete='cascade'), 
            primary_key=True),
    Column('role_id', None, ForeignKey('roles.role_id', ondelete='cascade'), 
            primary_key=True),
)

class Role(db.Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True)
    label = Column(Unicode)
    private = Column(Boolean, default=False)

    users = relationship('User', secondary='users_roles', backref='roles')
