import os
import json
from influxdb import InfluxDBClient
from alpha_vantage.timeseries import TimeSeries


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


def load_stock_data_from_file(data):
    if not data:
        data = "GOOGL.json"
    try:
        measurement = data[:-5]  # strip `.json` from the file name. Use the file name as measurement
    except TypeError:
        print(f"input data is not a json file")
        return

    with open(data) as f:
        try:
            data = json.load(f)
            json_body = parse_stock(data, measurement=measurement)
        except:
            print(f'Cannot parse the input data')
            return

    print(json_body)
    return json_body


def demo_local(client):
    json_body = load_stock_data_from_file('GOOGL.json')
    print(json_body)
    client.write_points(json_body)


def demo(client):
    ts = TimeSeries(key=ALPHAVANTAGE_API_KEY)
    # Get json object with the intraday data and another with the call's metadata
    data, meta_data = ts.get_intraday("GOOGL")

    # print(json.dumps(data))
    measurement = meta_data.get("2. Symbol")
    if not measurement:
        print(f'Error when trying to get "2. Symbol" from meta_data')
        return

    json_body = parse_stock(data, measurement)

    print(json_body)
    client.write_points(json_body)


if __name__ == "__main__":
    user = "root"
    password = "root"
    dbname = "example"
    client = InfluxDBClient(
        host="127.0.0.1", port=8086, username=user, password=password, database=dbname
    )
    client.create_database(dbname)  # Currently influxdb checks if the db exists. If it does, influxdb does nothing
    # and return

    ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    if ALPHAVANTAGE_API_KEY:
        #demo_local(client)
        demo(client)
    else:
        print(f"Set ALPHAVANTAGE_API_KEY as an environment variable first")
        print(f"abort")
