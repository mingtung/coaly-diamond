import json
import logging
import os

from flask import Flask, request, Response, render_template, jsonify

from symbol import SymbolUtil, write_trade_data_in_db, get_all_symbols

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/symbols", methods=["GET", "POST"])
def list_symbols():
    search_symbol_name = request.form.get('search_symbol', '')
    confirmed_symbol_name = request.form.get('confirmed_symbol')

    search_result = None

    if request.method == "POST":
        if search_symbol_name:
            search_result = SymbolUtil.search_in_alphavantage(search_symbol_name)['bestMatches']

        if confirmed_symbol_name:
            # add trade data for symbol in db
            write_trade_data_in_db(confirmed_symbol_name)

    symbols = get_all_symbols()
    return render_template("symbol.html", symbols=symbols,  search_symbol=search_symbol_name, search_result=search_result)


@app.route("/search/<keyword>", methods=["GET"])
def search_symbol(keyword):
    return SymbolUtil.search_in_alphavantage(keyword)


@app.route('/get-trade-data/<symbol>', methods=['GET'])
def get_trade_data(symbol):
    return jsonify(SymbolUtil.get_daily_trade_data(symbol))


@app.route('/', methods=['GET'])
def home():
    return Response('http://localhost:5000/symbols')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
