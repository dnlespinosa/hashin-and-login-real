from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.model):
    __tablename__ = 'users'

    username = db.Column(db.Text, nullable=False, unique=True, max_length=20)
    password = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True, max_length=50)
    first_name = db.Column(db.Text, nullable=False, max_length=30)
    last_name = db.Column(db.Text, nullable=False, max_length=30)


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, max_length=100)
    content = db.Column(db.text, nullable=False)
    username = db.ForeignKey(User, username)
    
