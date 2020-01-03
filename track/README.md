# WIP

## Setup
* prepare docker
* or setup environment
    * `$ python3 -m venv venv`
    * `$ source venv/bin/activate`
    * `$ pip install -r requirments.txt`

* an api key from [Alphavantage API](https://www.alphavantage.co/documentation/)
       
## Run services 
* with docker `$ docker-compose up -d`
* or individually
    * Influxdb v2.0
        * start influxdb via docker `$ docker run --name influxdb -d -p 9999:9999 quay.io/influxdb/influxdb:2.0.0-alpha`
        * run on localhost:9999
        
    * run flask app
        * `$ python app.py`
    * fetch data periodically
        - schedule a periodic task to fetch daily data
            - `$ celery -A tasks.app beat --loglevel=info`
        - run the worker 
            - `$ celery -A tasks.app worker --loglevel=info` 
 
## Use 

* (add trading data by symbol via CLI tool)
    - `$ python symbol.py GOOGL`
    - This gets data from alphavantage, parses the data and stores it in Influxdb.
    - Fetch data for all added stock `$ python symbol.py update_all=1`
    
* add trading data by symbol via app
    - `http://localhost:5000/symbols`

* use Dashboards in influxdb
    - `http://localhost:9999/`
