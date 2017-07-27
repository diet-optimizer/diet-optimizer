<<<<<<< HEAD
# from diet_optimizer import *
from __init__ import *
from models import *
from settings import *
from forms import SignupForm, LoginForm, PersonalDetailsForm, SettingsForm,FeedbackForm
from sqlalchemy.sql import select

@app.route('/', methods=['GET'])
@cross_origin()
def index():
    print random.choice(USDAfoods.query.all())
    return render_template('index.html')


@app.route('/about', methods=['GET'])
@cross_origin()
def about():
    return render_template('about.html')


@app.route('/signup1', methods=['GET', 'POST'])
@cross_origin()
def signup1():
    if 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        form = SignupForm(request.form)
        if form.validate() == False:
            return render_template('signup1.html', form=form)
        else:
            try:
                newuser = UserDB("xxxx", "xxxx", request.form['nick_name'], request.form['email'],
                                 request.form['password'], 0, 0, None, None, None, None)
                db.session.add(newuser)
                db.session.commit()
                global email
                global username
                global password
                email = newuser.email
                username = newuser.nickname
                password = newuser.pwdhash
                return redirect(url_for('personal_details'))
                # url_for needs the function inside the route
            except:
                db.session.rollback()
                print("Unexpected error:", sys.exc_info()[0])
                raise
    elif request.method == 'GET':
        form = SignupForm()
        return render_template('signup1.html', form=form)


@app.route('/personal_details', methods=['GET', 'POST'])
@cross_origin()
def personal_details():
    if request.method == 'POST':
        form = PersonalDetailsForm(request.form)
        if form.validate() == False:
            return render_template('personal_details.html', form=form)
        else:
            try:
                user = UserDB.query.filter_by(nickname=username).first()
                ##enter missing info of user in databse : change them from NULL to new entry
                user.lastname = form.last_name.data
                user.firstname = form.first_name.data
                if request.form.get("weightunit") == "lbs":
                    user.weight = form.weight.data / 2.20462
                else:
                    user.weight = form.weight.data

                if request.form.get("heightunit") == "in":
                    user.height = form.height.data / 0.393701
                else:
                    user.height = form.height.data
                user.birthdate = form.birth_date.data
                user.activitylevel = form.activity_level.data
                user.diet = form.diet.data
                user.gender = form.gender.data
                #add each element of the intolerence list in the database
                for i in form.intolerences.data :
                    user_intolerence = Intolerences(user.uid,i)
                    db.session.add(user_intolerence)
                db.session.commit()

                return redirect(url_for('profile'))

            # url_for needs the function inside the route
            except:
                db.session.rollback()
                print("Unexpected error:", sys.exc_info()[0])
                raise
    elif request.method == 'GET':
        form = PersonalDetailsForm()
        return render_template('personal_details.html', form=form)


@app.route('/login', methods=['GET','POST'])
@cross_origin()
def login():
    # if 'email' in session:
    if 'user_name' in session:
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('login.html', form=form)
        else:
            # email = form.email.data
            user_name = form.nick_name.data
            password = form.password.data
            username = form.nick_name.data
            # user = UserDB.query.filter_by(email=email).first()
            user = UserDB.query.filter_by(nickname=user_name).first()
            if user is not None and user.check_password(password):
                session['user_name'] = form.nick_name.data
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('login'))


    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@cross_origin()
def logout():
    session.pop('user_name', None)
    return redirect(url_for('index'))


@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route('/profile', methods=['GET'])
@cross_origin()
def profile():
    if 'user_name' in session :
        user = UserDB.query.filter_by(nickname=session.get('user_name',None)).first()
    elif username is not None :
        user = UserDB.query.filter_by(nickname=username).first()
    intol = Intolerences.query.filter_by(uid=user.uid)

    if user.birthdate > datetime.date.today().replace(year=user.birthdate.year):
        age = datetime.date.today().year - user.birthdate.year - 1
    else:
        age = datetime.date.today().year - user.birthdate.year

    current_user = User(age, user.weight, user.height, user.gender, user.activitylevel)
    print '**************'
    print current_user.weight
    print current_user.height
    print '################################'
    obj = request.args.get('obj')
    obj_nut = request.args.get('objNut')

    session['e_mail']=user.email
    session['first_name']=user.firstname
    session['last_name']=user.lastname
    session['birth_date']=user.birthdate
    session['diet']=user.diet
    session['gender']=user.gender
    intolerences=''
    for key in intol:
        intolerences= key.intolerencename + ' ' +intolerences
    session['intolerences']=intolerences
    session['age'] = age
    session['exercise_level'] = user.activitylevel
    session['obj'] = obj
    session['obj_nut'] = obj_nut

    user_daily_nutrients = current_user.daily_nutrients
    session['carb_low'] = user_daily_nutrients['carb_low']
    session['carb_up'] = user_daily_nutrients['carb_up']
    session['prot_low'] = user_daily_nutrients['prot_low']
    session['prot_up'] = user_daily_nutrients['prot_up']
    session['fat_low'] = user_daily_nutrients['fat_low']
    session['fat_up'] = user_daily_nutrients['fat_up']
    session['cal_low'] = user_daily_nutrients['cal_low']
    session['cal_up'] = user_daily_nutrients['cal_up']

    return render_template('profile.html', response={'user_info': {'age': age, 'weight': user.weight, 'height': user.height,
                          'gender': user.gender, 'exercise_level': user.activitylevel,
                          'diet': user.diet, 'intolerances': intolerences, 'obj': obj,
                          'obj_nut': obj_nut},'user_daily_nutrients': user_daily_nutrients})


@app.route('/history', methods=['GET','POST'])
@cross_origin()
def history():
    if 'user_name' in session:
        user = UserDB.query.filter_by(nickname=session.get('user_name', None)).first()
    elif username is not None:
        user = UserDB.query.filter_by(nickname=username).first()
    feed_back=Feedback.query.filter_by(uid=user.uid).all()
    print feed_back
    form = FeedbackForm(request.form)
    form.recipe.choices = [(Recipe.query.filter_by(rid=i.rid).first().name, Recipe.query.filter_by(rid=i.rid).first().name) for i in feed_back]
    recipes_name=[Recipe.query.filter_by(rid=i.rid).first().name for i in feed_back]
    recipes_link=[Recipe.query.filter_by(rid=i.rid).first().link for i in feed_back]
    feedback = Feedback.query.filter_by(uid=user.uid)
    marks = [key.mark for key in feedback]
    print marks
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('history.html', form=form)
        else:
            try:
                id = Recipe.query.filter_by(name=form.recipe.data).first().rid
                rate = Feedback.query.filter_by(rid=id).first()
                rate.mark=form.mark.data
                db.session.commit()
                return redirect(url_for('history'))
            except:
                db.session.rollback()
                print("Unexpected error:", sys.exc_info()[0])
                raise

    elif request.method == 'GET':
        #        return render_template('history.html',form=form)
        return render_template('history.html', form=form, response={'recipes_name' : recipes_name, 'recipes_link' : recipes_link, 'marks' : marks})


