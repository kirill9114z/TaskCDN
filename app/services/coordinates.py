import asyncio
from typing import Coroutine
from functools import wraps
from aiohttp import ClientSession
from aiohttp import ClientResponseError, ClientConnectorError, ClientError

from app.core.config import settings


def retrying_http_err(func: Coroutine):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        last_exc = None
        for attempt in range(settings.MAX_RETRIES):
            try:
                return await func(*args, **kwargs)
            except ClientConnectorError as err:
                last_exc = err
                print(f'attempt: {attempt} | Connection error: {err}')

            except ClientResponseError as err:
                if err.status not in settings.RETRY_STATUSES:
                    print(f'Client error: {err}')
                    return None

                last_exc = err
                print(f"Response error: {err}")

            except ClientError as err:
                last_exc = err
                print(f'Client error: {err}')

            except Exception as err:
                print(f'Unexpected error: {err}')
                return None

            await asyncio.sleep(settings.DELAY + attempt)
        raise last_exc
    return wrapper

@retrying_http_err
async def get_city_coordinates(city_name: str, session: ClientSession):
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }
    async with session.get(settings.BASE_URL, params=params, headers=settings.HEADERS) as response:
        data = await response.json()
        if data:
            city_data = data[0]
            return {
                "lat": float(city_data["lat"]),
                "lon": float(city_data["lon"]),
            }
        return None






