from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import *

router = Router(name="progress-router")


@router.message(Command("check_progress"))
async def check_progress(message: Message, session: AsyncSession):
    water_goal = await db_get_water_goal(message, session)
    logged_water = await db_get_logged_water(message, session)
    logged_calories = await db_get_logged_calories(message, session)
    calorie_goal = await db_get_calorie_goal(message, session)
    burned_calories = await db_get_burned_calories(message, session)
    await message.reply(
        f"Ваш прогресс на сегодня \n"
        f"\n"
        f"Выпито – {logged_water} из {water_goal} мл.\n"
        f"Осталось выпить – {water_goal - logged_water} мл.\n"
        f"\n"
        f"Потреблено калорий – {logged_calories} из {calorie_goal} ккал.\n"
        f"Сожжено калорий – {burned_calories} ккал.\n"
        f"Баланс – {logged_calories - burned_calories} ккал.\n"
    )
