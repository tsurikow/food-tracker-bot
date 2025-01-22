from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.exceptions import AiogramError
from sqlalchemy.ext.asyncio import AsyncSession

from app.states.states import Food
from app.utils.gpt import get_gpt_food
from database.db_commands import db_update_log_food

router = Router(name="food-router")

@router.message(Command("log_food"))
async def start_log_food(message: Message, state: FSMContext):
    await message.reply("Введите название продукта для учета калорий")
    await state.set_state(Food.name)

@router.message(Food.name)
async def process_food_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply("Введите массу продукта в граммах")
    await state.set_state(Food.weight)

@router.message(Food.weight)
async def process_food_weight(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    name = data.get("name")
    weight = int(data.get("weight"))
    try:
        food_info = await get_gpt_food(name)
        await message.reply(f"{name} – калорийность {food_info} ккал на 100 грамм")
        log_food = food_info / 100 * weight
        await message.reply(f"Всего потреблено {log_food} ккал")
        await db_update_log_food(log_food, message, session)
    except AiogramError as e:
        await message.reply('Не удалось получить информацию о калорийности!')
        await message.reply(e)
    await state.clear()
