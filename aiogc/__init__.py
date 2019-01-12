GOOGLEAPIS_BASE_URL = 'https://www.googleapis.com'
GOOGLE_TOKEN_URI = 'https://oauth2.googleapis.com/token'

name = "aiogc"
__version__ = '0.1.1'

from . import events
from models import Credentials, Event, Time, Person
