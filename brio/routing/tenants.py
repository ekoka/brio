from brio.startup import app
from brio.operations import tenants
from brio.models.users import authorize_owner

app.add_route('/{tenant}/tenants', tenants.get_tenants, methods=['GET'], 
              tenants=['mudplay'], authorization=['admin'])
app.add_route('/{tenant}/tenants', tenants.post_tenant, methods=['POST'], 
              tenants=['mudplay'], authorization=['admin'])
app.add_route('/{tenant}/tenants/{tenant_id}', tenants.get_tenant, 
              methods=['GET'], tenants=['mudplay'], authorization=['admin'],)
