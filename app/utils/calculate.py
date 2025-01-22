def calculate_norm(age, weight, height, activity, temp=0):
    if temp > 25:
        t = 1
    else:
        t = 0
    water_norm = (weight * 30) + ((activity / 30) * 500) + (t * 500)
    calories_norm = (10 * weight) + (6.25 * height) - (5 * age)
    return water_norm, calories_norm
