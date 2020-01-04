# WIP

## Setup
* prepare docker
* or setup environment
    * `$ python3 -m venv venv`
    * `$ source venv/bin/activate`
    * `$ pip install -r requirments.txt`

* an api key from [Alphavantage API](https://www.alphavantage.co/documentation/)
       
### environment variables
add these variables in a `.env` file or set them as environment variable

- for influxdb
```.env
INFLUXDB_BUCKET=your_influxdb_bucket
INFLUXDB_ORG=your_influxdb_org
INFLUXDB_ADMIN_TOKEN=your_influxdb_admin_token
```
- for Alphavantage
```.env
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
```
- for web and worker app

set to something like `host.docker.internal` if using Docker for Mac, otherwise, "http://localhost" should be enough
```.env
WEB_HOST=host.docker.internal  
CELERY_BROKER_URL=redis://host.docker.internal:6379
CELERY_RESULT_BACKEND=redis://host.docker.internal:6379
```

## Run services 
* option1: with docker `$ docker-compose up -d`
* option2:
    * Influxdb v2.0
        * start influxdb via docker `$ docker run --name influxdb -d -p 9999:9999 quay.io/influxdb/influxdb:2.0.0-alpha`
        * run on localhost:9999
    * run flask app
        * `$ python app.py`
    * fetch data periodically
        * schedule a periodic task to fetch daily data
            * `$ celery -A tasks.app beat --loglevel=info`
        * run the worker 
            * `$ celery -A tasks.app worker --loglevel=info` 
 
## Use 

* (add trading data by symbol via CLI tool)
    - `$ python symbol.py GOOGL`
    - This gets data from alphavantage, parses the data and stores it in Influxdb.
    - Fetch data for all added stock `$ python symbol.py update_all=1`
    
* add trading data by symbol via app
    - `http://localhost:5000/symbols`

* use Dashboards in influxdb
    - `http://localhost:9999/`

