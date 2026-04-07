import asyncio
import os
import httpx

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.init_db import init_db
from app.handlers import add_birthday, list_birthdays, delete_birthday, import_birthdays
from app.scheduler import check_birthdays, birthday_party_by_time

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()
scheduler = AsyncIOScheduler()

# Подключаем все роутеры
dp.include_router(add_birthday.router)
dp.include_router(list_birthdays.router)
dp.include_router(delete_birthday.router)
dp.include_router(import_birthdays.router)


@app.get("/")
def root():
    return {"status": "ok"}


# 🔁 Самопинг (чтобы не засыпал)
async def self_ping():
    url = os.getenv("RENDER_EXTERNAL_URL")

    if not url:
        print("❌ RENDER_EXTERNAL_URL не найден")
        return

    while True:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(url)
                print(f"🔁 self-ping: {r.status_code}")
        except Exception as e:
            print(f"❌ ping error: {e}")

        await asyncio.sleep(240)  # каждые 4 минуты


@app.on_event("startup")
async def startup():
    await init_db()

    # 🎂 Основные напоминания
    scheduler.add_job(check_birthdays, "interval", hours=24, args=[bot])

    # 🎉 Режим праздника по времени
    scheduler.add_job(birthday_party_by_time, "interval", minutes=1, args=[bot])

    scheduler.start()

    asyncio.create_task(dp.start_polling(bot))
    asyncio.create_task(self_ping())
