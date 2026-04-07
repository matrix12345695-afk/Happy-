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
    await message.answer("📅 Введи дату (ДД-ММ или ДД-ММ-ГГГГ):")
    await state.set_state(AddBirthday.date)

@router.message(AddBirthday.date)
async def get_date(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]

    text = message.text.strip()

    # Поддержка разных форматов
    formats = ["%d-%m", "%d-%m-%Y", "%d.%m", "%d.%m.%Y"]

    birth_date = None

    for fmt in formats:
        try:
            parsed = datetime.strptime(text, fmt)
            if "%Y" not in fmt:
                parsed = parsed.replace(year=2000)
            birth_date = parsed.date()
            break
        except:
            continue

    if not birth_date:
        await message.answer("❌ Неверный формат. Пример: 26-05 или 26-05-2000")
        return

    async with async_session() as session:
        session.add(Birthday(
            full_name=name,
            birth_date=birth_date,
            chat_id=message.chat.id
        ))
        await session.commit()

    await message.answer(f"✅ Добавлен: {name} ({birth_date.strftime('%d-%m')})")
    await state.clear()
