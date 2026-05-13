from aiohttp import ClientSession
from fastapi import Request

async def get_http_session(request: Request) -> ClientSession:
    return request.app.state.http_session