@app.route('/settings', methods=['GET', 'POST'])
@cross_origin()
def settings():
    if 'user_name' in session :
        user = UserDB.query.filter_by(nickname=session.get('user_name',None)).first()
    elif username is not None :
        user = UserDB.query.filter_by(nickname=username).first()
    form = SettingsForm()
    intol = Intolerences.query.filter_by(uid=user.uid)
    intolerences=''
    for key in intol:
        intolerences= key.intolerencename + ' ' +intolerences
    session['intolerences']=intolerences

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('settings.html', form=form, response={'user_info': {'birthdate' : user.birthdate, 'weight': user.weight, 'height': user.height,
                          'gender': user.gender, 'activitylevel': user.activitylevel,
                          'diet': user.diet, 'intolerances': intolerences}})
        else:
            if request.form.get("weightunit") == "lbs":
                user.weight = form.weight.data / 2.20462
            else:
                user.weight = form.weight.data

            if request.form.get("heightunit") == "in":
                user.height = form.height.data / 0.393701
            else:
                user.height = form.height.data
            birthdate = form.birth_date.data
            activitylevel = form.activity_level.data
            diet = form.diet.data
            gender = form.gender.data
            print gender
            for key in intol:
                db.session.delete(key)
                db.session.commit()
            intolerences_data = form.intolerences.data
            intolerences=''
            for key in intolerences_data:
                intol_temp = Intolerences(user.uid, key)
                db.session.add(intol_temp)
                db.session.commit()
                intolerences = intolerences + ' ' + key
            print intolerences
            #user.height = form.height.data
            #user.weight = form.weight.data
            user.birthdate = form.birth_date.data
            user.activitylevel = form.activity_level.data
            user.diet = form.diet.data
            user.gender = form.gender.data
            #intol.intolerencename = session.get('intolerences')
            db.session.commit()
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('settings.html', form=form, response={'user_info': {'birthdate' : user.birthdate, 'weight': user.weight, 'height': user.height,
                          'gender': user.gender, 'activitylevel': user.activitylevel,
                          'diet': user.diet, 'intolerances': intolerences}})



@app.route('/basicresults', methods=['GET'])
@cross_origin()
def get_usr_input_basic():

    current_user = UserDB.query.filter_by(email=session.get('e_mail', None)).first()
    intol = Intolerences.query.filter_by(uid=current_user.uid).first()
    cuisine = request.args.getlist('cuisine')
    recipe_types = request.args.getlist('recipeTypes')
    raw_groups = request.args.getlist('rawGroups')
	# # exclude_ingredients = request.args.getlist('excludeIngredients')
    obj = request.args.get('obj')
    obj_nut = request.args.get('objNut')

    if current_user.birthdate > datetime.date.today().replace(year=current_user.birthdate.year):
        age=datetime.date.today().year - current_user.birthdate.year - 1
    else:
        age=datetime.date.today().year - current_user.birthdate.year

    user = User(age, current_user.weight, current_user.height, current_user.gender, current_user.activitylevel)

    session['age'] = age
    session['height'] = current_user.height
    session['weight'] = current_user.weight
    session['gender'] = current_user.gender
    session['exercise_level'] = current_user.activitylevel
    session['cuisine'] = cuisine
    session['diet'] = current_user.diet
    session['intolerances'] = intol.intolerencename
    session['recipe_types'] = recipe_types
    session['obj'] = obj
    session['obj_nut'] = obj_nut
    session['raw_groups'] = raw_groups

    user_daily_nutrients = user.daily_nutrients

    session['carb_low'] = user_daily_nutrients['carb_low']
    session['carb_up'] = user_daily_nutrients['carb_up']
    session['prot_low'] = user_daily_nutrients['prot_low']
    session['prot_up'] = user_daily_nutrients['prot_up']
    session['fat_low'] = user_daily_nutrients['fat_low']
    session['fat_up'] = user_daily_nutrients['fat_up']
    session['cal_low'] = user_daily_nutrients['cal_low']
    session['cal_up'] = user_daily_nutrients['cal_up']

    return render_template('basicresults.html', response={'user_info' : {'age':age, 'weight' : current_user.weight, 'height' : current_user.height, 'gender' : current_user.gender, 'exercise_level' : current_user.activitylevel,
    'cuisine' : cuisine, 'diet' : current_user.diet, 'intolerances' : intol.intolerencename, 'obj' : obj, 'obj_nut' : obj_nut, 'recipe_types' : recipe_types, 'raw_groups' : raw_groups},
	'user_daily_nutrients' : user_daily_nutrients})


@app.route('/results', methods=['GET'])
@cross_origin()
def get_usr_input():
    print '*****************'
    raw_groups = request.args.getlist('rawGroups')
    raw_list = [s.replace("+", " ") for s in raw_groups]
    raw_list = [s.replace("%2F", "/") for s in raw_list]
    print raw_list, 'RAW'
    print '*************'
    data = []
    for i in range(2):
        # data.append(random.choice(USDAfoods.query.all()))
        data.append(random.choice(USDAfoods.query.filter(USDAfoods.Group_Name.in_(raw_list)).all()))
    print type(data)
    print '****************'
    raw_foods_temp = {'raw': [d.__dict__ for d in data]}
    # print [type(d) for d in data]

    raw_foods = []
    for d in data:
        dct = {
            "NDB_No": d.NDB_No,
            "Desc": d.Desc,
            "Cal": d.Cal,
            "Prot": d.Prot,
            "Fat": d.Fat,
            "Carb": d.Carb,
            "Group_Code": d.Group_Code,
            "Group_Name": d.Group_Name
        }
        raw_foods.append(dct)

    total_raw_calories = sum(item['Cal'] for item in raw_foods_temp['raw'])
    total_raw_carbs = sum(item['Carb'] for item in raw_foods_temp['raw'])
    total_raw_protein = sum(item['Prot'] for item in raw_foods_temp['raw'])
    total_raw_fat = sum(item['Fat'] for item in raw_foods_temp['raw'])
    # print total_raw_fat
    # print total_raw_protein
    # print total_raw_carbs
    print raw_foods, "SECOND"

    # raw1 = random.choice(USDAfoods.query.all())
    # raw2 = random.choice(USDAfoods.query.all())

    # total_raw_calories = raw1.Cal + raw2.Cal
    # total_raw_carbs = raw1.Carb + raw2.Carb
    # total_raw_protein = raw1.Prot + raw2.Prot
    # total_raw_fat = raw1.Fat + raw2.Fat

    # raw_foods = [raw1,raw2]
