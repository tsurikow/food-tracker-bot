# Запуск бота

Пререквизиты: Python 3.11, Docker Compose и uv, ключ API YandexGPT и токен Телеграм-бота

Установка зависимостей локально

```
uv sync
```

Для запуска проекта необходимо заполнить файл `.env.dist` и переименовать его в `.env`

После этого запускаем сборку

```
docker-compose up --build
```

Основные зависимости

```
dependencies = [
    "aiogram~=3.17.0",
    "aiohttp~=3.11.11",
    "python-dotenv~=1.0.1",
    "pydantic>=2.10.4",
    "redis~=5.2.1",
    "alembic~=1.14.0",
    "asyncpg~=0.30.0",
    "sqlalchemy~=2.0.36",
    "yandex_cloud_ml_sdk==0.2.4"
]
```

## Logging

Логи бота пишутся в logs.log в корневом каталоге

![logs1.png](assets/logs1.png)

## /set_profile

![profile1.png](assets/profile1.png)

![profile2.png](assets/profile2.png?t=1737578606324)

## /help

![help.png](assets/help.png)

## /log_water

![water1.png](assets/water1.png)

## /log_food

![food1.png](assets/food1.png)

![food2.png](assets/food2.png)

## /log_workout

![workout1.png](assets/workout1.png)

![workout2.png](assets/workout2.png)

## /check_progress

![progress.png](assets/progress.png)

## /recommend

![recommend1.png](assets/recommend1.png)

![recommend2.png](assets/recommend2.png)

## Postgres

![db.png](assets/db.png)
