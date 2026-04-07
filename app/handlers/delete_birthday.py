from aiogram import Router
from aiogram.types import Message
from sqlalchemy import delete

from app.database import async_session
from app.models import Birthday

router = Router()

@router.message(lambda msg: msg.text.startswith("/delete"))
async def delete_birthday(message: Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    try:
        name = message.text.split(" ", 1)[1]
    except:
        await message.answer("❌ Пример: /delete Иван")
        return

    async with async_session() as session:
        await session.execute(delete(Birthday).where(Birthday.full_name == name))
        await session.commit()

    await message.answer(f"🗑 Удалён {name}")
