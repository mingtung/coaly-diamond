import os
import json
import sys
import logging

from influxdb import InfluxDBClient
from alpha_vantage.timeseries import TimeSeries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_stock(data, measurement):
    json_body = []
    for k, v in data.items():
        try:
            fields = {
                "open": float(v.get("1. open")),
                "high": float(v.get("2. high")),
                "low": float(v.get("3. low")),
                "close": float(v.get("4. close")),
                "volume": float(v.get("5. volume")),
            }
        except ValueError:
            print(f"maybe values in fields are not float")
            continue

        item = {"measurement": measurement, "time": k, "fields": fields}
        json_body.append(item)

    return json_body


def get_symbol_data(client, symbol=None):
    ts = TimeSeries(key=ALPHAVANTAGE_API_KEY)
    symbol = symbol if symbol else "GOOGL"
    # Get json object with the daily data and another with the call's metadata
    logger.info(f"Getting data for {symbol}")
    data, meta_data = ts.get_daily(symbol)

    # print(json.dumps(data))
    measurement = meta_data.get("2. Symbol")
    if not measurement:
        logging.error(f'Error when trying to get "2. Symbol" from meta_data')
        return

    json_body = parse_stock(data, measurement)
    logger.info(json_body)
    client.write_points(json_body)


if __name__ == "__main__":
    user = "root"
    password = "root"
    dbname = "example"
    client = InfluxDBClient(
        host="127.0.0.1", port=8086, username=user, password=password, database=dbname
    )
    client.create_database(
        dbname
    )  # Currently influxdb checks if the db exists. If it does, influxdb does nothing
    # and return

    ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    if ALPHAVANTAGE_API_KEY:
        symbol = sys.argv[1] if len(sys.argv) == 2 else None
        get_symbol_data(client, symbol=symbol)

    else:
        print(f"Set ALPHAVANTAGE_API_KEY as an environment variable first")
        print(f"abort")
