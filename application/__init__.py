from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

from application import routes