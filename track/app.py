import json
import logging
import os

from flask import Flask, request, Response, render_template

from symbol import SymbolManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")

app = Flask(__name__)


@app.route("/symbols", methods=["GET", "POST"])
def list_symbols():
    search_symbol_name = request.form.get('search_symbol', '')
    confirmed_symbol_name = request.form.get('confirmed_symbol')

    search_result = None

    if request.method == "POST":
        if search_symbol_name:
            search_result = SymbolManager.search_in_alphavantage(search_symbol_name)['bestMatches']

        if confirmed_symbol_name:
            # add trade data for symbol in db
            SymbolManager.write_trade_data_in_db(confirmed_symbol_name)

    symbols = SymbolManager.get_all_symbols()
    SymbolManager.close_client()
    return render_template("symbol.html", symbols=symbols,  search_symbol=search_symbol_name, search_result=search_result)


@app.route("/search/<keyword>", methods=["GET"])
def search_symbol(keyword):
    return SymbolManager.search_in_alphavantage(keyword)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
