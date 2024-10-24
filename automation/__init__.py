import os, pytz
from flask import Flask
from .core import PyAutomation


app = Flask(__name__, instance_relative_config=False)

MANUFACTURER = os.environ.get('MANUFACTURER')
SEGMENT = os.environ.get('SEGMENT')
TIMEZONE = os.environ.get('TIMEZONE') or "America/Caracas"
TIMEZONE = pytz.timezone(TIMEZONE)
CERT_FILE = os.path.join(".", "ssl", os.environ.get('CERT_FILE') or "")
KEY_FILE = os.path.join(".", "ssl", os.environ.get('KEY_FILE') or "")
if not os.path.isfile(CERT_FILE):
    CERT_FILE = None

if not os.path.isfile(KEY_FILE):
    KEY_FILE = None

class CreateApp():
    """Initialize the core application."""


    def __call__(self):
        """
        Documentation here
        """
        app.client = None
        self.application = app
        
        with app.app_context():

            from . import extensions
            extensions.init_app(app)

            from . import modules
            modules.init_app(app)
            
            return app
        
__application = CreateApp()
server = __application()    
server.config['TPT_TOKEN'] = '073821603fcc483f9afee3f1500782a4'
