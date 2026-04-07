import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_birthday_text(name: str):
    prompt = f"""
Напиши яркое, живое поздравление с днем рождения для человека по имени {name}.
Стиль: дружелюбный, немного дерзкий, современный.
Добавь эмоции, эмодзи, юмор.
Не делай слишком длинно (6-10 строк).
"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты пишешь крутые поздравления."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9
    )

    return response.choices[0].message.content