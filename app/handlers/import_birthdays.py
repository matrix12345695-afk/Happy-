from aiogram import Router
from aiogram.types import Message
from datetime import datetime

from app.database import async_session
from app.models import Birthday

router = Router()

@router.message(lambda msg: msg.text.startswith("/import"))
async def import_birthdays(message: Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    lines = message.text.split("\n")[1:]  # пропускаем /import

    added = 0
    errors = 0

    async with async_session() as session:
        for line in lines:
            try:
                parts = line.strip().rsplit(" ", 1)
                name = parts[0]
                date_str = parts[1]

                birth_date = datetime.strptime(date_str, "%d-%m-%Y").date()

                session.add(Birthday(
                    full_name=name,
                    birth_date=birth_date,
                    chat_id=message.chat.id
                ))

                added += 1

            except:
                errors += 1

        await session.commit()

    await message.answer(
        f"🎂 Импорт завершён!\n\n"
        f"✅ Добавлено: {added}\n"
        f"❌ Ошибки: {errors}"
    )
