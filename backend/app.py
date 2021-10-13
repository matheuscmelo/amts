from sys import argv, exit
from os import environ

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import ssl
import config
from db import db
from resources import (UserCRUD, ForgetUser, UserRequest, UserRequestDetail, Login,
                      Auth, Image, User, ResetPassword, RequestResetPassword, AddInteraction,
                      Info)


is_prod = config.ENVIRONMENT == 'prod'

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
api.add_resource(UserCRUD, '/users')
api.add_resource(ForgetUser, '/users/<id>/forget')
api.add_resource(UserRequest, '/requests')
api.add_resource(UserRequestDetail, '/requests/<request_id>')
api.add_resource(Login, '/login')
api.add_resource(Auth, '/auth')
api.add_resource(User, '/user')
api.add_resource(Image, '/user/image')
api.add_resource(ResetPassword, '/reset_password')
api.add_resource(RequestResetPassword, '/request_reset_password')
api.add_resource(AddInteraction, '/interactions')
api.add_resource(Info, '/info')

jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'super-secret'

api = Api(app)
migrate = Migrate(app, db)
config.set_callbacks(app)


if __name__ == '__main__':
    if "test" in argv:
        import pytest
        db.init_app(app)
        db.app = app
        db.create_all()
        code = pytest.main(['tests'])
        exit(code)
    else:
        SECRET_KEY = environ.get('SECRET_KEY')
        db.init_app(app)
        db.app = app
        uri = f'mysql+pymysql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@mariadb:3306/db'
        app.config['SQLALCHEMY_DATABASE_URI'] = uri

        if is_prod:
            config.set_mariadb_password()
            uri = f'mysql+pymysql://{config.DATABASE_USER}:{config.read_database_password()}@mariadb:3306/db'
            app.config['SQLALCHEMY_DATABASE_URI'] = uri
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain('/cert.pem', '/key.pem')

        db.create_all()
        app.config['JWT_SECRET_KEY'] = SECRET_KEY
        config.run_populate_db()

        if is_prod:
            app.run(host="0.0.0.0")
        else:
            app.run(host="0.0.0.0")
