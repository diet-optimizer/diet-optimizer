import MySQLdb
from models import USDAfoods,db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/foods'
db = SQLAlchemy(app)
db.create_all()
db.session.commit()

item = ('01001', 'Butter, salted',717L, 0.85, 81.11, 0.06, '0100', 'Dairy and Egg Products')

asdfghjkl = USDAfoods(*item)
db.session.add(asdfghjkl)
db.session.commit()