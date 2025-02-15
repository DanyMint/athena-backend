import sys
from os import environ, getenv
import logging
from loguru import logger
from .settings import BASE_DIR


def get_loguru_level(record):
    try:
        return logger.level(record.levelname).name
    except ValueError:
        return record.levelno


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Конвертируем `logging` record в `loguru` record
        level = get_loguru_level(record)
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


# Удаляем стандартные обработчики у `logging`
logging.root.handlers = []
logging.basicConfig(handlers=[InterceptHandler()], level=0)

logger.remove()  # Удаляем стандартный логер Loguru
logger.add(sys.stderr, level="WARNING", format="{time} {level} {message}")  # Вывод в консоль
logger.add(f"{BASE_DIR}/logs/app.log", level="DEBUG", rotation="50 kB", compression="zip")  # Файл с ротацией

# Перехватываем логи из Django, DRF и других библиотек
logging.getLogger("django").handlers = [InterceptHandler()]
logging.getLogger("uvicorn").handlers = [InterceptHandler()]
logging.getLogger("psycopg").handlers = [InterceptHandler()]