##########################################

    current_user = UserDB.query.filter_by(email=session.get('e_mail', None)).first()
    intol = Intolerences.query.filter_by(uid=current_user.uid).first()

    if current_user.birthdate > datetime.date.today().replace(year=current_user.birthdate.year):
        age = datetime.date.today().year - current_user.birthdate.year - 1
    else:
        age = datetime.date.today().year - current_user.birthdate.year

    ###########################################################

    #age = int(request.args.get('age'))
    #height = float(request.args.get('height'))
    #weight = float(request.args.get('weight'))
    #gender = request.args.get('gender')
    #exercise_level = request.args.get('exerciseLevel')
    cuisine = request.args.getlist('cuisine')
    diet = request.args.get('diet')
    #intolerances = request.args.getlist('intolerances')
    recipe_types = request.args.getlist('recipeTypes')
    # exclude_ingredients = request.args.getlist('excludeIngredients')
    obj = request.args.get('obj')
    obj_nut = request.args.get('objNut')

    #user = User(age, weight, height, gender, exercise_level)
    user = User(age, current_user.weight, current_user.height, current_user.gender, current_user.activitylevel)

    # session['age'] = age
    # session['height'] = height
    # session['weight'] = weight
    # session['gender'] = gender
    # session['exercise_level'] = exercise_level
    # session['cuisine'] = cuisine
    # session['diet'] = diet
    # session['intolerances'] = intolerances
    # session['recipe_types'] = recipe_types
    # session['obj'] = obj
    # session['obj_nut'] = obj_nut

    session['age'] = age
    session['height'] = current_user.height
    session['weight'] = current_user.weight
    session['gender'] = current_user.gender
    session['exercise_level'] = current_user.activitylevel
    session['cuisine'] = cuisine
    session['diet'] = diet
    session['intolerances'] = intol.intolerencename
    session['recipe_types'] = recipe_types
    session['obj'] = obj
    session['obj_nut'] = obj_nut

    user_daily_nutrients = user.daily_nutrients  # without the subtraction of raw foods info
    print "user daily nutrients"
    print user_daily_nutrients

    user_daily_nutrients['cal_up'] = user_daily_nutrients['cal_up'] - total_raw_calories
    user_daily_nutrients['carb_up'] = user_daily_nutrients['carb_up'] - total_raw_carbs
    user_daily_nutrients['fat_up'] = user_daily_nutrients['fat_up'] - total_raw_fat
    user_daily_nutrients['prot_up'] = user_daily_nutrients['prot_up'] - total_raw_protein

    print "user daily nutrients after raw foods"
    print user_daily_nutrients

    # session['carb_low'] = user_daily_nutrients['carb_low'] - total_raw_carbs
    # session['carb_up'] = user_daily_nutrients['carb_up'] - total_raw_carbs
    # session['prot_low'] = user_daily_nutrients['prot_low'] - total_raw_protein
    # session['prot_up'] = user_daily_nutrients['prot_up'] - total_raw_protein
    # session['fat_low'] = user_daily_nutrients['fat_low'] - total_raw_fat
    # session['fat_up'] = user_daily_nutrients['fat_up'] - total_raw_fat
    # session['cal_low'] = user_daily_nutrients['cal_low'] - total_raw_calories
    # session['cal_up'] = user_daily_nutrients['cal_up'] - total_raw_calories
    print '****************'
    req = RecipeHandler(user.daily_nutrients, cuisine, diet, intol.intolerencename, "", recipe_types)
    print '****************'
    res = req.get_recipes()
    print '*******************'
    lp = LinearProgrammingSolver(obj, obj_nut, res['dict_prot'], res['dict_fat'], res['dict_cal'], res['dict_carb'],
                                 res['dict_title'], res['dict_price'], res['dict_time'], res['recipe_types'],
                                 user.daily_nutrients)

    lp_func = lp.func_lp()

    suggested_recipes = lp_func['suggested_recipes']
    total_nutrients_taken = lp_func['total_nutrients_taken']
    diet_recipes = lp.get_lp_output(suggested_recipes)

    print (total_raw_calories, total_raw_carbs, total_raw_protein, total_raw_fat)
    print raw_foods, "RAW FOODS"
    # print raw1.Desc
    # print raw2.Desc

    print current_user.weight
    print current_user.height
    print current_user.gender
    print current_user.activitylevel
    print cuisine
    print diet
    print obj
    print obj_nut
    print recipe_types
    print raw_groups
    print user_daily_nutrients
    print diet_recipes
    print total_nutrients_taken
    print raw_foods

    for key in diet_recipes :
        if Recipe.query.filter_by(ridapi=key["id"]).first():
            print "recipe already in database"
            if Feedback.query.filter_by(uid=current_user.uid).first():
                print "user already tried this recipe"
            else :
                temp_recipes = Recipe.query.filter_by(ridapi=key["id"]).first()
                temp_feedback = Feedback(temp_recipes.rid, current_user.uid, None)
                db.session.add(temp_feedback)
                db.session.commit()
        else:
            temp_recipes = Recipe(key["id"], key["title"], key["sourceUrl"])
            db.session.add(temp_recipes)
            db.session.commit()
            temp_feedback = Feedback(temp_recipes.rid, current_user.uid, None)
            db.session.add(temp_feedback)
            db.session.commit()


    return render_template('results.html', response={
        'user_info': {'age': age, 'weight': current_user.weight, 'height': current_user.height, 'gender': current_user.gender,
                      'exercise_level': current_user.activitylevel,
                      'cuisine': cuisine, 'diet': diet, 'intolerances': intol.intolerencename, 'obj': obj, 'obj_nut': obj_nut,
                      'recipe_types': recipe_types, "raw_groups": raw_groups},
        'user_daily_nutrients': user_daily_nutrients, 'recipes': diet_recipes,
        'total_nutrients_taken': total_nutrients_taken, 'raw_foods': raw_foods})


