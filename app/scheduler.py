from datetime import date
from sqlalchemy import select
from app.database import async_session
from app.models import Birthday
import random


async def check_birthdays(bot):
    async with async_session() as session:
        result = await session.execute(select(Birthday))
        birthdays = result.scalars().all()

    today = date.today()

    for b in birthdays:
        bday = b.birth_date.replace(year=today.year)
        delta = (bday - today).days

        if delta == 30:
            text = f"🎂 Через месяц день рождения у {b.full_name} 🎁"

        elif delta == 14:
            text = f"📅 Через 2 недели у {b.full_name} праздник"

        elif delta == 2:
            text = f"🔥 Через 2 дня день рождения у {b.full_name}"

        elif delta == 1:
            text = f"⚠️ Завтра день рождения у {b.full_name}!"

        elif delta == 0:
            wishes = [
                "🚀 Пусть все цели достигаются легко!",
                "💰 Денег столько, чтобы считать надоело!",
                "🔥 Жизнь как сериал — только без плохих сезонов!",
                "🎯 Удача всегда на твоей стороне!",
                "🏆 Успех приходит быстрее, чем ожидания!"
            ]

            text = (
                f"🎉🎉🎉 ВНИМАНИЕ!!! 🎉🎉🎉\n\n"
                f"🔥 Сегодня день рождения у {b.full_name.upper()}!!! 🔥\n\n"
                f"{random.choice(wishes)}\n\n"
                f"🎂 Пусть жизнь будет сладкой как торт\n"
                f"💰 Деньги приходят без задержек\n"
                f"🚀 Цели достигаются быстрее дедлайнов\n"
                f"💪 Здоровье крепче стали\n\n"
                f"🥳 С ДНЁМ РОЖДЕНИЯ!!! 🥳"
            )

        else:
            continue

        await bot.send_message(b.chat_id, text)
