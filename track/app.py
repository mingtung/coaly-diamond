import logging
import os

import requests
from flask import Flask, jsonify, request, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create my app
app = Flask(__name__)
ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")


@app.route("/search/<keyword>", methods=["GET"])
def search_symbol(keyword):
    logging.info(f"searching for {keyword}")

    alpha_search_url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={ALPHAVANTAGE_API_KEY}"

    try:
        r = requests.get(alpha_search_url)
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Alphavantage api error: {e}")
        return Response("Alphavantage api error")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