@app.route('/apiresults', methods=['GET'])
@cross_origin()
def get_usr_input_api():
    data = []
    for i in range(2):
        # data.append(random.choice(USDAfoods.query.all()))
        data.append(
            random.choice(USDAfoods.query.filter(USDAfoods.Group_Name.like('Vegetables and Vegetable Products')).all()))
    print "********"
    print type(data)
    print "********"
    raw_foods_temp = {'raw': [d.__dict__ for d in data]}
    # print [type(d) for d in data]

    raw_foods = []
    for d in data:
        dct = {
            "NDB_No": d.NDB_No,
            "Desc": d.Desc,
            "Cal": d.Cal,
            "Prot": d.Prot,
            "Fat": d.Fat,
            "Carb": d.Carb,
            "Group_Code": d.Group_Code,
            "Group_Name": d.Group_Name
        }
        raw_foods.append(dct)

    total_raw_calories = sum(item['Cal'] for item in raw_foods_temp['raw'])
    total_raw_carbs = sum(item['Carb'] for item in raw_foods_temp['raw'])
    total_raw_protein = sum(item['Prot'] for item in raw_foods_temp['raw'])
    total_raw_fat = sum(item['Fat'] for item in raw_foods_temp['raw'])
    print total_raw_fat
    print total_raw_protein
    print total_raw_carbs

    age = int(request.args.get('age'))
    height = float(request.args.get('height'))
    weight = float(request.args.get('weight'))
    gender = request.args.get('gender')
    exercise_level = request.args.get('exerciseLevel')
    cuisine = request.args.getlist('cuisine')
    diet = request.args.get('diet')
    intolerances = request.args.getlist('intolerances')
    recipe_types = request.args.getlist('recipeTypes')
    # exclude_ingredients = request.args.getlist('excludeIngredients')
    obj = request.args.get('obj')
    obj_nut = request.args.get('objNut')

    user = User(age, weight, height, gender, exercise_level)

    user_daily_nutrients = user.daily_nutrients

    print "USER DAILY NUT ***********"
    print user_daily_nutrients

    req = RecipeHandler(user.daily_nutrients, cuisine, diet, intolerances, "", recipe_types)

    res = req.get_recipes()

    lp = LinearProgrammingSolver(obj, obj_nut, res['dict_prot'], res['dict_fat'], res['dict_cal'], res['dict_carb'],
                                 res['dict_title'], res['dict_price'], res['dict_time'], res['recipe_types'],
                                 user.daily_nutrients)

    lp_func = lp.func_lp()

    suggested_recipes = lp_func['suggested_recipes']
    total_nutrients_taken = lp_func['total_nutrients_taken']
    diet_recipes = lp.get_lp_output(suggested_recipes)

    print (total_raw_calories, total_raw_carbs, total_raw_protein, total_raw_fat)

    return jsonify({'user_info': {'age': age, 'weight': weight, 'height': height, 'gender': gender,
                                  'exercise_level': exercise_level,                                  'cuisine': cuisine, 'diet': diet, 'intolerances': intolerances, 'obj': obj,
                                  'obj_nut': obj_nut, 'recipe_types': recipe_types},
                    'user_daily_nutrients': user_daily_nutrients, 'recipes': diet_recipes,
                    'total_nutrients_taken': total_nutrients_taken, 'raw_foods': raw_foods})


# @app.route('/recresults', methods=['GET'])
# @cross_origin()
# def recompute_usr_input():
#	 data = []
#	 for i in range(2):
#		 # data.append(random.choice(USDAfoods.query.all()))
#		 data.append(random.choice(USDAfoods.query.filter(USDAfoods.Group_Name.like('Vegetables and Vegetable Products')).all()))
#	 print "********"
#	 print type(data)
#	 print "********"
#	 raw_foods_temp = {'raw': [d.__dict__ for d in data]}
#	 # print [type(d) for d in data]

#	 raw_foods = []
#	 for d in data:
#		 dct = {
#			 "NDB_No": d.NDB_No, 
#			 "Desc": d.Desc, 
#			 "Cal": d.Cal, 
#			 "Prot": d.Prot, 
#			 "Fat": d.Fat, 
#			 "Carb": d.Carb, 
#			 "Group_Code": d.Group_Code, 
#			 "Group_Name": d.Group_Name
#		 }
#		 raw_foods.append(dct)

#	 total_raw_calories = sum(item['Cal'] for item in raw_foods_temp['raw'])
#	 total_raw_carbs = sum(item['Carb'] for item in raw_foods_temp['raw'])
#	 total_raw_protein = sum(item['Prot'] for item in raw_foods_temp['raw'])
#	 total_raw_fat = sum(item['Fat'] for item in raw_foods_temp['raw'])
#	 # print total_raw_fat
#	 # print total_raw_protein
#	 # print total_raw_carbs
#	 print raw_foods

#	 age = session.get('age')
#	 height = session.get('height')
#	 weight = session.get('weight')
#	 gender = session.get('gender')
#	 exercise_level = session.get('exercise_level')
#	 cuisine = session.get('cuisine')
#	 diet = session.get('diet')
#	 intolerances = session.get('intolerances')
#	 recipe_types = session.get('recipe_types')
#	 obj = session.get('obj')
#	 obj_nut = session.get('obj_nut')

#	 user = User(age, weight, height, gender, exercise_level)

#	 cuisine_q = request.args.getlist('cuisine')
#	 diet_q = request.args.get('diet')
#	 intolerances_q = request.args.getlist('intolerances')
#	 recipe_types_q = request.args.getlist('recipeTypes')
#	 obj_q = request.args.get('obj')
#	 obj_nut_q = request.args.get('objNut')
#	 carb_low = request.args.get('carbLow')
#	 carb_up = request.args.get('carbUp')
#	 prot_low = request.args.get('protLow')
#	 prot_up = request.args.get('protUp')
#	 fat_low = request.args.get('fatLow')
#	 fat_up = request.args.get('fatUp')
#	 cal_low = request.args.get('calLow')
#	 cal_up = request.args.get('calUp')

#	 if len(cuisine_q) > 0:
#		 cuisine = cuisine_q
#	 if diet_q != '':
#		 diet = diet_q
#	 if len(intolerances_q) > 0:
#		 intolerances = intolerances_q
#	 if len(recipe_types_q)  > 0:
#		 print '****RECIPETYPES'
#		 recipe_types = recipe_types_q
#	 if obj_q != '':
#		 obj = obj_q
#	 if obj_nut_q != '':
#		 obj_nut = obj_nut_q

#	 if carb_low != '':
#		 user.daily_nutrients['carb_low'] = float(carb_low)
#	 if carb_up != '':
#		 user.daily_nutrients['carb_up'] = float(carb_up)
#	 if prot_low != '':
#		 user.daily_nutrients['prot_low'] = float(prot_low)
#	 if prot_up != '':
#		 user.daily_nutrients['prot_up'] = float(prot_up)
#	 if fat_low != '':
#		 user.daily_nutrients['fat_low'] = float(fat_low)
#	 if fat_up != '':
#		 user.daily_nutrients['fat_up'] = float(fat_up)
#	 if cal_low != '':
#		 user.daily_nutrients['cal_low'] = float(cal_low)
#	 if cal_up != '':
#		 user.daily_nutrients['cal_up'] = float(cal_up)

#	 req = RecipeHandler(user.daily_nutrients, cuisine, diet, intolerances, "", recipe_types)

#	 ress = req.get_recipes()

#	 lp = LinearProgrammingSolver(obj, obj_nut, ress['dict_prot'], ress['dict_fat'], ress['dict_cal'], ress['dict_carb'], ress['dict_title'], ress['dict_price'], ress['dict_time'], ress['recipe_types'], user.daily_nutrients)

#	 lp_func = lp.func_lp()

#	 suggested_recipes = lp_func['suggested_recipes']
#	 total_nutrients_taken = lp_func['total_nutrients_taken']#	 diet_recipes = lp.get_lp_output(suggested_recipes)

