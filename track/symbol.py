from datetime import datetime
import os
import sys
import logging
import time

import requests

from influxdb_client import InfluxDBClient, WriteOptions
from alpha_vantage.timeseries import TimeSeries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SymbolUtil:
    ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    INFLUXDB_ADMIN_TOKEN = os.environ.get("INFLUXDB_ADMIN_TOKEN")
    INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")
    INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET")

    def __init__(
        self,
        host="http://localhost",
        port=9999,
        token=INFLUXDB_ADMIN_TOKEN,
        org=INFLUXDB_ORG,
        bucket=INFLUXDB_BUCKET,
        debug=False,
    ):
        self.host = host
        self.port = port
        self.token = token
        self.org = org
        self.debug = debug
        self.bucket = bucket
        self._client = None

    def __enter__(self):
        self._client = InfluxDBClient(
            url=f"{self.host}:{self.port}",
            token=self.token,
            org=self.org,
            debug=self.debug,
        )
        self.write_api = self._client.write_api(
            write_options=WriteOptions(
                batch_size=500,
                flush_interval=10_000,
                jitter_interval=2_000,
                retry_interval=5_000,
            )
        )
        self.query_api = self._client.query_api()

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._client.__del__()

    @classmethod
    def parse_daily_trades(cls, data, symbol):
        trade_data = []
        for k, v in data.items():
            timestamp = int(datetime.strptime(k, "%Y-%m-%d").timestamp()) * (
                10 ** 9
            )  # in nanosecond
            try:
                fields = {
                    "open": float(v.get("1. open")),
                    "high": float(v.get("2. high")),
                    "low": float(v.get("3. low")),
                    "close": float(v.get("4. close")),
                    "volume": float(v.get("5. volume")),
                }

            except ValueError:
                print(f"maybe values in fields are not float {v}")
                continue

            item = {
                "measurement": "trade",
                "time": timestamp,
                "fields": fields,
                "tags": {"symbol": symbol},
            }
            trade_data.append(item)

        return trade_data

    @classmethod
    def get_daily_trade_data(cls, symbol, outputsize="compact"):
        if not symbol:
            logging.info(f"please provider a symbol")
            return

        ts = TimeSeries(key=cls.ALPHAVANTAGE_API_KEY)
        # Get json object with the daily data and another with the call's metadata
        logger.info(f"Getting data for {symbol}")
        try:
            data, meta_data = ts.get_daily(symbol, outputsize=outputsize)
        except ValueError:
            # no data found for symbol
            return

        symbol = meta_data.get("2. Symbol")
        if not symbol:
            logging.error(f'Error when trying to get "2. Symbol" from meta_data')
            return

        if not data:
            logger.info(f"no data found for symbol {symbol}")
            return

        trade_data = cls.parse_daily_trades(data, symbol)
        logger.info(f"got {len(trade_data)} records")

        return trade_data

    @classmethod
    def search_in_alphavantage(cls, keyword):
        alpha_search_url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={cls.ALPHAVANTAGE_API_KEY}"

        try:
            r = requests.get(alpha_search_url)
            if r.status_code == 200:
                return r.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Alphavantage api error: {e}")

    def write_data(self, points):
        self.write_api.write(bucket=self.bucket, org=self.org, record=points)


def get_all_symbols(debug=False):
    with SymbolUtil(debug=debug) as symbol_manager:
        query = (
            f'from(bucket:"{symbol_manager.bucket}")'
            " |> range(start: -20d)"
            ' |> filter(fn: (r) => r._measurement == "trade") '
            ' |> filter(fn: (r) => r._field == "close") '
            ' |> distinct(column:"symbol")'
        )
        records = symbol_manager.query_api.query_stream(
            org=symbol_manager.org, query=query
        )  # this returns a generator
        symbols = [record.values["symbol"] for record in records]

    return symbols


def write_trade_data_in_db(symbol, full=False, debug=False):
    if not symbol:
        logging.info(f"please provider a symbol")
        return

    json_body = SymbolUtil.get_daily_trade_data(
        symbol, outputsize="full" if full else "compact"
    )
    if not json_body:
        logger.info(f"no data to write into db")
        return

    logger.info(f"write trade data for symbol {symbol}")
    with SymbolUtil(debug=debug) as symbol_manager:
        try:
            while len(json_body) > 0:
                points = json_body[-500:]
                print(f"write up to 500 data points")
                symbol_manager.write_data(points)

                json_body = json_body[:-500]
                time.sleep(1)

        except Exception as err:
            logger.error(f"error {err}")


if __name__ == "__main__":
    ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    INFLUXDB_ADMIN_TOKEN = os.environ.get("INFLUXDB_ADMIN_TOKEN")
    INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")
    INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET")
    DEBUG = os.environ.get("DEBUG", False)

    if (
        ALPHAVANTAGE_API_KEY
        and INFLUXDB_ADMIN_TOKEN
        and INFLUXDB_ORG
        and INFLUXDB_BUCKET
    ):
        if len(sys.argv) < 2:
            print(
                "please provide a symbol, e.g. GOOGL, or use a command, e.g. update_all=1"
            )
        else:
            full, update_all = False, False
            for i in sys.argv[1:]:
                try:
                    key, v = i.split("=")
                    if v != "1":
                        print(f'command "{key}" has no effect')
                        continue
                    if key == "debug":
                        DEBUG = True
                        print(f"debug mode on")
                    if key == "full":
                        full = True
                        print(f"loading full trade data")
                    if key == "update_all":
                        update_all = True
                        print(f"update trade data for all symbols")
                except ValueError:
                    symbol = i
                    print(f"got symbol {symbol}")

            if update_all:
                # TODO use task
                for symbol in get_all_symbols(debug=DEBUG):
                    print(f"writing trade data in db for {symbol}")
                    write_trade_data_in_db(symbol, full=full, debug=DEBUG)
                    time.sleep(1)
            else:
                print(f"writing trade data in db for {symbol}")
                write_trade_data_in_db(symbol, full=full, debug=DEBUG)

            print(f"done")
    else:
        print(
            f"Set ALPHAVANTAGE_API_KEY, INFLUXDB_ADMIN_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET as an environment variable first"
        )
        print(f"abort")
