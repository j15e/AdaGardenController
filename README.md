## Quick start

Requires python 3.6+ and virtualenv.

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Deploy infrastructure setup

    cd terraform
    export AWS_ACCESS_KEY_ID="anaccesskey"
    export AWS_SECRET_ACCESS_KEY="asecretkey"
    export AWS_DEFAULT_REGION="us-east-1"
    terraform init
    terraform plan
    terraform apply

## Deploy script updates

    make package && make deploy

## Required environment variables

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
