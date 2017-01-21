from brio.startup import db, app
from brio.models import User, Role
from brio.framework import request

def get_users(__tenant__):
    records = (db.session.query(User)
                .filter(User.tenant_id==__tenant__.tenant_id)
                .all())
    rv = dict(users=[])
    for r in records:
        rv['users'].append(_get_user(r))
    return rv

def _get_user(r):
    return dict(
        user_id=r.user_id,
        email=r.email,
        first_name=r.first_name,
        last_name=r.last_name,
        status=r.status,
        lang=r.lang,
    )


def get_user(user_id):
    user = db.session.query(User).get(user_id)
    return {"user_id": user.user_id,
            "email": user.email,
            'path': request.path}

def post_user(__data__):
    user = User(tenant_id=1, **__data__)
    db.session.add(user)
    db.session.flush()
    return {'user_id': user.user_id}

def get_user_token(user_id):
    user = db.session.query(User).get(user_id)
    rv = dict(
        user_id=user.user_id,
        token=user.token,
    )
    return rv

def user_login(username, password, tenant_id=1):
    query = db.session.query(User).filter(User.email==username)
    try:
        user = rv = (query.filter(User.tenant_id==tenant_id) 
                     if tenant_id else query).one()
    except:
        user = rv = None

    if user:
        if not password==user.token:
            user.token = None
            if user.failed_attempts:
                user.failed_attempts += 1
            else:
                user.failed_attempts = 1
            if user.authenticate(password):
                user.new_token()
                user.failed_attempts = 0
            else:
                rv = None
            db.session.flush()
    return rv

def get_roles():
    pass

def get_role(role_id):
    pass

def put_role(role_id):
    pass

def post_role(__data__):
    r = Role(**__data__)
    db.session.add(r)
    db.session.flush()
    return {}

def delete_role(role_id):
    pass
