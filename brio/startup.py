from .config import conf
from proto import API
from proto import local
from proto import request
from proto.database import SQLAlchemy 

application = app = API(conf, default_multitenancy=True)
db = SQLAlchemy(app.config)
