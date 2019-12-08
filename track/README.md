## Setup
* setup environment
    * `$ python3 -m venv venv`
    * `$ source venv/bin/activate`
    * `$ pip install -r requirments.txt`
    * `$ brew install influxdb`
    * set up for grafana: create a persistent volume for your data in /var/lib/grafana (database and plugins)
       * `$ docker volume create grafana-storage` 
       
* run services
    * start grafana
        * `$ docker run -d -p 3000:3000 --name=grafana -v grafana-storage:/var/lib/grafana grafana/grafana`
        * later can just start it by `$ docker start grafana`
        
    * InfluxDB
       * run influxdb in a separate terminal 
         `$ influxd -config /usr/local/etc/influxdb.conf` 
         see: [docs.influxdata.com](https://docs.influxdata.com/influxdb/v1.7/introduction/installation/)
    
    * run flask app
        * `$ python app.py`

* set up grafana with influxdb
    * some common steps
    * use "http://127.0.0.1:8086/" (instead of localhost:8086) when setting up influxdb as a datasource in grafana.  
    * use "stock" as db

* api key from [Alphavantage API](https://www.alphavantage.co/documentation/)
 
### WIP
- add trading data by symbol via CLI tool
    - `$ python symbol.py GOOGL`
    - This gets data from alphavantage, parses the data and stores it in Influxdb.
   
- add trading data by symbol via app
    - (`$ python app.py`)
    - `http://localhost:5000/symbols`

~~- open grafana and create a dashboard, e.g. 
    - FROM default "GOOGL"
    - SELECT field(open)
    - FORMAT AS Time series
    - ALIAS BY open~~
 
