from aiogram import Router
from aiogram.types import Message
from sqlalchemy import select
from datetime import datetime, timedelta

from app.database import async_session
from app.models import Birthday

router = Router()

@router.message(lambda msg: msg.text == "/next")
async def next_birthdays(message: Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    async with async_session() as session:
        result = await session.execute(select(Birthday))
        birthdays = result.scalars().all()

    if not birthdays:
        await message.answer("📭 Список пуст")
        return

    now = datetime.utcnow() + timedelta(hours=5)
    today = now.date()

    def days_left(b):
        bday = b.birth_date.replace(year=today.year)
        if bday < today:
            bday = bday.replace(year=today.year + 1)
        return (bday - today).days

    birthdays.sort(key=days_left)

    text = "🔥 Ближайшие дни рождения:\n\n"

    for b in birthdays[:5]:
        text += f"{b.full_name} — через {days_left(b)} дн.\n"

    await message.answer(text)
