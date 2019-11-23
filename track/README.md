## Setup
* setup environment
    * `$ python3 -m venv venv`
    * `$ source venv/bin/activate`
    * `$ pip install -r requirments.txt`
    * `$ brew install influxdb`

* run services
    * `$ docker run -d -p 3000:3000 grafana/grafana`
    * InfluxDB
       * run influxdb in a separate terminal 
         `$ influxd -config /usr/local/etc/influxdb.conf` 
         see: [docs.influxdata.com](https://docs.influxdata.com/influxdb/v1.7/introduction/installation/)

* set up grafana with influxdb
    * some common steps
    * use "http://127.0.0.1:8086/" (instead of localhost:8086) when setting up influxdb as a datasource in grafana.  
 
### WIP
- Example data from [Alphavantage API](https://www.alphavantage.co/documentation/)
- run `$ python demo_stock.py`. This will parse data from Alphavatage and put it in Influxdb.
- open grafana and create a dashboard, e.g. 
    - FROM default "GOOGL"
    - SELECT field(open)
    - FORMAT AS Time series
    - ALIAS BY open
 
