from contextlib import asynccontextmanager

import sentry_sdk
from app.api.db import create_tables
from app.api.movies import movies
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

sentry_sdk.init()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/v1/movies/openapi.json",
    docs_url="/api/v1/movies/docs",
)
app.include_router(movies, prefix="/api/v1/movies", tags=["movies"])
