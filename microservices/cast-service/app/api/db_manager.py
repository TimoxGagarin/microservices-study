from app.api.db import Casts, async_session
from app.api.models import CastIn, CastOut, CastUpdate


async def add_cast(payload: CastIn):
    async with async_session() as session:
        new_cast = Casts(**payload.model_dump())
        session.add(new_cast)
        await session.commit()
        return new_cast.id


async def get_cast(id):
    async with async_session() as session:
        res = await session.get(Casts, id)
        return res
