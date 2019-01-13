import datetime
import typing
from dataclasses import InitVar, dataclass, field

import aiohttp

from . import GOOGLE_TOKEN_URI
from .helpers import NoAsDict


@dataclass
class Credentials:
    client_id: str
    client_secret: str
    scopes: typing.List[str]
    refresh_token: str
    expires_in: InitVar[int] = 0
    obtained_at: datetime.datetime = field(init=False, default_factory=datetime.datetime.now)
    expires_at: datetime.datetime = field(init=False)
    access_token: str = None

    def __post_init__(self, expires_in: int):
        self.expires_at = self.obtained_at + datetime.timedelta(seconds=expires_in)

    def __make_refresh_json(self) -> dict:
        return {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }

    def is_fresh(self, stock: datetime.timedelta = datetime.timedelta()) -> bool:
        return datetime.datetime.now() + stock <= self.expires_at

    async def refresh(self, session: aiohttp.ClientSession) -> typing.NoReturn:
        async with session.post(url=GOOGLE_TOKEN_URI,
                                json=self.__make_refresh_json(),
                                raise_for_status=True) as r:
            response = await r.json()
            self.obtained_at = datetime.datetime.now()
            self.expires_at = self.obtained_at + datetime.timedelta(seconds=response['expires_in'])
            self.access_token = response['access_token']


@dataclass
class Person:
    id: str = NoAsDict
    email: str = NoAsDict
    displayName: str = NoAsDict
    self: bool = NoAsDict


@dataclass
class Time:
    timeZone: str = NoAsDict
    date: str = NoAsDict
    dateTime: str = NoAsDict


@dataclass
class Event:
    kind: str = NoAsDict
    etag: str = NoAsDict
    id: str = NoAsDict
    status: str = NoAsDict
    htmlLink: str = NoAsDict
    created: str = NoAsDict
    updated: str = NoAsDict
    summary: str = NoAsDict
    description: str = NoAsDict
    location: str = NoAsDict
    colorId: str = NoAsDict
    creator: typing.Union[dict, Person] = NoAsDict
    organizer: typing.Union[dict, Person] = NoAsDict
    start: typing.Union[dict, Time] = NoAsDict
    end: typing.Union[dict, Time] = NoAsDict
    endTimeUnspecified: bool = NoAsDict
    recurrence: typing.List[str] = NoAsDict
    recurringEventId: str = NoAsDict
    originalStartTime: typing.Union[dict, Time] = NoAsDict
    transparency: str = NoAsDict
    visibility: str = NoAsDict
    iCalUID: str = NoAsDict
    sequence: int = NoAsDict
    attendee: typing.List[dict] = NoAsDict
    attendeesOmitted: bool = NoAsDict
    extendedProperties: dict = NoAsDict
    hangoutLink: str = NoAsDict
    conferenceData: dict = NoAsDict
    anyoneCanAddSelf: bool = NoAsDict
    guestsCanInviteOthers: bool = NoAsDict
    guestsCanModify: bool = NoAsDict
    guestsCanSeeOtherGuests: bool = NoAsDict
    privateCopy: bool = NoAsDict
    locked: bool = NoAsDict
    reminders: dict = NoAsDict
    source: dict = NoAsDict
    attachments: typing.List[dict] = NoAsDict

    def __post_init__(self):
        if isinstance(self.start, dict):
            self.start = Time(**self.start)
        if isinstance(self.end, dict):
            self.end = Time(**self.end)
        if isinstance(self.creator, dict):
            self.creator = Person(**self.creator)
        if isinstance(self.organizer, dict):
            self.organizer = Person(**self.organizer)


@dataclass
class Interval:
    start: str = NoAsDict
    end: str = NoAsDict


@dataclass
class _FreeBusyCalendar:
    errors: typing.List[typing.Dict[str, str]] = NoAsDict
    busy: typing.List[typing.Union[dict, Interval]] = NoAsDict

    def __post_init__(self):
        for i, b in enumerate(self.busy):
            if isinstance(b, dict):
                self.busy[i] = Interval(**b)


@dataclass
class FreeBusy:
    kind: str = NoAsDict
    timeMin: typing.Union[dict, Time] = NoAsDict
    timeMax: typing.Union[dict, Time] = NoAsDict
    groups: dict = NoAsDict
    calendars: typing.Dict[str, _FreeBusyCalendar] = NoAsDict

    def __post_init__(self):
        if isinstance(self.timeMin, dict):
            self.timeMin = Time(**self.timeMin)
        if isinstance(self.timeMax, dict):
            self.timeMax = Time(**self.timeMax)
        if isinstance(self.calendars, dict):
            for k, v in self.calendars.items():
                if isinstance(v, dict):
                    self.calendars[k] = _FreeBusyCalendar(**v)
