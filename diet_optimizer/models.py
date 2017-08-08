import unirest
import re
from pulp import *
import settings
import random
import datetime
#from flask import current_app
from smtplib import SMTP

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, foreign
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserDB(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    nickname = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(120), unique = True)
    pwdhash = db.Column(db.String(100))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    birthdate = db.Column(db.Date)
    activitylevel = db.Column(db.String(100))
    diet = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    #intolerences = db.Column(db.String(15))

    def __init__(self, firstname, lastname, nickname, email, password, height, weight, birthdate, activitylevel, diet, gender):
        self.firstname = firstname
        self.lastname = lastname
        self.nickname = nickname
        #self.gender = gender.lower()
        self.email = email
        self.set_password(password)
        self.height = height
        self.weight = weight
        self.birthdate = birthdate
        self.activitylevel = activitylevel
        self.diet = diet
        self.gender = gender
        #self.intolerences = intolerences.lower()

    def __repr__(self):
        return '<firstname : %s, lastname : %s, nickname : %s, gender : %s, email : %s, password : %s, height : %s, weight : %s, birthdate : %s, activity : %s, diet : %s>' %(self.firstname, self.lastname, self.nickname, self.gender, self.email, self.pwdhash, self.height, self.weight, self.birthdate, self.activitylevel, self.diet)

    def set_password(self, password):
         self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    # def generate_reset_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'reset': self.uid})

    # def reset_password(self, token, new_password):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return False
    #     if data.get('reset') != self.uid:
    #         return False
    #     self.password = new_password
    #     db.session.add(self)
    #     return True

class Recipe(db.Model):
    __tablename__ = 'recipes'
    rid = db.Column(db.Integer, primary_key = True)
    ridapi = db.Column(db.Integer)
    name = db.Column(db.String(100))
    link = db.Column(db.String(1000))

    def __init__(self,ridapi,name,link):
        self.ridapi = ridapi
        self.name = name
        self.link = link

class Feedback(db.Model):
    __tablename__ = 'feedback'
    rid = db.Column(db.ForeignKey('recipes.rid'))
    uid = db.Column(db.ForeignKey('users.uid'))
    mark = db.Column(db.Integer)

    recipe = relationship('Recipe')
    user = relationship('UserDB')

    __table_args__ = (
        db.PrimaryKeyConstraint('rid','uid'),
    )

# if a primary key is composed of two elements or more self become an object here : self.rif & self.uid

    def __init__(self,rid, uid, mark):
        self.rid = rid
        self.uid = uid
        self.mark = mark

class FeedbackRawFood(db.Model):
    __tablename__ = 'feedbackrawfood'
    fid = db.Column(db.ForeignKey('usda.NDB_No'))
    uid = db.Column(db.ForeignKey('users.uid'))
    mark = db.Column(db.Integer)

    rawfood = relationship('USDAfoods')
    user = relationship('UserDB')

    __table_args__ = (
        db.PrimaryKeyConstraint('fid','uid'),
    )

# if a primary key is composed of two elements or more self become an object here : self.rif & self.uid

    def __init__(self,fid, uid, mark):
        self.fid = fid
        self.uid = uid
        self.mark = mark

class Intolerences(db.Model):
    __tablename__ = 'intolerences'
    iid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.ForeignKey('users.uid'))
    intolerencename = db.Column(db.String(100))

    def __init__(self, uid, intolerencename):
        self.uid = uid
        self.intolerencename = intolerencename

#ryan added code
class USDAfoods(db.Model):
    __tablename__ = 'usda'
    NDB_No = db.Column(db.Integer, primary_key = True)
    Desc = db.Column(db.String(100))
    Cal = db.Column(db.Integer)
    Prot = db.Column(db.Integer)
    Fat = db.Column(db.Integer)
    Carb = db.Column(db.Integer)
    Group_Code = db.Column(db.Integer)
    Group_Name = db.Column(db.String(100))

    def __init__(self,food_id,food_description,Cal,Prot,Fat,Carb,food_group_id,group_description):
        self.Desc = food_description
        self.NDB_No = food_id
        self.Group_Name = group_description
        self.Group_Code = food_group_id
        self.Cal = Cal
        self.Prot = Prot
        self.Fat = Fat
        self.Carb = Carb
####

