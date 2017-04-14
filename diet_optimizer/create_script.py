import MySQLdb
from models import USDAfoods,db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/foods'
db = SQLAlchemy(app)

"""
db_ex = MySQLdb_ex.connect(host="localhost",	# your host, usually localhost
					user="root",		# your username
					passwd="password",			# your password
					db_ex="foods")			# name of the data base
"""

rows = db.engine.execute("SELECT `abbrev`.`NDB_No` AS `NDB_No`, `food_des`.`Long_Desc` AS `Desc`, `abbrev`.`Energ_Kcal` AS `Cal`, `abbrev`.`Protein_(g)` AS `Prot`, `abbrev`.`Lipid_Tot_(g)` AS `Fat`, `abbrev`.`Carbohydrt_(g)` AS `Carb`, `food_des`.`FdGrp_Cd` AS `Group_Code`, `fd_group`.`FdGrp_Desc` AS `Group_Name` FROM ((`abbrev` JOIN `food_des`) JOIN `fd_group`) WHERE ((`abbrev`.`NDB_No` = `food_des`.`NDB_No`) AND (`food_des`.`FdGrp_Cd` = `fd_group`.`FdGrp_CD`));")
#id,description,calories,protien,fat,carbs,group code, group name
for row in rows:
	instance = USDAfoods(*row)
	db.session.add(instance)
	db.session.commit()

db.close()