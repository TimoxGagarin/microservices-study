import os

from dotenv import load_dotenv
from sqlalchemy import ARRAY, Column, Integer, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")


sync_engine = create_engine(SYNC_DATABASE_URL)
async_engine = create_async_engine(ASYNC_DATABASE_URL)

async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    def to_dict(self):
        return {k: self.__dict__[k] for k in self.__dict__ if "_sa_" != k[:4]}

    def __repr__(self):
        return f"<{self.__class__.__name__}({[', '.join('%s=%s' % (k, self.__dict__[k]) for k in self.__dict__ if '_sa_' != k[:4])]}"


class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    plot = Column(String(250))
    genres = Column(ARRAY(String))
    casts = Column(ARRAY(Integer))


def create_tables():
    Base.metadata.create_all(bind=sync_engine)
