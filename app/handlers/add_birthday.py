from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from app.database import async_session
from app.models import Birthday

router = Router()

class AddBirthday(StatesGroup):
    name = State()
    date = State()

@router.message(F.text == "/add")
async def add_start(message: Message, state: FSMContext):
    if message.chat.type not in ["group", "supergroup"]:
        return

    await message.answer("👤 Введи имя:")
    await state.set_state(AddBirthday.name)

@router.message(AddBirthday.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📅 Дата (ДД-ММ):")
    await state.set_state(AddBirthday.date)

@router.message(AddBirthday.date)
async def get_date(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]

    try:
        date = datetime.strptime(message.text, "%d-%m")
        birth_date = date.replace(year=2000)
    except:
        await message.answer("❌ Ошибка формата")
        return

    async with async_session() as session:
        session.add(Birthday(
            full_name=name,
            birth_date=birth_date.date(),
            chat_id=message.chat.id
        ))
        await session.commit()

    await message.answer(f"✅ Добавлен {name}")
    await state.clear()
