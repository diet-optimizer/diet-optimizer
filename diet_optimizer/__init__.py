#!flask/bin/python
from flask import *
from flask_restful import *
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap

import diet_optimizer.settings
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dietoptimizer@104.131.95.4:3306/dietoptimizer'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bae74984c70df0:6280cc0c@us-cdbr-iron-east-04.cleardb.net/heroku_194b00fe5baed38'
app.secret_key = settings.APP_KEY
db.init_app(app)

Bootstrap(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

import diet_optimizer.views
