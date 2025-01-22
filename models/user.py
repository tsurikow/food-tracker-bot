from sqlalchemy import BigInteger, Column, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "user_data"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String, nullable=True)
    tg_id = Column(BigInteger, unique=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    activity = Column(Integer, nullable=False)
    water_goal = Column(Integer, nullable=True)
    calorie_goal = Column(Integer, nullable=True)
    logged_water = Column(Integer, nullable=True)
    logged_calories = Column(Integer, nullable=True)
    burned_calories = Column(Integer, nullable=True)
