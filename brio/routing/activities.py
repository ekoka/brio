from brio.startup import app
from brio.operations import activities 

app.add_route('/{tenant}/activities', activities.get_activities, 
              methods=['GET'])
app.add_route('/{tenant}/activities/{activity_id:int}', 
              activities.get_activity, methods=['GET'])
