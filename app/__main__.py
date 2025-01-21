import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.handlers.handlers import setup_handlers
from app.middlewares.middlewares import DbSessionMiddleware, LoggingMiddleware
from config.config import DB_PATH, REDIS_URL, TOKEN


async def main():
    engine = create_async_engine(url=DB_PATH, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    # Создаем экземпляры бота и диспетчера с Redis
    bot = Bot(token=TOKEN)
    storage = RedisStorage.from_url(REDIS_URL)
    dp = Dispatcher(storage=storage)

    # Настраиваем middleware и обработчики
    dp.message.middleware(LoggingMiddleware())
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    setup_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
