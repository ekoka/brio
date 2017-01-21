# coding=utf-8

# LOGGER
#fh = logging.FileHandler(conf.LOGGING_PATH)
#logger = logging.getLogger('mudplay')
#logger.setLevel(logging.INFO)
#logger.addHandler(fh)

from proto import AuthMiddleware, GlobalsMiddleWare, TenantMiddleware
from .startup import application, db
from .routing import (
    activities,
    tenants,
    users,
)
from .operations.users import user_login
from .operations.tenants import get_tenant_from_name as get_tenant

#db.drop_all()
db.create_all()
application.db = db

for m in (GlobalsMiddleWare(application),
          TenantMiddleware(application, get_tenant),
          AuthMiddleware(application, user_login),):
    application.middleware.append(m)

application.serve()
