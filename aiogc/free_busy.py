import typing

import aiohttp

from . import GOOGLEAPIS_BASE_URL
from .helpers import _make_authorization_header, fresh_credentials
from .models import Credentials, FreeBusy
import datetime


@fresh_credentials
async def query(*,
                time_min: datetime.datetime,
                time_max: datetime.datetime,
                calendar_or_group_ids: typing.List[str],
                credentials: Credentials,
                session: aiohttp.ClientSession,
                version: str = 'v3',
                **params) -> FreeBusy:
    async with session.post(
            url=f'{GOOGLEAPIS_BASE_URL}/calendar/{version}/freeBusy',
            json={
                'timeMin': time_min.isoformat(),
                'timeMax': time_max.isoformat(),
                'items': [{
                    'id': i
                } for i in calendar_or_group_ids],
                **params
            },
            headers=_make_authorization_header(credentials.access_token),
            raise_for_status=True
    ) as r:
        return FreeBusy(**(await r.json()))
