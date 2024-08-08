from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.api.casts import casts
from app.api.db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/v1/casts/openapi.json",
    docs_url="/api/v1/casts/docs",
)
app.include_router(casts, prefix="/api/v1/casts", tags=["casts"])
