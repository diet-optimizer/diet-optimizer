#!flask/bin/python
from flask import *
from flask_restful import *
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap

import diet_optimizer.settings
from models import *

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://us-cdbr-iron-east-04.cleardb.net/heroku_194b00fe5baed38'
app.config['MYSQL_USER'] = 'bae74984c70df0'
app.config['MYSQL_PASSWORD'] = '6280cc0c'
app.config['MYSQL_DB'] = 'heroku_194b00fe5baed38'
app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-04.cleardb.net'
db.init_app(app)

Bootstrap(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = settings.APP_KEY

import diet_optimizer.views