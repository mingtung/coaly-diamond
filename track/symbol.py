import os
import json
import sys
import logging

import requests
from influxdb import InfluxDBClient
from alpha_vantage.timeseries import TimeSeries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SymbolUtil:
    ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")

    def __init__(self, host='127.0.0.1', port=8086, dbname="stock", user="root", password="root", timeout=60):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.timeout = timeout
        self.client = None

    def __enter__(self):
        self.client = InfluxDBClient(
            host=self.host, port=self.port, username=self.user, password=self.password, database=self.dbname, timeout=self.timeout
        )
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close()

    @classmethod
    def parse_trades(cls, data, symbol):
        trade_data = []
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

            item = {"measurement": 'trade', "time": k, "fields": fields, "tags": {'symbol': symbol}}
            trade_data.append(item)

        return trade_data

    @classmethod
    def get_trade_data(cls, symbol):
        ts = TimeSeries(key=cls.ALPHAVANTAGE_API_KEY)
        symbol = symbol if symbol else "GOOGL"
        # Get json object with the daily data and another with the call's metadata
        logger.info(f"Getting data for {symbol}")
        try:
            data, meta_data = ts.get_daily(symbol)
        except ValueError:
            # no data found for symbol
            return

        # print(json.dumps(data))
        symbol = meta_data.get("2. Symbol")
        if not symbol:
            logging.error(f'Error when trying to get "2. Symbol" from meta_data')
            return

        trade_data = cls.parse_trades(data, symbol)
        logger.info(f'got {len(trade_data)} records')

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


def get_all_symbols():
    with SymbolUtil() as symbol_manager:
        query = 'SELECT count("open") from "trade" group by "symbol"'  # the selected count on `open` does not matter
        result = symbol_manager.client.query(query)
        symbols = [i[1]['symbol'] for i in result.keys()]

    return symbols


def write_trade_data_in_db(symbol):
    json_body = SymbolUtil.get_trade_data(symbol)
    if json_body:
        with SymbolUtil() as symbol_manager:
            symbol_manager.client.write_points(json_body)
    else:
        logger.info(f'no data to write into db')


if __name__ == "__main__":
    ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    if ALPHAVANTAGE_API_KEY:
        symbol = sys.argv[1] if len(sys.argv) == 2 else None
        write_trade_data_in_db(symbol)

    else:
        print(f"Set ALPHAVANTAGE_API_KEY as an environment variable first")
        print(f"abort")
