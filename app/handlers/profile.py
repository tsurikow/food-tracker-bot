from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.states.states import Profile
from app.utils.calculate import calculate_norm
from app.utils.gpt import get_gpt_temp
from database.db_commands import db_register_user

router = Router(name="profile-router")


# FSM: диалог с пользователем
@router.message(Command("set_profile"))
async def start_form(message: Message, state: FSMContext):
    await message.reply("Как вас зовут?")
    await state.set_state(Profile.name)


@router.message(Profile.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply("Сколько вам лет?")
    await state.set_state(Profile.age)


@router.message(Profile.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply("Введите свой вес:")
    await state.set_state(Profile.weight)


@router.message(Profile.weight)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.reply("Введите свой рост:")
    await state.set_state(Profile.height)


@router.message(Profile.height)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await message.reply("Сколько минут активности у вас в день?")
    await state.set_state(Profile.activity)


@router.message(Profile.activity)
async def process_activity(message: Message, state: FSMContext):
    await state.update_data(activity=message.text)
    await message.reply("В каком городе вы находитесь?")
    await state.set_state(Profile.city)


@router.message(Profile.city)
async def process_city(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(city=message.text)
    data = await state.get_data()
    name = data.get("name")
    age = int(data.get("age"))
    weight = int(data.get("weight"))
    height = int(data.get("height"))
    activity = int(data.get("activity"))
    city = data.get("city")
    temp = await get_gpt_temp(city)
    water_goal, calorie_goal = calculate_norm(age, weight, height, activity, temp)
    await message.reply(f"Профиль заполнен успешно, {name}!")
    await message.reply(f"Текущая температура в {city}: {temp} градусов Цельсия")
    await db_register_user(
        name, age, weight, height, activity, city, water_goal, calorie_goal, message, session
    )
    await message.reply("Информация сохранена в базу данных!")
    await state.clear()
