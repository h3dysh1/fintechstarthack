from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from peewee import SqliteDatabase

# Define your SQLite database connection here
db = SqliteDatabase('my_database.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KOWALA'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from finbear import routes