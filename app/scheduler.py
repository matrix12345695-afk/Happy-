from datetime import date, datetime, timedelta
from sqlalchemy import select
from app.database import async_session
from app.models import Birthday
import random


# 🎂 Основные напоминания (за 30 / 14 / 2 / 1 / 0 дней)
async def check_birthdays(bot):
    async with async_session() as session:
        result = await session.execute(select(Birthday))
        birthdays = result.scalars().all()

    now = datetime.utcnow() + timedelta(hours=5)
    today = now.date()

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


# 🎉 Режим праздника по времени
async def birthday_party_by_time(bot):
    async with async_session() as session:
        result = await session.execute(select(Birthday))
        birthdays = result.scalars().all()

    now_dt = datetime.utcnow() + timedelta(hours=5)
    today = now_dt.date()
    now = now_dt.strftime("%H:%M")

    birthday_people = []

    for b in birthdays:
        bday = b.birth_date.replace(year=today.year)
        if bday == today:
            birthday_people.append(b.full_name)

    if not birthday_people:
        return

    name = ", ".join(birthday_people)

    messages = {
        "00:01": f"🎉🎉🎉 Сегодня день рождения у {name.upper()}!!! 🎂🥳",
        "09:00": f"🥳 Не забываем поздравлять {name}!",
        "12:00": f"🍰 Кто ещё не поздравил {name}? 😄",
        "18:00": f"🎊 Праздник продолжается! {name} сегодня главный герой!",
        "21:00": f"🔥 Завершаем день красиво — ещё раз поздравляем {name}!"
    }

    if now in messages:
        await bot.send_message(birthdays[0].chat_id, messages[now])
