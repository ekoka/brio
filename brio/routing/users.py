from brio.startup import app
from brio.operations import users
from brio.models.users import authorize_owner

app.add_route('/{tenant}/users', users.get_users, methods=['GET'], 
              authorization=['admin'])
app.add_route('/{tenant}/users', users.post_user, methods=['POST'], 
              authorization=['admin'])
app.add_route('/{tenant}/users/{user_id:int}', users.get_user, methods=['GET'],
              authorization=['admin'])
app.add_route('/{tenant}/users/{user_id:int}/token', users.get_user_token, 
              methods=['GET'], authorization=[authorize_owner('user_id'), 
                                              'admin', ])
app.add_route('/{tenant}/roles', users.post_role, methods=['POST'], 
              tenants=['mudplay'], authorization=['admin'],)
