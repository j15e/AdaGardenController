from Adafruit_IO import Client, Data
from datetime import date
from datetime import timedelta
from csv import DictReader
import csv
import os
import urllib.request

ADAFRUIT_USERNAME = os.environ['AIO_USERNAME']
ADAFRUIT_KEY = os.environ['AIO_KEY']
ADAFRUIT_PUMP_FEED = os.environ['AIO_PUMP_FEED']
PRECIPITATION_DAYS = int(os.environ['PRECIPITATION_DAYS'])
PRECIPITATION_SKIP = int(os.environ['PRECIPITATION_SKIP'])
CLIMATE_STATION_ID = os.environ["CLIMATE_STATION_ID"]
CLIMATE_CSV_URL = ("http://climate.weather.gc.ca/climate_data/bulk_data_e.html"
                   "?format=csv&stationID={}&Year={}&timeframe=2"
                   .format(CLIMATE_STATION_ID, date.today().year))


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


def aio_start_watering():
    aio = Client(ADAFRUIT_USERNAME, ADAFRUIT_KEY)
    aio.create_data(ADAFRUIT_PUMP_FEED, Data(value=1))


total_precipitation = 0.0
check_dates = last_few_days(days=PRECIPITATION_DAYS)
csv = climate_csv()
for row in csv:
    date = row["Date/Time"]
    if date not in check_dates:
        continue

    precipitation = row["Total Precip (mm)"]
    if not precipitation:
        continue

    total_precipitation += float(precipitation)

summary = "Total precipitation in past {0:d} days : {1:.2f}mm"
print(summary.format(len(check_dates), total_precipitation))


if total_precipitation > PRECIPITATION_SKIP:
    print("Skip watering for today (more than {}mm).".format(PRECIPITATION_SKIP))
else:
    print("Trigger watering today (less than {}mm).".format(PRECIPITATION_SKIP))
    aio_start_watering()
