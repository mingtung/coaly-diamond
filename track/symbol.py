import os
import json
import sys
import logging

import requests
from influxdb import InfluxDBClient
from alpha_vantage.timeseries import TimeSeries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SymbolManager:
    ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    user = "root"
    password = "root"
    dbname = "stock"
    client = InfluxDBClient(
        host="127.0.0.1", port=8086, username=user, password=password, database=dbname
    )
    client.create_database(
        dbname
    )  # Currently influxdb checks if the db exists. If it does, influxdb does nothing
    # and return

    @classmethod
    def _parse_trades(cls, data, symbol):
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
    def get_all_symbols(cls):
        query = 'SELECT count("open") from "trade" group by "symbol"'  # the selected count on `open` does not matter
        result = cls.client.query(query)
        symbols = [i[1]['symbol'] for i in result.keys()]

        return symbols

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

        trade_data = cls._parse_trades(data, symbol)
        logger.info(f'got {len(trade_data)} records')

        return trade_data

    @classmethod
    def write_trade_data_in_db(cls, symbol):
        json_body = cls.get_trade_data(symbol)
        if json_body:
            cls.client.write_points(json_body)
        else:
            logger.info(f'no data to write into db')

    @classmethod
    def close_client(cls):
        cls.client.close()

    @classmethod
    def search_in_alphavantage(cls, keyword):
        alpha_search_url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={cls.ALPHAVANTAGE_API_KEY}"

        try:
            r = requests.get(alpha_search_url)
            if r.status_code == 200:
                return r.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Alphavantage api error: {e}")


if __name__ == "__main__":
    ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    if ALPHAVANTAGE_API_KEY:
        symbol = sys.argv[1] if len(sys.argv) == 2 else None
        SymbolManager.write_trade_data_in_db(symbol)
        SymbolManager.close_client()

    else:
        print(f"Set ALPHAVANTAGE_API_KEY as an environment variable first")
        print(f"abort")
