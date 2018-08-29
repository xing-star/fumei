from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS

db = SQLAlchemy()

config_name = config['default']

app = Flask(__name__)
app.config.from_object(config_name)
config_name.init_app(app)
db.init_app(app)

CORS(app)

from .users.urls import usersrouter
usersrouter()
from .transaction.urls import transactionrouter
transactionrouter()
from .market.urls import marketrouter
marketrouter()
