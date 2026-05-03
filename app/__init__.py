from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'   # обязательно для @login_required

from . import models, views

with app.app_context():
    db.create_all()