from __future__ import annotations
from yandex_cloud_ml_sdk import AsyncYCloudML
from config.config import GPT_AUTH, GPT_FOLDER

async def get_gpt_food(name: str) -> int:
    food_msg = [
        {
            "role": "system",
            "text": """Я буду писать названия продуктов, 
            мне нужен ответ в формате целого числа без иных символов, 
            ответ содержит калорийность продукта на 100 грамм,
            если калорийность продукта не удается найти по любым причинам,
            то считаем в ответе, что она равна 0""",
        },
        {
            "role": "user",
            "text": name,
        },
    ]
    calorie = await get_gpt_result(food_msg)
    return int(calorie)

async def get_gpt_temp(name: str) -> int:
    temp_msg = [
        {
            "role": "system",
            "text": """Я буду писать названия города, 
            мне нужен ответ в формате целого числа без иных символов, 
            ответ содержит текущую температуру по прогнозу погоды в градусах цельсия,
            если прогноз погоды не доступен по любым причинам, то считаем, что температура в ответе равна 0""",
        },
        {
            "role": "user",
            "text": name,
        },
    ]
    temp = await get_gpt_result(temp_msg)
    return int(temp)

async def get_gpt_train(name: str) -> int:
    train_msg = [
        {
            "role": "system",
            "text": """Я буду писать вид тренировки, 
            мне нужен ответ в формате целого числа без иных символов, 
            ответ содержит количество килокалорий, которое сжигает указанная тренировка за одну минуту,
            если не удается найти информацию о сжигании калорий, то считаем, что в ответе она равна 0""",
        },
        {
            "role": "user",
            "text": name,
        },
    ]
    burn = await get_gpt_result(train_msg)
    return int(burn)

async def get_gpt_advice(calories: int) -> str:
    train_msg = [
        {
            "role": "system",
            "text": """Я буду писать количество килокалорий, которые мне необходимо потребить сегодня, 
            мне нужно составить сбалансированный рацион питания, который примерно равен к-ву указанных калорий, 
            ответ содержит только список продуктов питания или блюд, калорийность, а так же краткий совет 
            сколько минут в день уделить тренировкам. Ответ должен быть не длиннее 120 слов.""",
        },
        {
            "role": "user",
            "text": f"{calories}",
        },
    ]
    advice = await get_gpt_result(train_msg)
    return advice


async def get_gpt_result(msg: list) -> str:
    sdk = AsyncYCloudML(folder_id=GPT_FOLDER, auth=GPT_AUTH)

    model = sdk.models.completions("yandexgpt")
    model = model.configure(temperature=0.3)
    result = await model.run(msg)

    return result[0].text