#!flask/bin/python
from flask import *
from flask_restful import *
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap

import diet_optimizer.settings
from models import *

app = Flask(__name__)
Bootstrap(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = settings.APP_KEY

import diet_optimizer.views