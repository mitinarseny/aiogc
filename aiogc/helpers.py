import functools
import typing

import aiohttp


class NoAsDict:
    ...


def _no_as_dict_factory(kvs: typing.List[typing.Tuple[str, typing.Any]]) -> dict:
    res = dict()
    for k, v in kvs:
        if not (type(v) is type and issubclass(v, NoAsDict)):
            res[k] = v
    return res


def _make_authorization_header(access_token: str) -> dict:
    return {
        'Authorization': f'Bearer {access_token}'
    }


from .models import Credentials


def fresh_credentials(func):
    @functools.wraps(func)
    async def wrapper(credentials: Credentials, session: aiohttp.ClientSession, **kwargs):
        if not credentials.is_fresh():
            await credentials.refresh(session)
        return await func(credentials=credentials, session=session, **kwargs)

    return wrapper
