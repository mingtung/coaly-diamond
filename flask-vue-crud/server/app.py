from flask import Flask, jsonify
from flask_cors import CORS

DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)
"""
It's worth noting that the above setup allows cross-origin requests on all routes, from any domain, protocol, or port. In a production environment, you should only allow cross-origin requests from the domain where the front-end application is hosted. Refer to the Flask-CORS documentation for more info on this.
"""


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()
