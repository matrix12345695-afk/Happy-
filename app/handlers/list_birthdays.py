from aiogram import Router
from aiogram.types import Message
from sqlalchemy import select

from app.database import async_session
from app.models import Birthday

router = Router()

@router.message(lambda msg: msg.text == "/list")
async def list_birthdays(message: Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    async with async_session() as session:
        result = await session.execute(select(Birthday))
        data = result.scalars().all()

    if not data:
        await message.answer("📭 Пусто")
        return

    text = "🎂 Список:\n"
    for b in data:
        text += f"{b.full_name} — {b.birth_date.strftime('%d-%m')}\n"

    await message.answer(text)