#	 return render_template('recresults.html', response={'user_info' : {'age':age, 'weight' : weight, 'height' : height, 'gender' : gender, 'exercise_level' : exercise_level,
#	 'cuisine' : cuisine, 'diet' : diet, 'intolerances' : intolerances, 'obj' : obj, 'obj_nut' : obj_nut, 'recipe_types' : recipe_types},
#	 'user_daily_nutrients' : user.daily_nutrients, 'recipes' : diet_recipes, 'total_nutrients_taken' : total_nutrients_taken, 'raw_foods' : raw_foods})

# @app.route('/newform', methods=['GET'])
# @cross_origin()
# def new_form():
#     age = session.get('age')
#     height = session.get('height')
#     weight = session.get('weight')
#     gender = session.get('gender')
#     exercise_level = session.get('exercise_level')
#     cuisine = session.get('cuisine')
#     diet = session.get('diet')
#     intolerances = session.get('intolerances')
#     recipe_types = session.get('recipe_types')
#     obj = session.get('obj')
#     obj_nut = session.get('obj_nut')
#
#     user = User(age, weight, height, gender, exercise_level)
#
#     user_daily_nutrients = user.daily_nutrients
#
#     carb_low = user_daily_nutrients['carb_low']
#     carb_up = user_daily_nutrients['carb_up']
#     prot_low = user_daily_nutrients['prot_low']
#     prot_up = user_daily_nutrients['prot_up']
#     fat_low = user_daily_nutrients['fat_low']
#     fat_up = user_daily_nutrients['fat_up']
#     cal_low = user_daily_nutrients['cal_low']
#     cal_up = user_daily_nutrients['cal_up']
#
#     cuisine_dictionary = {
#         '': 'All',
#         'african': 'African',
#         'chinese': 'Chinese',
#         'japanese': 'Japanese',
#         'korean': 'Korean',
#         'vietnamese': 'Vietnamese',
#         'thai': 'Thai',
#         'indian': 'Indian',
#         'british': 'British',
#         'irish': 'Irish',
#         'french': 'French',
#         'italian': 'Italian',
#         'mexican': 'Mexican',
#         'spanish': 'Spanish',
#         'middle+eastern': 'Middle Eastern',
#         'jewish': 'Jewish',
#         'american': 'American',
#         'cajun': 'Cajun',
#         'southern': 'Southern',
#         'greek': 'Greek',
#         'german': 'German',
#         'nordic': 'Nordic',
#         'eastern+european': 'Eastern european',
#         'caribbean': 'Caribbean',
#         'latin+american': 'Latin American'
#     }
#
#     diet_dictionary = {
#         '': 'None',
#         'pescetarian': 'Pescetarian',
#         'lacto+vegetarian': 'Lacto vegetarian',
#         'ovo+vegetarian': 'Ovo vegetarian',
#         'vegan': 'Vegan',
#         'paleo': 'Paleo',
#         'primal': 'Primal',
#         'vegetarian': 'Vegetarian'
#     }
#
#     intolerances_dictionary = {
#         '': 'None',
#         'dairy': 'Dairy',
#         'egg': 'Egg',
#         'gluten': 'Gluten',
#         'peanut': 'Peanut',
#         'sesame': 'Sesame',
#         'seafood': 'Seafood',
#         'shellfish': 'Shellfish',
#         'soy': 'Soy',
#         'sulfite': 'Sulfite',
#         'tree+nut': 'Tree Nut',
#         'wheat': 'Wheat'
#     }
#
#     obj_nut_list = [
#         'Calories',
#         'Protein',
#         'Carbs',
#         'Fat',
#         'Price',
#         'Time'
#     ]
#
#     obj_list = [
#         'Max',
#         'Min'
#     ]
#
#     recipe_types_dictionary = {
#         'main+course': 'Main Course',
#         'side+dish': 'Side Dish',
#         'dessert': 'Dessert',
#         'appetizer': 'Appetizer',
#         'salad': 'Salad',
#         'bread': 'Bread',
#         'breakfast': 'Breakfast',
#         'soup': 'Soup',
#         'beverage': 'Beverage',
#         # 'sauce' : 'Sauce',
#         # 'drink' : 'Drink'
#     }
#
#     return render_template('newform.html', response={
#         'carb_low': carb_low,
#         'carb_up': carb_up,
#         'prot_low': prot_low,
#         'prot_up': prot_up,
#         'fat_low': fat_low,
#         'fat_up': fat_up,
#         'cal_low': cal_low,
#         'cal_up': cal_up,
#         'cuisine_dictionary': cuisine_dictionary,
#         'diet_dictionary': diet_dictionary,
#         'intolerances_dictionary': intolerances_dictionary,
#         'recipe_types_dictionary': recipe_types_dictionary,
#         'obj_nut_list': obj_nut_list,
#         'obj_list': obj_list,
#         'cuisine': cuisine,
#         'diet': diet,
#         'intolerances': intolerances,
#         'recipe_types': recipe_types,
#         'obj': obj,
#         'obj_nut': obj_nut
#     })

=======
from diet_optimizer import *
from forms import SignupForm, LoginForm

@app.route('/', methods=['GET'])
@cross_origin()
def index():
	print random.choice(USDAfoods.query.all())
	return render_template('index.html')

@app.route('/about', methods=['GET'])
@cross_origin()
def about():
	return render_template('about.html')

@app.route('/signup', methods=['GET','POST'])
@cross_origin()
def signup():
	if 'email' in session:
		return redirect(url_for('home'))

	form = SignupForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			try:
				newuser = UserDB(form.first_name.data, form.last_name.data, form.nick_name.data, form.email.data, form.password.data)
				db.session.add(newuser)
				db.session.commit()

				# session['email'] = newuser.email
				session['user_name'] = newuser.nickname
				return redirect(url_for('home')) 
				#url_for needs the function inside the route
			except:
				db.session.rollback()
				print("Unexpected error:", sys.exc_info()[0])
				raise 

	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
@cross_origin()
def login():
	# if 'email' in session:
	if 'user_name' in session:
		return redirect(url_for('home'))

	form = LoginForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('login.html', form=form)
		else:
			# email = form.email.data
			user_name = form.nick_name.data
			password = form.password.data

			# user = UserDB.query.filter_by(email=email).first()
			user = UserDB.query.filter_by(nickname=user_name).first()
			print user
			if user is not None and user.check_password(password):
				# session['email'] = form.email.data
				session['user_name'] = form.nick_name.data
				return redirect(url_for('home')) 
			else:
				return redirect(url_for('login')) 

	elif request.method == 'GET':
		return render_template('login.html', form=form)

@app.route('/logout', methods=['GET','POST'])
@cross_origin()
def logout():
	session.pop('user_name', None)
	return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
	if 'user_name' not in session:
		return redirect(url_for('login'))

	return render_template("home.html")

