from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User


async def db_add_to_db(item, message: Message, session: AsyncSession):
    session.add(item)
    try:
        await session.commit()
        await session.refresh(item)
        return item
    except IntegrityError as ex:
        await session.rollback()
        await message.answer("DB error!")
        await message.answer(ex)


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
    except IntegrityError as ex:
        await session.rollback()
        await message.answer("DB error!")
        await message.answer(ex.args[0])
        return False


async def db_get_all_users(message: Message, session: AsyncSession):
    sql = select(User)
    users_sql = await session.execute(sql)
    users = users_sql.scalars()

    users_list = "\n".join([f"{index + 1}. {item.tg_id}" for index, item in enumerate(users)])

    return users_list
