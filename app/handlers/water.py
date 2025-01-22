from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.states.states import Water
from database.db_commands import db_update_log_water, db_get_water_goal, db_get_logged_water

router = Router(name="water-router")

@router.message(Command("log_water"))
async def start_log_water(message: Message, state: FSMContext):
    await message.reply("Сколько воды было выпито в миллилитрах?")
    await state.set_state(Water.volume)

@router.message(Water.volume)
async def process_food_volume(message: Message, state: FSMContext, session: AsyncSession):
    volume = message.text
    await state.update_data(volume=volume)
    await db_update_log_water(int(volume), message, session)
    await message.reply("Информация успешно сохранена!")
    water_goal = await db_get_water_goal(message, session)
    logged_water = await db_get_logged_water(message, session)
    await message.reply(f"Ваша норма воды сегодня – {water_goal} мл. \n"
                        f"Выпито всего – {logged_water} мл. \n"
                        f"Осталось выпить – {water_goal - logged_water} мл.")

    await state.clear()
