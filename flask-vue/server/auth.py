import functools
import logging

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# route `/auth/register` with `register` view
@bp.route('/register', methods=('GET', 'POST'))
def register():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        logging.debug(post_data)
        print(post_data)
        username = post_data['username']
        password = post_data['password']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username,
                                                                               generate_password_hash(password)))
            db.commit()

        else:
            response_object['status'] = 'failed'
            response_object['message'] = 'Register failed.'
            flash(error)

    return jsonify(response_object)


@bp.route('/vue_login', methods=('GET', 'POST'))
def vue_login():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data['username']
        password = post_data['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            response_object['message'] = 'Login success!'
        else:
            response_object['status'] = 'failed'
            response_object['message'] = 'Register failed.'
            flash(error)

    return jsonify(response_object)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
