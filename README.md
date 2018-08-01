# AdaGardenController

This pythons script controller when to water a garden. 

It uses historical precipitation data from [Weather Canada](http://climate.weather.gc.ca/) 
and sun position from the [astral](https://github.com/sffjunkie/astral/) library.

The script emits an on/off state to Adafruit IO feed, and the pump act accordingly.

See [AdaGarden](https://github.com/j15e/AdaGarden) for the Arduino system controlling 
the pump switch.

## Quick start

Requires python 3.6+ and virtualenv.

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python main.py

The `main.py` is there only to test the lambda function handler locally.

## Deploy script updates

    make package && make deploy

## Terraform setup

Setup the AWS Lambda & other requirements (scheduler, role, etc) with terraform.

    cd terraform
    export AWS_ACCESS_KEY_ID="anaccesskey"
    export AWS_SECRET_ACCESS_KEY="asecretkey"
    export AWS_DEFAULT_REGION="us-east-1"
    terraform init
    terraform plan
    terraform apply

## Environment variables (AWS Lambda)

Put configurations specifics to the python controller in `terraform/terraform.tfvars`.

```
# Adafruit.io account keys
AIO_USERNAME=
AIO_KEY=

# Adafruit feed to trigger watering
AIO_PUMP_FEED=garden-pump-staging

# Number of past days to check precipitations
PRECIPITATION_DAYS=2

# Total precipitation to skip watering
PRECIPITATION_SKIP=20

# Duration of watering in minutes
WATERING_DURATION=30

# Weater.gc.ca climate station ID to check
CLIMATE_STATION_ID=27803

# City name to check dawn time
CLIMATE_CITY=Quebec
```
