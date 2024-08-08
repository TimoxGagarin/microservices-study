from celery import Celery
from fastapi import APIRouter, Body

from app.settings import setting

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.api.notifications"],
)

celery.conf.update(
    result_expires=3600,
)


router = APIRouter()


@router.post("/send")
async def send_message_in_tg(user_id: int = Body(), message: dict = Body()):
    send_message_to_user.delay(user_id, message)
    return {
        "status": 200,
        "data": "Message sent",
        "details": None,
    }


@celery.task
def send_message_to_user(user_id: int = Body(), message: dict = Body()) -> dict:
    import asyncio

    async def send_message():
        await setting.bot.send_message(chat_id=user_id, text=str(message))

    asyncio.run(send_message())
    return {"status": "success"}
