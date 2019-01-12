# aiogc
> Async Google Calendar API Client for Python 3

## Installation

Run this in your terminal:
```commandLine
pip install aiogc
```

## Usage
Following code prints summary and `start` and `end` datetimes of upcoming events within nearest 5 days.
```python
import asyncio
import datetime

import aiohttp

from aiogc import events, models

c = models.Credentials(
	client_id='<your_client_id>',
    client_secret='<your_client_secret>',
    scopes=['<your_scope1>', 'your_scope2'],
    refresh_token='<your_refresh_token>'
)

async def main():
	async with aiohttp.ClientSession() as s:
		es = await events.list(
			calendar_id='<your_calendar_id>',
			credentials=c,
			session=s,
			singleEvents='true',
			timeMin=datetime.datetime.now().isoformat(),
			timeMax=(datetime.datetime.now() + datetime.timedelta(days=5)).isoformat(),
			orderBy='startTime',
		)
		for e in es:
			print(f'{e.summary}:\n{e.start.dateTime} – {e.end.dateTime}')

if __name__=='__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
```