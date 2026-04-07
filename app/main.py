import asyncio
import os
from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.init_db import init_db
from app.handlers import add_birthday, list_birthdays, delete_birthday
from app.scheduler import check_birthdays

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()
scheduler = AsyncIOScheduler()

dp.include_router(add_birthday.router)
dp.include_router(list_birthdays.router)
dp.include_router(delete_birthday.router)

@app.get("/")
def root():
    return {"status": "ok"}

@app.on_event("startup")
async def startup():
    await init_db()

    scheduler.add_job(check_birthdays, "interval", hours=24, args=[bot])
    scheduler.start()

    asyncio.create_task(dp.start_polling(bot))
