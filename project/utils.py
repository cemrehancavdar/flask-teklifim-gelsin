from datetime import date, timedelta
from random import uniform

today = date.today() + timedelta(days=3)


def calculate_expiry_date(days):
    return date.today() + timedelta(days=days)



def calculate_random_float():
    return round(uniform(1,4), 2)