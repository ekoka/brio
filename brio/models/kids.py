from sqlalchemy import (Table, Column, Integer, String, Unicode, DateTime, 
                        Date, Numeric, Boolean, ForeignKey)
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import mapper, relationship, backref

from .junctures import Juncture, db

class Kid(Juncture):
    __tablename__ = 'kids'

    kid_id=Column(Integer, ForeignKey('junctures.juncture_id'),
                  primary_key=True)
    firstname=Column(Unicode)
    lastname=Column(Unicode)
    dob=Column(Date)
    phone=Column(Unicode)
    email=Column(Unicode)
    address=Column(Unicode)
    city=Column(Unicode)
    postal_code=Column(Unicode)
    parent_firstname=Column(Unicode)
    parent_lastname=Column(Unicode)
    healthcare_number=Column(Unicode)
    healthcare_expiration=Column(Unicode)
    conditions_allergies=Column(Unicode)
    additional_info=Column(Unicode)
    status=Column(Unicode)

    __mapper_args__ = {'polymorphic_identity':'kids'}

class Registration(db.Base):
    __tablename__ = 'registrations'

    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), nullable=False)
    registration_id=Column(Integer, primary_key=True)
    kid_id=Column(None, ForeignKey('kids.kid_id'))
    activity_id=Column(None, ForeignKey('activities.activity_id'))
    date=Column(Date)
    post_activity_action=Column(Unicode)
    balance=Column(Numeric(precision=10, scale=2, asdecimal=True))
    optin_photo=Column(Boolean)
    optin_newsletter=Column(Boolean)

    UniqueConstraint('kid_id', 'activity_id')

    # relationships
    # we use the Association Object pattern here.
    # http://docs.sqlalchemy.org/en/rel_0_7/orm/relationships.html#association-object
    payments=relationship('Payment', backref='registration')
    activity=relationship('Activity', backref='registrations')
    kid=relationship('Kid', backref='registrations')

class Payment(db.Base):
    __tablename__ = 'payments'

    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), nullable=False)
    payment_id=Column(Integer, primary_key=True)
    registration_id=Column(None, ForeignKey('registrations.registration_id'))
    type=Column(Unicode)
    paid=Column(Numeric(precision=10, scale=2, asdecimal=True))
    initial_balance=Column(Numeric(precision=10, scale=2, asdecimal=True))
    new_balance=Column(Numeric(precision=10, scale=2, asdecimal=True))
    date=Column(Date)
