from contextlib import asynccontextmanager
from fastapi import FastAPI
from aiohttp import ClientSession, ClientTimeout

from app.api.user import router
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    timeout = ClientTimeout(total=30)  # Таймаут на весь запрос
    app.state.http_session = ClientSession(timeout=timeout)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await app.state.http_session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router)