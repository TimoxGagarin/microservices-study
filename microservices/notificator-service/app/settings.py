import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis import Redis
from uvloop import EventLoopPolicy

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    REDIS_HOST: str
    REDIS_PORT: int

    router: Router = Router()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def bot(self) -> Bot:
        return Bot(
            token=self.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    @property
    def redis_conn(self) -> Redis:
        return Redis(host=self.REDIS_HOST, port=self.REDIS_PORT, decode_responses=True)

    @property
    def storage(self) -> RedisStorage:
        return RedisStorage.from_url(f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}")

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        asyncio.set_event_loop_policy(EventLoopPolicy())
        return asyncio.get_event_loop()

    @property
    def dispatcher(self) -> Dispatcher:
        dp = Dispatcher(loop=self.loop, storage=self.storage)
        dp.include_router(self.router)
        return dp


setting = Settings()
