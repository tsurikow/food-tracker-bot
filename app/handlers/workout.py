from aiogram import Router
from aiogram.exceptions import AiogramError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.states.states import Burn
from app.utils.gpt import get_gpt_train
from database.db_commands import db_update_burn_calories, db_update_water_goal

router = Router(name="workout-router")


@router.message(Command("log_workout"))
async def start_log_workout(message: Message, state: FSMContext):
    await message.reply("Каким видом тренировки вы занимались?")
    await state.set_state(Burn.name)


@router.message(Burn.name)
async def process_workout_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply("Сколько минут вы тренировались?")
    await state.set_state(Burn.time)


@router.message(Burn.time)
async def process_workout_time(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(time=message.text)
    data = await state.get_data()
    name = data.get("name")
    time = int(data.get("time"))
    add_water = int(time / 30 * 200)
    try:
        await db_update_water_goal(add_water, message, session)
        workout_info = await get_gpt_train(name)
        await message.reply(f"{name} – сжигание {workout_info} ккал на минуту")
        await message.reply(f"Норма воды увеличена на {add_water} мл.")
        log_workout = workout_info * time
        await message.reply(f"Всего вы сожгли {log_workout} ккал")
        await db_update_burn_calories(log_workout, message, session)
    except AiogramError as e:
        await message.reply("Не удалось получить информацию о тренировке!")
        await message.reply(e)
    await state.clear()