class User(object):

    def __init__(self, age, weight, height, gender, exercise_level):
        self.age = age
        self.gender = gender
        #self.weight = weight/2.20462 ##to convert to kg
        #self.height = height/0.393701 ##to convert to cm
        self.weight = weight
        self.height = height
        self.exercise_level = exercise_level
        self.daily_nutrients = self.get_daily_nutrients()

		##calculating user's age
	# def get_age(self):
	# 	if self.birthdate > datetime.date.today().replace(year = self.birthdate.year):
	# 		return datetime.date.today().year - self.birthdate.year - 1
	# 	else:
	# 		return datetime.date.today().year - self.birthdate.year

	##
    ##BMI
    def get_BMI(self):

        return round(self.weight/(self.height*self.height*0.0001),2)

    ##Physical Activity
    def get_PA(self):
        print self.age
        print self.weight
        print self.height
        if self.exercise_level == 'Sedentary':
            return 1.00
        if self.exercise_level == 'Low Active':
            if (self.gender == 'Male' and self.age < 19):
                return 1.13
            if (self.gender == 'Female' and self.age < 19):
                return 1.16
            if (self.gender == 'Male' and self.age >= 19):
                return 1.11
            if (self.gender == 'Female' and self.age >= 19):
                return 1.12
        if self.exercise_level == 'Active':
            if (self.gender == 'Male' and self.age < 19):
                return 1.26
            if (self.gender == 'Female' and self.age < 19):
                return 1.31
            if (self.gender == 'Male' and self.age >= 19):
                return 1.25
            if (self.gender == 'Female' and self.age >= 19):
                return 1.27
        if self.exercise_level == 'Very Active':
            if (self.gender == 'Male' and self.age < 19):
                return 1.42
            if (self.gender == 'Female' and self.age < 19):
                return 1.56
            if (self.gender == 'Male' and self.age >= 19):
                return 1.48
            if (self.gender == 'Female' and self.age >= 19):
                return 1.45

    ##Calories
    ##ages younger than 3 years and pregnancy situations are not considered.
    def get_calorie(self):
        ##height was divided by 100 because of cm m conversion.
        pa = self.get_PA()
        print pa
        if (self.gender == 'Male' and self.age < 9):
            eer = (88.5-(61.9*self.age)+pa*((26.7*self.weight)+(903*self.height/100)))+20
        if (self.gender == 'Male' and 9 <= self.age < 19):
            eer = (88.5-(61.9*self.age)+pa*((26.7*self.weight)+(903*self.height/100)))+25

        if (self.gender == 'Female' and self.age < 9):
            eer = (135.3-(30.8*self.age)+pa*((10*self.weight)+(934*self.height/100)))+20
        if (self.gender == 'Female' and 9 <= self.age < 19):
            eer = (135.3-(30.8*self.age)+pa*((10*self.weight)+(934*self.height/100)))+25

        if (self.gender == 'Male' and self.age >= 19):
            eer = (662-(9.53*self.age)+pa*((15.91*self.weight)+(539.6*self.height/100)))
        if (self.gender == 'Female' and self.age >= 19):
            eer = (354-(6.91*self.age)+pa*((9.36*self.weight)+(726*self.height/100)))

        return round(eer)

    ##Carbs
    def get_carb_lower(self, calories):
        x = 4 #energy provided by carbs/g
        return round(0.45*calories/x)

    def get_carb_upper(self, calories):
        x = 4 #energy provided by carbs/g
        return round(0.65*calories/x)

    ##Protein
    def get_protein_lower(self, calories):
        x = 4 #energy provided by protein/g
        if self.age < 4:
            return round(0.05*calories/x)
        if self.age < 19:
            return round(0.1*calories/x)
        return round(0.1*calories/x)

    def get_protein_upper(self, calories):
        x = 4 #energy provided by protein/g
        if self.age < 4:
            return round(0.2*calories/x)
        if self.age < 19:
            return round(0.3*calories/x)
        return round(0.35*calories/x)

    ##Fat
    def get_fat_lower(self, calories):
        x = 9 #energy provided by fat/g
        if self.age < 4:
            return round(0.3*calories/x)
        if self.age < 19:
            return round(0.25*calories/x)
        return round(0.2*calories/x)

    def get_fat_upper(self, calories):
        x = 9 #energy provided by fat/g
        if self.age < 4:
            return round(0.4*calories/x)
        if self.age < 19:
            return round(0.35*calories/x)
        return round(0.35*calories/x)

    def get_daily_nutrients(self):
        calories = self.get_calorie()
        bmi = self.get_BMI()
        carb_low = self.get_carb_lower(calories)
        carb_up = self.get_carb_upper(calories)
        prot_low = self.get_protein_lower(calories)
        prot_up = self.get_protein_upper(calories)
        fat_low = self.get_fat_lower(calories)
        fat_up = self.get_fat_upper(calories)
        return  {'bmi' : bmi, 'cal_low' : round(calories * 0.9, 1), 'cal_up' : round(calories * 1.1, 1), 'carb_low' : carb_low, 'carb_up' : carb_up, 'prot_low' : prot_low, 'prot_up' : prot_up, 'fat_low' : fat_low, 'fat_up' : fat_up}

    def set_daily_nutrients(self, cal_low, cal_up, carb_low, carb_up, prot_low, prot_up, fat_low, fat_up):
        if cal_low != '':
            self.daily_nutrients.cal_low = cal_low
        if cal_low != '':
            self.daily_nutrients.cal_up = cal_up
        if cal_low != '':
            self.daily_nutrients.carb_low = carb_low
        if cal_low != '':
            self.daily_nutrients.carb_up = carb_up
        if cal_low != '':
            self.daily_nutrients.prot_low = prot_low
        if cal_low != '':
            self.daily_nutrients.prot_up = prot_up
        if cal_low != '':
            self.daily_nutrients.fat_low = fat_low
        if cal_low != '':
            self.daily_nutrients.fat_up = fat_up


