from finbear import app, db, login_manager
from peewee import Model, CharField, DateTimeField, IntegerField, ForeignKeyField
import datetime
from flask_login import UserMixin

# from sqlalchemy.orm import Mapped, mapped_column
# from sqlalchemy import ForeignKey


@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(id = int(user_id))

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel, UserMixin):
    username = CharField(max_length=20, unique=True)
    email = CharField(max_length=50, unique=True)
    password = CharField()

class QuizScore(BaseModel):
    score = IntegerField()
    user = ForeignKeyField(User, backref='quiz_scores')
    date = DateTimeField(default=datetime.datetime.now)

db.connect()
db.create_tables([User, QuizScore])