@app.route('/basicresults', methods=['GET'])
@cross_origin()
def get_usr_input_basic():

	age = int(request.args.get('age'))
	height = float(request.args.get('height'))
	weight = float(request.args.get('weight'))
	gender = request.args.get('gender')
	exercise_level = request.args.get('exerciseLevel')
	cuisine = request.args.getlist('cuisine')
	diet = request.args.get('diet')
	intolerances = request.args.getlist('intolerances')
	recipe_types = request.args.getlist('recipeTypes')
	raw_groups = request.args.getlist('rawGroups')
	# exclude_ingredients = request.args.getlist('excludeIngredients')
	obj = request.args.get('obj')
	obj_nut = request.args.get('objNut')

	user = User(age, weight, height, gender, exercise_level)

	session['age'] = age
	session['height'] = height
	session['weight'] = weight
	session['gender'] = gender
	session['exercise_level'] = exercise_level
	session['cuisine'] = cuisine
	session['diet'] = diet
	session['intolerances'] = intolerances
	session['recipe_types'] = recipe_types
	session['obj'] = obj
	session['obj_nut'] = obj_nut
	session['raw_groups'] = raw_groups

	user_daily_nutrients = user.daily_nutrients

	session['carb_low'] = user_daily_nutrients['carb_low']
	session['carb_up'] = user_daily_nutrients['carb_up']
	session['prot_low'] = user_daily_nutrients['prot_low']
	session['prot_up'] = user_daily_nutrients['prot_up']
	session['fat_low'] = user_daily_nutrients['fat_low']
	session['fat_up'] = user_daily_nutrients['fat_up']
	session['cal_low'] = user_daily_nutrients['cal_low']
	session['cal_up'] = user_daily_nutrients['cal_up']

	return render_template('basicresults.html', response={'user_info' : {'age':age, 'weight' : weight, 'height' : height, 'gender' : gender, 'exercise_level' : exercise_level,
	'cuisine' : cuisine, 'diet' : diet, 'intolerances' : intolerances, 'obj' : obj, 'obj_nut' : obj_nut, 'recipe_types' : recipe_types, 'raw_groups' : raw_groups},
	'user_daily_nutrients' : user_daily_nutrients})


@app.route('/results', methods=['GET'])
@cross_origin()
def get_usr_input():
	raw_groups = request.args.getlist('rawGroups')
	raw_list = [s.replace("+"," ") for s in raw_groups]
	raw_list = [s.replace("%2F","/") for s in raw_list]
	print raw_list,'RAW'
	data = []
	for i in range(2):
		# data.append(random.choice(USDAfoods.query.all()))
		data.append(random.choice(USDAfoods.query.filter(USDAfoods.Group_Name.in_(raw_list)).all()))
	print "********"
	print type(data)
	print "********"
	raw_foods_temp = {'raw': [d.__dict__ for d in data]}
	# print [type(d) for d in data]
	
	raw_foods = []
	for d in data:
		dct = {
			"NDB_No": d.NDB_No, 
			"Desc": d.Desc, 
			"Cal": d.Cal, 
			"Prot": d.Prot, 
			"Fat": d.Fat, 
			"Carb": d.Carb, 
			"Group_Code": d.Group_Code, 
			"Group_Name": d.Group_Name
		}
		raw_foods.append(dct)

	total_raw_calories = sum(item['Cal'] for item in raw_foods_temp['raw'])
	total_raw_carbs = sum(item['Carb'] for item in raw_foods_temp['raw'])
	total_raw_protein = sum(item['Prot'] for item in raw_foods_temp['raw'])
	total_raw_fat = sum(item['Fat'] for item in raw_foods_temp['raw'])
	# print total_raw_fat
	# print total_raw_protein
	# print total_raw_carbs
	print raw_foods,"SECOND"

	# raw1 = random.choice(USDAfoods.query.all())
	# raw2 = random.choice(USDAfoods.query.all())

	# total_raw_calories = raw1.Cal + raw2.Cal
	# total_raw_carbs = raw1.Carb + raw2.Carb
	# total_raw_protein = raw1.Prot + raw2.Prot
	# total_raw_fat = raw1.Fat + raw2.Fat

	# raw_foods = [raw1,raw2]

	age = int(request.args.get('age'))
	height = float(request.args.get('height'))
	weight = float(request.args.get('weight'))
	gender = request.args.get('gender')
	exercise_level = request.args.get('exerciseLevel')
	cuisine = request.args.getlist('cuisine')
	diet = request.args.get('diet')
	intolerances = request.args.getlist('intolerances')
	recipe_types = request.args.getlist('recipeTypes')
	# exclude_ingredients = request.args.getlist('excludeIngredients')
	obj = request.args.get('obj')
	obj_nut = request.args.get('objNut')

	user = User(age, weight, height, gender, exercise_level)

	session['age'] = age
	session['height'] = height
	session['weight'] = weight
	session['gender'] = gender
	session['exercise_level'] = exercise_level
	session['cuisine'] = cuisine
	session['diet'] = diet
	session['intolerances'] = intolerances
	session['recipe_types'] = recipe_types
	session['obj'] = obj
	session['obj_nut'] = obj_nut

	user_daily_nutrients = user.daily_nutrients #without the subtraction of raw foods info
	print "user daily nutrients"
	print user_daily_nutrients

	user_daily_nutrients['cal_up'] = user_daily_nutrients['cal_up']-total_raw_calories
	user_daily_nutrients['carb_up'] = user_daily_nutrients['carb_up']-total_raw_carbs
	user_daily_nutrients['fat_up'] = user_daily_nutrients['fat_up']-total_raw_fat
	user_daily_nutrients['prot_up'] = user_daily_nutrients['prot_up']-total_raw_protein

	print "user daily nutrients after raw foods"
	print user_daily_nutrients

	# session['carb_low'] = user_daily_nutrients['carb_low'] - total_raw_carbs
	# session['carb_up'] = user_daily_nutrients['carb_up'] - total_raw_carbs
	# session['prot_low'] = user_daily_nutrients['prot_low'] - total_raw_protein
	# session['prot_up'] = user_daily_nutrients['prot_up'] - total_raw_protein
	# session['fat_low'] = user_daily_nutrients['fat_low'] - total_raw_fat
	# session['fat_up'] = user_daily_nutrients['fat_up'] - total_raw_fat
	# session['cal_low'] = user_daily_nutrients['cal_low'] - total_raw_calories
	# session['cal_up'] = user_daily_nutrients['cal_up'] - total_raw_calories

	req = RecipeHandler(user.daily_nutrients, cuisine, diet, intolerances, "", recipe_types)

	res = req.get_recipes()

	lp = LinearProgrammingSolver(obj, obj_nut, res['dict_prot'], res['dict_fat'], res['dict_cal'], res['dict_carb'], res['dict_title'], res['dict_price'], res['dict_time'], res['recipe_types'], user.daily_nutrients)

	lp_func = lp.func_lp()

	suggested_recipes = lp_func['suggested_recipes']
	total_nutrients_taken = lp_func['total_nutrients_taken']
	diet_recipes = lp.get_lp_output(suggested_recipes)

	print (total_raw_calories,total_raw_carbs,total_raw_protein,total_raw_fat)
	print raw_foods,"RAW FOODS"
	# print raw1.Desc
	# print raw2.Desc

	return render_template('results.html', response={'user_info' : {'age':age, 'weight' : weight, 'height' : height, 'gender' : gender, 'exercise_level' : exercise_level,
	'cuisine' : cuisine, 'diet' : diet, 'intolerances' : intolerances, 'obj' : obj, 'obj_nut' : obj_nut, 'recipe_types' : recipe_types, "raw_groups": raw_groups},
	'user_daily_nutrients' : user_daily_nutrients, 'recipes' : diet_recipes, 'total_nutrients_taken' : total_nutrients_taken, 'raw_foods' : raw_foods})

