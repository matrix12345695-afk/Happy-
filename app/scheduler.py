from datetime import date
from sqlalchemy import select
from app.database import async_session
from app.models import Birthday

async def check_birthdays(bot):
    async with async_session() as session:
        result = await session.execute(select(Birthday))
        birthdays = result.scalars().all()

    today = date.today()

    for b in birthdays:
        bday = b.birth_date.replace(year=today.year)
        delta = (bday - today).days

        if delta in [30, 14, 2, 1, 0]:
            if delta == 0:
                text = f"🎉 Сегодня день рождения у {b.full_name}!!!"
            else:
                text = f"🎂 Через {delta} дн. день рождения у {b.full_name}"

            await bot.send_message(b.chat_id, text)
