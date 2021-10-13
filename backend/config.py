from os import environ, path
from flask import jsonify, request
from exceptions import AppBaseException
from threading import Thread
from hashlib import sha256

REDIS_HOST = environ.get('REDIS_HOST', 'redis')
REDIS_PORT = environ.get('REDIS_PORT', '6379')
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI')
ADMIN_EMAIL = environ.get('ADMIN_EMAIL')
ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD')
DATABASE_USER = environ.get('DATABASE_USER')
DATABASE_PASSWORD = environ.get('DATABASE_PASSWORD')
ENVIRONMENT = environ.get('ENVIRONMENT')


def set_callbacks(app):

    @app.errorhandler(AppBaseException)
    def handle_error(e):
        return jsonify({"message": e.message}), e.status_code

    @app.before_request
    def verify_json():
        if (not request.method == 'GET' and not request.method == 'OPTIONS') and not request.is_json:
            return jsonify({"message" : "Request type is not JSON"}), 400


def run_populate_db():
    from services import user_service

    def populate_db():

        password = sha256((ADMIN_EMAIL+ADMIN_PASSWORD).encode()).hexdigest()
        u = user_service.create_user(ADMIN_EMAIL, password, 2, '', '', '', '' )
        user = u.approve()
        user.save()

    Thread(target=populate_db).run()


def set_mariadb_password():
    if path.exists('/encrypted-backend/password.txt'):
        return

    import random
    import string
    from db import db
    letters_and_digits = string.ascii_letters + string.digits
    password = ''.join((random.choice(letters_and_digits) for i in range(32)))
    sql = f"SET PASSWORD = PASSWORD('{password}')"
    db.engine.execute(sql)
    with open('/encrypted-backend/password.txt', 'w') as f:
        f.write(password)


def read_database_password():
    with open('/encrypted-backend/password.txt') as f:
        password = f.read()
    return password
