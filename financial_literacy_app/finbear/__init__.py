from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from peewee import SqliteDatabase

db = SqliteDatabase('my_database.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KOWALA'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from finbear import routes