class RecipeHandler(object):

    def __init__(self, user_daily_nutrients, cuisine, diet, intolerances, exclude_ingredients, recipe_types):
        self.user_daily_nutrients = user_daily_nutrients
        self.recipe_types = recipe_types
        self.cuisine = cuisine
        self.diet = diet
        self.intolerances = intolerances
        self.exclude_ingredients = exclude_ingredients

    def get_URL(self, recipe_type, offset):

        add_recipe_info = "true"

        #One or more (comma separated) of the following: african, chinese, japanese, korean, vietnamese,
        #thai, indian, british, irish, french, italian, mexican, spanish, middle eastern, jewish, american,
        #cajun, southern, greek, german, nordic, eastern european, caribbean, or latin american.
        #Possible values are: pescetarian, lacto vegetarian, ovo vegetarian, vegan, paleo, primal, and vegetarian.

        # excludeIngredients = ""
        fill_ingredients = "false"
        include_ingredients = ""
        #Possible values are: dairy, egg, gluten, peanut, sesame, seafood, shellfish, soy, sulfite, tree nut, and wheat.
        limit_license = "false"
        number = "100"
        query = "recipe"
        ranking = "1"


        #One of the following: main course, side dish, dessert, appetizer, salad, bread, breakfast,
        #soup, beverage, sauce, or drink.
        # recipeType = ""

        req_URL = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/searchComplex?addRecipeInformation=" + add_recipe_info

        if self.cuisine != None:
            #print "cuisine is not null"
            cuisine_str = ",".join(self.cuisine)
            cuisine_str = cuisine_str.replace(" ", "+")
            cuisine_str = cuisine_str.replace(",", "%2C")
            req_URL += "&cuisine=" + cuisine_str

        # if len(self.cuisine) > 0 :
        #     cuisine_str = '%2C'.join(self.cuisine)
        #     cuisine_str = cuisine_str.replace(" ", "+")
        #     req_URL += "&cuisine=" + cuisine_str

        if self.diet != None:
            #print "diet is not null"
            diet_str = self.diet
            diet_str = diet_str.replace(" ", "+")
            req_URL += "&diet=" + diet_str

        # if self.exclude_ingredients != None:
        #     exclude_ingredients_str = self.exclude_ingredients
        #     exclude_ingredients_str = exclude_ingredients_str.replace(" ", "+")
        #     exclude_ingredients_str = exclude_ingredients_str.replace(",", "%2C")
        #     req_URL += "&excludeIngredients=" + exclude_ingredients_str

        req_URL += "&fillIngredients=" + fill_ingredients

        if self.intolerances != None:
            intolerances_str = ",".join(self.intolerances)
            intolerances_str = intolerances_str.replace(" ", "+")
            intolerances_str = intolerances_str.replace(",", "%2C")
            req_URL += "&intolerances=" + intolerances_str

        req_URL +=  "&limitLicense=" + limit_license + "&maxCalories="+ str(self.user_daily_nutrients['cal_up']) + "&maxCarbs=" + str(self.user_daily_nutrients['carb_up']) + "&maxFat=" + str(self.user_daily_nutrients['fat_up']) + "&maxProtein=" + str(self.user_daily_nutrients['prot_up']) + "&minCalories=" + str(0) + "&minCarbs=" + str(0) + "&minFat=" + str(0) + "&minProtein=" + str(0)

        req_URL += "&number=" + number + "&offset=" + str(offset) + "&query=" + query + "&ranking=" + ranking

        if recipe_type != None:
            recipe_type = str(recipe_type).replace(" ", "+")
            recipe_type = str(recipe_type).replace(",", "%2C")

            req_URL += "&type=" + recipe_type

        return req_URL

    def get_recipes(self):

        unique_IDs = []
        dict_keys = []
        dict_title = {}
        dict_cal = {}
        dict_prot = {}
        dict_carb = {}
        dict_fat = {}
        dict_price = {}
        dict_time = {}

        for recipe_type_index in range(len(self.recipe_types)):

            offset = random.randrange(0, 500)
            #offset was 0 - to regenarete random results
            print(offset)
            reached_length = False
            counter = 0
            while not reached_length and counter < 2:

                for i in range(1,2):
                    offset = i*offset #if range is bigger than one, you can get more results (one api call returns 100 recipes)
                    req_URL = self.get_URL(self.recipe_types[recipe_type_index], offset)
                    print(req_URL)

                    unirest.timeout(100) #100s timeout
                    print '************'
                    response = unirest.get(req_URL,
                      headers={
                        "X-Mashape-Key": settings.SPOONACULAR_KEY,
                        "Accept": "application/json"
                      }
                    )
                    print response.body
                    print settings.SPOONACULAR_KEY
                    json_data = response.body["results"]

                    print(len(json_data))
                    print(offset)
                    print(json_data)

                    if len(json_data) < 30:
                        offset = random.randrange(0, 500)
                        counter += 1

                    else:
                        reached_length = True
                        counter = 4

                    val_title = []
                    val_prot = []
                    val_carb = []
                    val_cal = []
                    val_fat = []
                    val_price = []
                    val_time = []

                    for d in json_data:
                        if d["id"] not in unique_IDs:
                            k = d['id']
                            unique_IDs.append(k)
                            dict_keys.append(k)
                            for key, value in d.iteritems():
                                    if key == "title":
                                        v = d[key].encode('ascii','ignore')
                                        val_title.append(v)
                                    if key == "calories":
                                        v = d[key]
                                        val_cal.append(v)
                                    if key == "protein":
                                        v = int(re.findall(r'\d+', d[key])[0])
                                        val_prot.append(v)
                                    if key == "carbs":
                                        v = int(re.findall(r'\d+', d[key])[0])
                                        val_carb.append(v)
                                    if key == "fat":
                                        v = int(re.findall(r'\d+', d[key])[0])
                                        val_fat.append(v)
                                    if key == "pricePerServing":
                                        v = round(float(d[key])/100,2)
                                        val_price.append(v)
                                    if key == "readyInMinutes":
                                        v = int(d[key])
                                        val_time.append(v)

            dict_cal_temp = dict(zip(dict_keys, val_cal))
            dict_prot_temp = dict(zip(dict_keys, val_prot))
            dict_carb_temp = dict(zip(dict_keys, val_carb))
            dict_fat_temp = dict(zip(dict_keys, val_fat))
            dict_title_temp = dict(zip(dict_keys, val_title))
            dict_price_temp = dict(zip(dict_keys, val_price))
            dict_time_temp = dict(zip(dict_keys, val_time))

            dict_cal[self.recipe_types[recipe_type_index].strip()] = dict_cal_temp
            dict_prot[self.recipe_types[recipe_type_index].strip()] = dict_prot_temp
            dict_carb[self.recipe_types[recipe_type_index].strip()] = dict_carb_temp
            dict_fat[self.recipe_types[recipe_type_index].strip()] = dict_fat_temp
            dict_title[self.recipe_types[recipe_type_index].strip()] = dict_title_temp
            dict_price[self.recipe_types[recipe_type_index].strip()] = dict_price_temp
            dict_time[self.recipe_types[recipe_type_index].strip()] = dict_time_temp

            dict_keys = []
            val_cal = []
            val_prot = []
            val_carb = []
            val_fat = []
            val_title = []
            val_price = []
            val_time = []

        return {"json" : response.body, "unique_IDs" : unique_IDs, "url" : req_URL, "dict_cal" : dict_cal, "dict_prot" : dict_prot, "dict_carb" : dict_carb, "dict_fat" : dict_fat, "dict_price" : dict_price, "dict_time" : dict_time, "dict_title" : dict_title, "recipe_types" : self.recipe_types}


