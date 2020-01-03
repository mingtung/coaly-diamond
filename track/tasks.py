import logging
import time

from celery import Celery

from symbol import get_all_symbols, write_trade_data_in_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Celery()
app.config_from_object('celeryconfig')


@app.task()
def fetch_daily_data():
    logger.info(f'Fetching daily data for all symbols')
    for symbol in get_all_symbols():
        logging.info(f"writing trade data in db for {symbol}")
        write_trade_data_in_db(symbol)
        time.sleep(1)

