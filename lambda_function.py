from Adafruit_IO import Client, Data
from datetime import date
from datetime import datetime
from datetime import timedelta
from csv import DictReader
from astral import Astral
from pytz import timezone
import pytz
import csv
import os
import urllib.request

ADAFRUIT_USERNAME = os.environ['AIO_USERNAME']
ADAFRUIT_KEY = os.environ['AIO_KEY']
ADAFRUIT_PUMP_FEED = os.environ['AIO_PUMP_FEED']
PRECIPITATION_DAYS = int(os.environ['PRECIPITATION_DAYS'])
PRECIPITATION_SKIP = int(os.environ['PRECIPITATION_SKIP'])
WATERING_DURATION_FEED = os.environ['WATERING_DURATION_FEED']
CLIMATE_CITY = os.environ['CLIMATE_CITY']
CLIMATE_STATION_ID = os.environ["CLIMATE_STATION_ID"]
CLIMATE_CSV_URL = ("http://climate.weather.gc.ca/climate_data/bulk_data_e.html"
                   "?format=csv&stationID={}&Year={}&timeframe=2"
                   .format(CLIMATE_STATION_ID, date.today().year))


def handler(event, context):
    aio = Client(ADAFRUIT_USERNAME, ADAFRUIT_KEY)
    check_dates = last_few_days(days=PRECIPITATION_DAYS)
    precipitation = total_precipitation(check_dates)
    duration = aio_watering_duration(aio)
    summary = "Total precipitation in past {0:d} days : {1:.2f}mm"
    print(summary.format(len(check_dates), precipitation))

    if precipitation > PRECIPITATION_SKIP:
        print("Skip watering {}min for today (more than {}mm).".format(duration, PRECIPITATION_SKIP))
    else:
        print("Will be watering {}min today (less than {}mm).".format(duration, PRECIPITATION_SKIP))

        if is_watering_period(duration):
            print("Watering NOW!")
            aio_set_pump(aio, 1)
        else:
            print("Not watering right now, outside target period.")
            aio_set_pump(aio, 0)


def total_precipitation(dates):
    total_precipitation = 0.0
    csv = climate_csv()
    for row in csv:
        row_date = row["Date/Time"]
        if row_date not in dates:
            continue

        precipitation = row["Total Precip (mm)"]
        if not precipitation:
            continue

        total_precipitation += float(precipitation)

    return total_precipitation


def is_watering_period(duration):
    a = Astral()
    a.solar_depression = 'civil'
    city = a[CLIMATE_CITY]
    sun = city.sun(date=date.today(), local=True)
    current_time = datetime.now(tz=timezone(city.timezone))
    watering_duration = timedelta(minutes=duration)
    # Start watering n minutes before dawn
    period_start = sun['dawn'] - watering_duration
    # Stop at dawn
    period_end = sun['dawn']
    print("Watering target period is from {:%H:%M} to {:%H:%M}".format(period_start, period_end))

    return current_time > period_start and current_time < period_end


def climate_csv():
    response = urllib.request.urlopen(CLIMATE_CSV_URL)
    data = response.read().decode('utf-8')
    fieldnames = ["Date/Time", "Year", "Month", "Day", "Data Quality", "Max Temp (°C)",
                  "Max Temp Flag", "Min Temp (°C)", "Min Temp Flag", "Mean Temp (°C)",
                  "Mean Temp Flag", "Heat Deg Days (°C)", "Heat Deg Days Flag",
                  "Cool Deg Days (°C)", "Cool Deg Days Flag", "Total Rain (mm)",
                  "Total Rain Flag", "Total Snow (cm)", "Total Snow Flag",
                  "Total Precip (mm)", "Total Precip Flag", "Snow on Grnd (cm)",
                  "Snow on Grnd Flag", "Dir of Max Gust (10s deg)", "Dir of Max Gust Flag",
                  "Spd of Max Gust (km/h)", "Spd of Max Gust Flag"]
    csv.register_dialect('weather-gc', delimiter=',', quoting=csv.QUOTE_ALL)

    return DictReader(data.splitlines(), dialect="weather-gc", fieldnames=fieldnames)


def last_few_days(days=None):
    one_day = timedelta(days=1)
    last_n_days = []
    while len(last_n_days) < days:
        previous_day = (date.today() - one_day - len(last_n_days) * one_day)
        last_n_days.append(previous_day.strftime("%Y-%m-%d"))

    return last_n_days


def aio_watering_duration(aio):
    data = aio.receive(WATERING_DURATION_FEED)
    return int(data.value)


def aio_set_pump(aio, state):
    aio.create_data(ADAFRUIT_PUMP_FEED, Data(value=state))
