from aiogram.fsm.state import State, StatesGroup


class Profile(StatesGroup):
    name = State()
    age = State()
    weight = State()
    height = State()
    activity = State()
    city = State()
    water_goal = State()
    calorie_goal = State()
    logged_water = State()
    logged_calories = State()
    burned_calories = State()

class Food(StatesGroup):
    name = State()
    weight = State()

class Water(StatesGroup):
    volume = State()

class Burn(StatesGroup):
    name = State()
    time = State()