@app.route('/apiresults', methods=['GET'])
@cross_origin()
def get_usr_input_api():

	data = []
	for i in range(2):
		# data.append(random.choice(USDAfoods.query.all()))
		data.append(random.choice(USDAfoods.query.filter(USDAfoods.Group_Name.like('Vegetables and Vegetable Products')).all()))
	print "********"
	print type(data)
	print "********"
	raw_foods_temp = {'raw': [d.__dict__ for d in data]}
	# print [type(d) for d in data]
	
	raw_foods = []
	for d in data:
		dct = {
			"NDB_No": d.NDB_No, 
			"Desc": d.Desc, 
			"Cal": d.Cal, 
			"Prot": d.Prot, 
			"Fat": d.Fat, 
			"Carb": d.Carb, 
			"Group_Code": d.Group_Code, 
			"Group_Name": d.Group_Name
		}
		raw_foods.append(dct)

	total_raw_calories = sum(item['Cal'] for item in raw_foods_temp['raw'])
	total_raw_carbs = sum(item['Carb'] for item in raw_foods_temp['raw'])
	total_raw_protein = sum(item['Prot'] for item in raw_foods_temp['raw'])
	total_raw_fat = sum(item['Fat'] for item in raw_foods_temp['raw'])
	print total_raw_fat
	print total_raw_protein
	print total_raw_carbs

	age = int(request.args.get('age'))
	height = float(request.args.get('height'))
	weight = float(request.args.get('weight'))
	gender = request.args.get('gender')
	exercise_level = request.args.get('exerciseLevel')
	cuisine = request.args.getlist('cuisine')
	diet = request.args.get('diet')
	intolerances = request.args.getlist('intolerances')
	recipe_types = request.args.getlist('recipeTypes')
	# exclude_ingredients = request.args.getlist('excludeIngredients')
	obj = request.args.get('obj')
	obj_nut = request.args.get('objNut')

	user = User(age, weight, height, gender, exercise_level)

	user_daily_nutrients = user.daily_nutrients

	print "USER DAILY NUT ***********"
	print user_daily_nutrients

	req = RecipeHandler(user.daily_nutrients, cuisine, diet, intolerances, "", recipe_types)

	res = req.get_recipes()

	lp = LinearProgrammingSolver(obj, obj_nut, res['dict_prot'], res['dict_fat'], res['dict_cal'], res['dict_carb'], res['dict_title'], res['dict_price'], res['dict_time'], res['recipe_types'], user.daily_nutrients)

	lp_func = lp.func_lp()

	suggested_recipes = lp_func['suggested_recipes']
	total_nutrients_taken = lp_func['total_nutrients_taken']
	diet_recipes = lp.get_lp_output(suggested_recipes)

	print (total_raw_calories,total_raw_carbs,total_raw_protein,total_raw_fat)

	return jsonify({'user_info' : {'age':age, 'weight' : weight, 'height' : height, 'gender' : gender, 'exercise_level' : exercise_level,
	'cuisine' : cuisine, 'diet' : diet, 'intolerances' : intolerances, 'obj' : obj, 'obj_nut' : obj_nut, 'recipe_types' : recipe_types},
	'user_daily_nutrients' : user_daily_nutrients, 'recipes' : diet_recipes, 'total_nutrients_taken' : total_nutrients_taken, 'raw_foods' : raw_foods})

# @app.route('/recresults', methods=['GET'])
# @cross_origin()
# def recompute_usr_input():
#	 data = []
#	 for i in range(2):
#		 # data.append(random.choice(USDAfoods.query.all()))
#		 data.append(random.choice(USDAfoods.query.filter(USDAfoods.Group_Name.like('Vegetables and Vegetable Products')).all()))
#	 print "********"
#	 print type(data)
#	 print "********"
#	 raw_foods_temp = {'raw': [d.__dict__ for d in data]}
#	 # print [type(d) for d in data]
	
#	 raw_foods = []
#	 for d in data:
#		 dct = {
#			 "NDB_No": d.NDB_No, 
#			 "Desc": d.Desc, 
#			 "Cal": d.Cal, 
#			 "Prot": d.Prot, 
#			 "Fat": d.Fat, 
#			 "Carb": d.Carb, 
#			 "Group_Code": d.Group_Code, 
#			 "Group_Name": d.Group_Name
#		 }
#		 raw_foods.append(dct)

#	 total_raw_calories = sum(item['Cal'] for item in raw_foods_temp['raw'])
#	 total_raw_carbs = sum(item['Carb'] for item in raw_foods_temp['raw'])
#	 total_raw_protein = sum(item['Prot'] for item in raw_foods_temp['raw'])
#	 total_raw_fat = sum(item['Fat'] for item in raw_foods_temp['raw'])
#	 # print total_raw_fat
#	 # print total_raw_protein
#	 # print total_raw_carbs
#	 print raw_foods

#	 age = session.get('age')
#	 height = session.get('height')
#	 weight = session.get('weight')
#	 gender = session.get('gender')
#	 exercise_level = session.get('exercise_level')
#	 cuisine = session.get('cuisine')
#	 diet = session.get('diet')
#	 intolerances = session.get('intolerances')
#	 recipe_types = session.get('recipe_types')
#	 obj = session.get('obj')
#	 obj_nut = session.get('obj_nut')

#	 user = User(age, weight, height, gender, exercise_level)

#	 cuisine_q = request.args.getlist('cuisine')
#	 diet_q = request.args.get('diet')
#	 intolerances_q = request.args.getlist('intolerances')
#	 recipe_types_q = request.args.getlist('recipeTypes')
#	 obj_q = request.args.get('obj')
#	 obj_nut_q = request.args.get('objNut')
#	 carb_low = request.args.get('carbLow')
#	 carb_up = request.args.get('carbUp')
#	 prot_low = request.args.get('protLow')
#	 prot_up = request.args.get('protUp')
#	 fat_low = request.args.get('fatLow')
#	 fat_up = request.args.get('fatUp')
#	 cal_low = request.args.get('calLow')
#	 cal_up = request.args.get('calUp')

