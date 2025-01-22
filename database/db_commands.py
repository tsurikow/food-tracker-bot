from aiogram.types import Message
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User


async def db_register_user(
    name,
    age,
    weight,
    height,
    activity,
    city,
    water_goal,
    calorie_goal,
    message: Message,
    session: AsyncSession,
):
    username = message.from_user.username if message.from_user.username else "Unknown"

    user = User(
        tg_id=int(message.from_user.id),
        user_name=username,
        name=name,
        age=int(age),
        weight=int(weight),
        height=int(height),
        activity=int(activity),
        water_goal=int(water_goal),
        calorie_goal=int(calorie_goal),
        logged_water=int(0),
        logged_calories=int(0),
        burned_calories=int(0),
        city=city,
    )

    session.add(user)

    try:
        await session.commit()
        await session.refresh(user)
        return True
    except IntegrityError:
        await session.rollback()
        await message.answer(
            "Не удалось сохранить профиль!\nВозможно, профиль уже зарегистрирован."
        )
        return False


async def db_update_burn_calories(burn_calories, message: Message, session: AsyncSession):
    await session.execute(
        update(User)
        .where(User.tg_id == message.from_user.id)
        .values(burned_calories=User.burned_calories + int(burn_calories))
    )

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        await message.answer("Не удалось сохранить сожженные калории!\nОшибка базы данных.")


async def db_update_water_goal(add_water, message: Message, session: AsyncSession):
    await session.execute(
        update(User)
        .where(User.tg_id == message.from_user.id)
        .values(water_goal=User.water_goal + int(add_water))
    )

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        await message.answer("Норма воды не была обновлена!\nОшибка базы данных.")


async def db_update_log_food(log_calories, message: Message, session: AsyncSession):
    await session.execute(
        update(User)
        .where(User.tg_id == message.from_user.id)
        .values(logged_calories=User.logged_calories + int(log_calories))
    )

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        await message.answer("Не удалось сохранить потребленные калории!\nОшибка базы данных.")


async def db_update_log_water(log_water, message: Message, session: AsyncSession):
    await session.execute(
        update(User)
        .where(User.tg_id == message.from_user.id)
        .values(logged_water=User.logged_water + int(log_water))
    )

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        await message.answer("Не удалось сохранить выпитую воду!\nОшибка базы данных.")


async def db_get_water_goal(message: Message, session: AsyncSession):
    water_goal = await session.execute(
        select(User.water_goal).where(User.tg_id == message.from_user.id)
    )

    try:
        await session.commit()
        return water_goal.scalar()
    except IntegrityError:
        await session.rollback()
        await message.answer("Не удалось загрузить вашу норму!\nОшибка базы данных.")


async def db_get_logged_water(message: Message, session: AsyncSession):
    logged_water = await session.execute(
        select(User.logged_water).where(User.tg_id == message.from_user.id)
    )

    try:
        await session.commit()
        return logged_water.scalar()
    except IntegrityError:
        await session.rollback()
        await message.answer("Не удалось загрузить выпитую воду!\nОшибка базы данных.")


async def db_get_calorie_goal(message: Message, session: AsyncSession):
    calorie_goal = await session.execute(
        select(User.calorie_goal).where(User.tg_id == message.from_user.id)
    )

    try:
        await session.commit()
        return calorie_goal.scalar()
    except IntegrityError:
        await session.rollback()
        await message.answer("Не удалось загрузить цель по калориям!\nОшибка базы данных.")


async def db_get_logged_calories(message: Message, session: AsyncSession):
    logged_calories = await session.execute(
        select(User.logged_calories).where(User.tg_id == message.from_user.id)
    )

    try:
        await session.commit()
        return logged_calories.scalar()
    except IntegrityError:
        await session.rollback()
        await message.answer("Не удалось загрузить потребленные калории!\nОшибка базы данных.")


async def db_get_burned_calories(message: Message, session: AsyncSession):
    burned_calories = await session.execute(
        select(User.burned_calories).where(User.tg_id == message.from_user.id)
    )

    try:
        await session.commit()
        return burned_calories.scalar()
    except IntegrityError:
        await session.rollback()
        await message.answer("Не удалось загрузить сожженные калории!\nОшибка базы данных.")
