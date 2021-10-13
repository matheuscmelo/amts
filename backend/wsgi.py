from app import app
from db import db
import config
from os import environ


SECRET_KEY = environ.get('SECRET_KEY')
db.init_app(app)
db.app = app
uri = f'mysql+pymysql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@mariadb:3306/db'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
config.set_mariadb_password()
uri = f'mysql+pymysql://{config.DATABASE_USER}:{config.read_database_password()}@mariadb:3306/db'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db.create_all()
app.config['JWT_SECRET_KEY'] = SECRET_KEY
config.run_populate_db()
