import time
from notifiers import *
import requests
from datetime import datetime
import os


token = os.environ.get("TOKEN")
my_id = os.environ.get("MY_ID")
MY_LAT = 13.496170
MY_LONG = 120.952920


def iss():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # iss_latitude = float(data["iss_position"]["latitude"])
    # iss_longitude = float(data["iss_position"]["longitude"])

    iss_latitude = 13.496170
    iss_longitude = 120.952920

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split("+")[0].split(":")[0])
    sunrise_hour_correct = sunrise_hour + 8
    if sunrise_hour_correct > 24:
        sunrise_hour_correct -= 24

    sunset_hour = int(data["results"]["sunset"].split("T")[1].split("+")[0].split(":")[0])
    sunset_hour_correct = sunset_hour + 8
    if sunset_hour_correct > 24:
        sunset_hour_correct -= 24

    # time_now = datetime.now().hour
    time_now = 19

    if time_now >= sunset_hour_correct or time_now <= sunrise_hour_correct:
        return True


while True:
    if iss() and is_night():
        telegram = get_notifier('telegram')
        telegram.notify(token=token, chat_id=my_id, message="Look at overhead! You can see ISS! 💫 ")
        time.sleep(60)