class LinearProgrammingSolver(object):

    def __init__(self, obj, obj_nut, dict_prot, dict_fat, dict_cal, dict_carb, dict_title, dict_price, dict_time, recipe_types, daily_nutrients):
        self.obj = obj
        self.obj_nut = obj_nut
        self.dict_prot = dict_prot
        self.dict_fat = dict_fat
        self.dict_cal = dict_cal
        self.dict_carb = dict_carb
        self.dict_price = dict_price
        self.dict_time = dict_time
        self.dict_title = dict_title
        self.recipe_types = recipe_types
        self.daily_nutrients = daily_nutrients
        x_appetizer = 0
        x_breakfast = 0
        x_dessert = 0
        x_maincourse = 0
        x_sidedish = 0
        x_salad = 0
        x_bread = 0
        x_soup = 0
        x_beverage = 0
        x_sauce = 0
        x_drink = 0

    def func_lp(self):

        if self.obj == "Max":
            objective = pulp.LpMaximize
        if self.obj == "Min":
            objective = pulp.LpMinimize

        lp_model = pulp.LpProblem('The Diet Problem', objective)

        # objective function creation with for loop requires an additional variable to add to the model
        obj_lp = 0
        cal_lp = 0
        prot_lp = 0
        fat_lp = 0
        carb_lp = 0
        price_lp = 0
        time_lp = 0
        # title_lp = []

            # create the objective
        if self.obj_nut == "Protein":
            dict_nut = self.dict_prot
        if self.obj_nut == "Fat":
            dict_nut = self.dict_fat
        if self.obj_nut == "Carbs":
            dict_nut = self.dict_carb
        if self.obj_nut == "Calories":
            dict_nut = self.dict_cal
        if self.obj_nut == "Price":
            dict_nut = self.dict_price
        if self.obj_nut == "Time":
            dict_nut = self.dict_time


        for recipe_type_name in self.recipe_types:

            print(recipe_type_name)
            recipe_type_name = recipe_type_name.strip()

            # variables
            # variable = vars()['x_' + recipeTypeName]
            vars()['x_' + recipe_type_name] = pulp.LpVariable.dict('x_%s', dict_nut[recipe_type_name].keys(), cat='Binary')
            variable = vars()['x_' + recipe_type_name]

            # objective
            obj_lp += sum(dict_nut[recipe_type_name][key] * variable[key] for key in dict_nut[recipe_type_name].keys())
            lp_model += obj_lp

            # constraint variables
            cal_lp += sum(self.dict_cal[recipe_type_name][key]*variable[key] for key in self.dict_cal[recipe_type_name].keys())
            prot_lp += sum(self.dict_prot[recipe_type_name][key]*variable[key] for key in self.dict_prot[recipe_type_name].keys())
            fat_lp += sum(self.dict_fat[recipe_type_name][key]*variable[key] for key in self.dict_fat[recipe_type_name].keys())
            carb_lp += sum(self.dict_carb[recipe_type_name][key]*variable[key] for key in self.dict_carb[recipe_type_name].keys())
            price_lp += sum(self.dict_price[recipe_type_name][key]*variable[key] for key in self.dict_price[recipe_type_name].keys())
            time_lp += sum(self.dict_time[recipe_type_name][key]*variable[key] for key in self.dict_time[recipe_type_name].keys())
            # title_lp += (self.dict_title[recipe_type_name][key] for key in self.dict_title[recipe_type_name].keys())

            #constraints
            lp_model += sum([variable[key] for key in self.dict_title[recipe_type_name].keys()]) <= 3
            # lp_model += sum([variable[key] for key in self.dict_title[recipe_type_name].keys()]) >= 1

            print(" ")
        # print title_lp

        #constraints
        lp_model += cal_lp <= self.daily_nutrients['cal_up']
        lp_model += cal_lp >= self.daily_nutrients['cal_low']
        lp_model += fat_lp >= self.daily_nutrients['fat_low']
        lp_model += fat_lp <= self.daily_nutrients['fat_up']
        lp_model += carb_lp >= self.daily_nutrients['carb_low']
        lp_model += carb_lp <= self.daily_nutrients['carb_up']
        lp_model += prot_lp >= self.daily_nutrients['prot_low']
        lp_model += prot_lp <= self.daily_nutrients['prot_up']

        lp_model.solve()
        # print lp_model

        print(" ")
        print("Status:",  pulp.LpStatus[lp_model.status])

        if pulp.LpStatus[lp_model.status] == "Optimal":

            #print the result
            print(" ")
            print('In order to satisfy your daily nutrition needs, you can eat a portion of: ')
            print(" ")

            c = 0
            p = 0
            f = 0
            cl = 0
            pr = 0
            t = 0
            suggested_recipes = []

            for recipe_type_name in self.recipe_types:
                recipe_type_name = recipe_type_name.strip()
                print(recipe_type_name + ':')
                for recipe_ID in self.dict_title[recipe_type_name].keys():
                    if vars()['x_' + recipe_type_name][recipe_ID].value() == 1.0:
                        suggested_recipes.append(recipe_ID)
                        print('recipeID ' + str(recipe_ID))
                        print('Title ' + str(self.dict_title[recipe_type_name][recipe_ID]))
                        print('Prot ' + str(float(self.dict_prot[recipe_type_name][recipe_ID])))
                        print('Carb ' + str(float(self.dict_carb[recipe_type_name][recipe_ID])))
                        print('Fat ' + str(float(self.dict_fat[recipe_type_name][recipe_ID])))
                        print('Cal ' + str(float(self.dict_cal[recipe_type_name][recipe_ID])))
                        print('Price ' + str(self.dict_price[recipe_type_name][recipe_ID]))
                        print('Time ' + str(self.dict_time[recipe_type_name][recipe_ID]))
                        print(" ")
                        p += self.dict_prot[recipe_type_name][recipe_ID]
                        c += self.dict_carb[recipe_type_name][recipe_ID]
                        f += self.dict_fat[recipe_type_name][recipe_ID]
                        cl += self.dict_cal[recipe_type_name][recipe_ID]
                        pr += self.dict_price[recipe_type_name][recipe_ID]
                        t += self.dict_time[recipe_type_name][recipe_ID]

            print(" ")
            print(" With eating a portion of suggested recipes you will take: ")
            print(" ")
            print('Total Protein (grams): ')
            print(p)
            print('Protein intake range is ' + str(self.daily_nutrients['prot_low']) + ' grams - ' + str(self.daily_nutrients['prot_up']) + ' grams')
            print(" ")
            print('Total Fat (grams): ')
            print(f)
            print('(Fat intake range is ' + str(self.daily_nutrients['fat_low']) + ' grams - ' + str(self.daily_nutrients['fat_up']) + ' grams')
            print(" ")
            print('Total Carb (grams): ')
            print(c)
            print('(Carbs intake range is ' + str(self.daily_nutrients['carb_low']) + ' grams - ' + str(self.daily_nutrients['carb_up']) + ' grams')
            print(" ")
            print('Total Calories (kcal): ')
            print(cl)
            print('(Calorie intake range is ' + str(self.daily_nutrients['cal_low']) + ' kcal - ' + str(self.daily_nutrients['cal_up']) + ' kcal')
            print(" ")
            print('Total Price (cents): ')
            print(pr)
            print(" ")
            print('Total Time (in minutes): ')
            print(t)

            return {'suggested_recipes' : suggested_recipes, 'total_nutrients_taken' : {'calories' : cl, 'protein' : p, 'carb' : c, 'fat' : f, 'price' : pr, 'time' : t }}
        else:
            print("****Solution is NOT Optimal****")
            return {'suggested_recipes' : [], 'total_nutrients_taken' : {'calories' : 0, 'protein' : 0, 'carb' : 0, 'fat' : 0, 'price' : 0, 'time' : 0 }}


    def get_lp_output(self, suggested_recipes):
       diet_recipes = []
       for recipe_ID in suggested_recipes:
           response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/" + str(recipe_ID) + "/information?includeNutrition=true",
             headers={
               "X-Mashape-Key": settings.SPOONACULAR_KEY,
               "Accept": "application/json"
             }
           )
           diet_recipes.append(response.body)
           # print response.body
       return diet_recipes
