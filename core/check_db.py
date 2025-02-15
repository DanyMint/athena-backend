import sys

import django.conf

from .logger import logger
from psycopg import connect
import time
from psycopg import OperationalError
from .settings import DATABASES


def check_db():
    max_retries = 5
    delay = 3

    for attempt in range(max_retries):
        try:
            with connect(
                    dbname=DATABASES['default']['NAME'],
                    user=DATABASES['default']['USER'],
                    password=DATABASES['default']['PASSWORD'],
                    host=DATABASES['default']['HOST'],
                    port=DATABASES['default']['PORT']
            ) as conn:
                logger.info("БД доступна. Продолжаем запуск")
                return 0
        except OperationalError:
            logger.warning(f"БД недоступна! Попытка подключения {attempt}/{max_retries}")
            time.sleep(delay)

    logger.error(f"Не удалось подключиться к БД. Проверьте запущена ли PostgreSQL")
    sys.exit(1)
