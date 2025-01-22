from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.gpt import get_gpt_advice
from database.db_commands import *

router = Router(name="advice-router")


@router.message(Command("recommend"))
async def check_progress(message: Message, session: AsyncSession):
    logged_calories = await db_get_logged_calories(message, session)
    calorie_goal = await db_get_calorie_goal(message, session)
    burned_calories = await db_get_burned_calories(message, session)
    goal = int(calorie_goal - logged_calories + burned_calories)
    advice = await get_gpt_advice(goal)
    await message.reply(advice)
