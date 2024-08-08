from sqlalchemy import delete, select, update

from app.api.db import Movies, async_session
from app.api.models import MovieIn


async def add_movie(payload: MovieIn):
    async with async_session() as session:
        new_user = Movies(**payload.model_dump())
        session.add(new_user)
        await session.commit()
        return new_user.id


async def get_all_movies():
    async with async_session() as session:
        query = select(Movies)
        res = await session.execute(query)
        return res.scalars().all()


async def get_movie(id: int):
    async with async_session() as session:
        query = select(Movies).where(Movies.id == id)
        return (await session.execute(query)).first()


async def delete_movie(id: int):
    async with async_session() as session:
        query = delete(Movies).where(Movies.id == id)
        await session.execute(query)
        await session.commit()


async def update_movie(id: int, payload: MovieIn):
    async with async_session() as session:
        query = update(Movies).where(Movies.id == id).values(**payload.model_dump())
        await session.execute(query)
        await session.commit()
