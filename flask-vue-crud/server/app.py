import uuid
import sqlite3
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort
from flask_cors import CORS

DEBUG = True
# configuration
DATABASE = 'flask-vue.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)
"""
It's worth noting that the above setup allows cross-origin requests on all routes, from any domain, protocol, or port. In a production environment, you should only allow cross-origin requests from the domain where the front-end application is hosted. Refer to the Flask-CORS documentation for more info on this.
"""

BOOKS = [{
    'id': uuid.uuid4().hex,
    'title': 'On the Road',
    'author': 'Jack Kerouac',
    'read': True
}, {
    'id': uuid.uuid4().hex,
    'title': 'Harry Potter and the Philosopher\'s Stone',
    'author': 'J. K. Rowling',
    'read': False
}, {
    'id': uuid.uuid4().hex,
    'title': 'Green Eggs and Ham',
    'author': 'Dr. Seuss',
    'read': False
}]


# connect to database
def connect_db():
    """Connects to the database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


# create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# open database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        """
        # TODO handle cases:
            1. book already exists
            2. error handling
            2.1 wrong type in request
            2.2 missing data in request
            3. an author with multiple books
        """
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS

    return jsonify(response_object)


def remove_book(book_id):
    the_book = [book for book in BOOKS if book['id'] == book_id]
    if the_book:
        BOOKS.remove(the_book[0])
        return True
    else:
        return False


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT' and request.get_json():
        post_data = request.get_json()
        is_removed = remove_book(book_id)
        if is_removed:
            BOOKS.append({
                'id': book_id,
                'title': post_data.get('title'),
                'author': post_data.get('author'),
                'read': post_data.get('read'),
            })
            response_object['message'] = 'Book updated!'
        else:
            response_object['message'] = 'No such book.'
            response_object['status'] = 'failed'
    elif request.method == 'DELETE':
        is_removed = remove_book(book_id)
        response_object['message'] = 'Book removed!'
    else:
        response_object['status'] = 'failed'

    return jsonify(response_object)


@app.route('/ping', methods=['GET'])
def ping_pong():
    return 'pong'


if __name__ == '__main__':
    init_db()
    app.run()