#	 if len(cuisine_q) > 0:
#		 cuisine = cuisine_q
#	 if diet_q != '':
#		 diet = diet_q
#	 if len(intolerances_q) > 0:
#		 intolerances = intolerances_q
#	 if len(recipe_types_q)  > 0:
#		 print '****RECIPETYPES'
#		 recipe_types = recipe_types_q
#	 if obj_q != '':
#		 obj = obj_q
#	 if obj_nut_q != '':
#		 obj_nut = obj_nut_q

#	 if carb_low != '':
#		 user.daily_nutrients['carb_low'] = float(carb_low)
#	 if carb_up != '':
#		 user.daily_nutrients['carb_up'] = float(carb_up)
#	 if prot_low != '':
#		 user.daily_nutrients['prot_low'] = float(prot_low)
#	 if prot_up != '':
#		 user.daily_nutrients['prot_up'] = float(prot_up)
#	 if fat_low != '':
#		 user.daily_nutrients['fat_low'] = float(fat_low)
#	 if fat_up != '':
#		 user.daily_nutrients['fat_up'] = float(fat_up)
#	 if cal_low != '':
#		 user.daily_nutrients['cal_low'] = float(cal_low)
#	 if cal_up != '':
#		 user.daily_nutrients['cal_up'] = float(cal_up)

#	 req = RecipeHandler(user.daily_nutrients, cuisine, diet, intolerances, "", recipe_types)

#	 ress = req.get_recipes()

#	 lp = LinearProgrammingSolver(obj, obj_nut, ress['dict_prot'], ress['dict_fat'], ress['dict_cal'], ress['dict_carb'], ress['dict_title'], ress['dict_price'], ress['dict_time'], ress['recipe_types'], user.daily_nutrients)

#	 lp_func = lp.func_lp()

#	 suggested_recipes = lp_func['suggested_recipes']
#	 total_nutrients_taken = lp_func['total_nutrients_taken']
#	 diet_recipes = lp.get_lp_output(suggested_recipes)

#	 return render_template('recresults.html', response={'user_info' : {'age':age, 'weight' : weight, 'height' : height, 'gender' : gender, 'exercise_level' : exercise_level,
#	 'cuisine' : cuisine, 'diet' : diet, 'intolerances' : intolerances, 'obj' : obj, 'obj_nut' : obj_nut, 'recipe_types' : recipe_types},
#	 'user_daily_nutrients' : user.daily_nutrients, 'recipes' : diet_recipes, 'total_nutrients_taken' : total_nutrients_taken, 'raw_foods' : raw_foods})

@app.route('/newform', methods=['GET'])
@cross_origin()
def new_form():
	age = session.get('age')
	height = session.get('height')
	weight = session.get('weight')
	gender = session.get('gender')
	exercise_level = session.get('exercise_level')
	cuisine = session.get('cuisine')
	diet = session.get('diet')
	intolerances = session.get('intolerances')
	recipe_types = session.get('recipe_types')
	obj = session.get('obj')
	obj_nut = session.get('obj_nut')

	user = User(age, weight, height, gender, exercise_level)

	user_daily_nutrients = user.daily_nutrients

	carb_low = user_daily_nutrients['carb_low']
	carb_up = user_daily_nutrients['carb_up']
	prot_low = user_daily_nutrients['prot_low']
	prot_up = user_daily_nutrients['prot_up']
	fat_low = user_daily_nutrients['fat_low']
	fat_up = user_daily_nutrients['fat_up']
	cal_low = user_daily_nutrients['cal_low']
	cal_up = user_daily_nutrients['cal_up']

	cuisine_dictionary = {
	'' : 'All',
	'african' : 'African',
	'chinese' : 'Chinese',
	'japanese' : 'Japanese',
	'korean' : 'Korean',
	'vietnamese' : 'Vietnamese',
	'thai' : 'Thai',
	'indian' : 'Indian',
	'british' : 'British',
	'irish' : 'Irish',
	'french' : 'French',
	'italian' : 'Italian',
	'mexican' : 'Mexican',
	'spanish' : 'Spanish',
	'middle+eastern' : 'Middle Eastern',
	'jewish' : 'Jewish',
	'american' : 'American',
	'cajun' : 'Cajun',
	'southern' : 'Southern',
	'greek' : 'Greek',
	'german' : 'German',
	'nordic' : 'Nordic',
	'eastern+european' : 'Eastern european',
	'caribbean' : 'Caribbean',
	'latin+american' : 'Latin American'
	}

	diet_dictionary = {
	'' : 'None',
	'pescetarian' : 'Pescetarian',
	'lacto+vegetarian' : 'Lacto vegetarian',
	'ovo+vegetarian' : 'Ovo vegetarian',
	'vegan' : 'Vegan',
	'paleo' : 'Paleo',
	'primal' : 'Primal',
	'vegetarian' : 'Vegetarian'
	}

	intolerances_dictionary = {
	'' : 'None',
	'dairy' : 'Dairy',
	'egg' : 'Egg',
	'gluten' : 'Gluten',
	'peanut' : 'Peanut',
	'sesame' : 'Sesame',
	'seafood' : 'Seafood',
	'shellfish' : 'Shellfish',
	'soy' : 'Soy',
	'sulfite' : 'Sulfite',
	'tree+nut' : 'Tree Nut',
	'wheat' : 'Wheat'
	}

	obj_nut_list = [
	'Calories',
	'Protein',
	'Carbs',
	'Fat',
	'Price',
	'Time'
	]

	obj_list = [
	'Max',
	'Min'
	]

	recipe_types_dictionary={
	'main+course' : 'Main Course',
	'side+dish' : 'Side Dish',
	'dessert' : 'Dessert',
	'appetizer' : 'Appetizer',
	'salad' : 'Salad',
	'bread' : 'Bread',
	'breakfast' : 'Breakfast',
	'soup' : 'Soup',
	'beverage' : 'Beverage',
	# 'sauce' : 'Sauce',
	# 'drink' : 'Drink'
	}

	return render_template('newform.html', response={
	'carb_low' : carb_low,
	'carb_up' : carb_up,
	'prot_low' : prot_low,
	'prot_up' : prot_up,
	'fat_low' : fat_low,
	'fat_up' : fat_up,
	'cal_low' : cal_low,
	'cal_up' : cal_up,
	'cuisine_dictionary' : cuisine_dictionary,
	'diet_dictionary' : diet_dictionary,
	'intolerances_dictionary' : intolerances_dictionary,
	'recipe_types_dictionary' : recipe_types_dictionary,
	'obj_nut_list' : obj_nut_list,
	'obj_list' : obj_list,
	'cuisine' : cuisine,
	'diet' : diet,
	'intolerances' : intolerances,
	'recipe_types' : recipe_types,
	'obj' : obj,
	'obj_nut' : obj_nut
	})
>>>>>>> 3d29df7e1e9b3a0c9a7fb3c374995aedfbb1c424
