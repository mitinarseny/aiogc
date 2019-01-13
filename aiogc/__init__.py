GOOGLEAPIS_BASE_URL = 'https://www.googleapis.com'
GOOGLE_TOKEN_URI = 'https://oauth2.googleapis.com/token'

__name__ = "aiogc"

from . import events, free_busy
from .models import Credentials, Event, Interval, Person, Time