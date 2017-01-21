from brio.startup import db
from brio.models import Tenant

def get_tenants():
    rows = db.session.query(Tenant).all()
    rv = {} 
    for r in rows: 
        rv.setdefault('tenants', []).append(_get_tenant(r))
    return rv

def _get_tenant(row):
    rv = dict(
        tenant_id=row.tenant_id,
        name=row.name,
    )
    return rv

def get_tenant(tenant_id):
    tenant = db.session.query(Tenant).get(tenant_id)
    return _get_tenant(tenant)

def post_tenant(__data__):
    tenant = Tenant(**__data__)
    db.session.add(tenant)
    db.session.flush()
    return {}

def get_tenant_from_name(tenant_name):
    try:
        return db.session.query(Tenant).filter(Tenant.name==tenant_name).one()
    except:
        pass
        
