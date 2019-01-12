import typing
from dataclasses import asdict

import aiohttp

from . import GOOGLEAPIS_BASE_URL
from .helpers import (_make_authorization_header,
                      _no_as_dict_factory,
                      fresh_credentials)
from .models import Credentials, Event


@fresh_credentials
async def list(*,
               calendar_id: str,
               credentials: Credentials,
               session: aiohttp.ClientSession,
               version: str = 'v3',
               **params) -> typing.Generator[Event, None, None]:
    if not credentials.is_fresh():
        await credentials.refresh(session)
    async with session.get(
            url=f'{GOOGLEAPIS_BASE_URL}/calendar/{version}/calendars/{calendar_id}/events',
            params=params,
            headers=_make_authorization_header(credentials.access_token),
            raise_for_status=True
    ) as r:
        return (Event(**_) for _ in (await r.json())['items'])


@fresh_credentials
async def insert(calendar_id: str,
                 event: Event,
                 credentials: Credentials,
                 session: aiohttp.ClientSession,
                 version: str = 'v3') -> Event:
    async with session.post(
            url=f'{GOOGLEAPIS_BASE_URL}/calendar/{version}/calendars/{calendar_id}/events',
            json=asdict(event, dict_factory=_no_as_dict_factory),
            headers=_make_authorization_header(credentials.access_token),
            raise_for_status=True
    ) as r:
        return Event(**(await r.json()))


@fresh_credentials
async def delete(calendar_id: str,
                 evend_id: str,
                 credentials: Credentials,
                 session: aiohttp.ClientSession,
                 version: str = 'v3') -> None:
    await session.delete(
        url=f'{GOOGLEAPIS_BASE_URL}/calendar/{version}/calendars/{calendar_id}/events/{evend_id}',
        headers=_make_authorization_header(credentials.access_token),
        raise_for_status=True
    )
