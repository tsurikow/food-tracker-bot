from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="general-router")


# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply(
        "Добро пожаловать! Я ваш бот для учета калорийности еды.\n"
        "Введите /help для списка команд."
    )


# Обработчик команды /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(
        "Доступные команды:\n"
        "/set_profile – настройка профиля\n"
        "/log_water – логирование воды\n"
        "/log_food – логирование еды\n"
        "/log_workout <тип тренировки> <время (мин)> – логирование тренировок\n"
        "/check_progress – прогресс по воде и калориям\n"
        "/recommend – рекомендация по питанию и тренировке\n"
    )