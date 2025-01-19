import logging

from aiogram import BaseMiddleware
from aiogram.types import Message

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s, %(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    filename="logs.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        logger.info(f"Получено сообщение: {event.text}")
        return await handler(event, data)
