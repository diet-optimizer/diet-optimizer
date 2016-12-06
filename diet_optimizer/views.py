from diet_optimizer import *
from forms import SignupForm, LoginForm


@app.route('/', methods=['GET'])
@cross_origin()
def index():
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
            newuser = UserDB(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('home')) 
            #url_for needs the function inside the route

    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
@cross_origin()
def login():
    if 'email' in session:
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('login.html', form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = UserDB.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home')) 
            else:
                return redirect(url_for('login')) 

    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/logout', methods=['GET','POST'])
@cross_origin()
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    return render_template("home.html")

@app.route('/results', methods=['GET'])
@cross_origin()
def get_usr_input():

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

    user_daily_nutrients = user.daily_nutrients

    session['carb_low'] = user_daily_nutrients['carb_low']
    session['carb_up'] = user_daily_nutrients['carb_up']
    session['prot_low'] = user_daily_nutrients['prot_low']
    session['prot_up'] = user_daily_nutrients['prot_up']
    session['fat_low'] = user_daily_nutrients['fat_low']
    session['fat_up'] = user_daily_nutrients['fat_up']
    session['cal_low'] = user_daily_nutrients['cal_low']
    session['cal_up'] = user_daily_nutrients['cal_up']

    req = RecipeHandler(user.daily_nutrients, cuisine, diet, intolerances, "", recipe_types)

    res = req.get_recipes()

    lp = LinearProgrammingSolver(obj, obj_nut, res['dict_prot'], res['dict_fat'], res['dict_cal'], res['dict_carb'], res['dict_title'], res['recipe_types'], user.daily_nutrients)

    lp_func = lp.func_lp()

    suggested_recipes = lp_func['suggested_recipes']
    total_nutrients_taken = lp_func['total_nutrients_taken']
    diet_recipes = lp.get_lp_output(suggested_recipes)

    return render_template('results.html', response={'user_info' : {'age':age, 'weight' : weight, 'height' : height, 'gender' : gender, 'exercise_level' : exercise_level,
    'cuisine' : cuisine, 'diet' : diet, 'intolerances' : intolerances, 'recipe_types' : recipe_types},
    'user_daily_nutrients' : user_daily_nutrients, 'recipes' : diet_recipes, 'total_nutrients_taken' : total_nutrients_taken})

@app.route('/apiresults', methods=['GET'])
@cross_origin()
def get_usr_input_api():

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

    req = RecipeHandler(user.daily_nutrients, cuisine, diet, intolerances, "", recipe_types)

    res = req.get_recipes()

    lp = LinearProgrammingSolver(obj, obj_nut, res['dict_prot'], res['dict_fat'], res['dict_cal'], res['dict_carb'], res['dict_title'], res['recipe_types'], user.daily_nutrients)

    lp_func = lp.func_lp()

    suggested_recipes = lp_func['suggested_recipes']
    total_nutrients_taken = lp_func['total_nutrients_taken']
    diet_recipes = lp.get_lp_output(suggested_recipes)

    return jsonify({'user_info' : {'age':age, 'weight' : weight, 'height' : height, 'gender' : gender, 'exercise_level' : exercise_level,
    'cuisine' : cuisine, 'diet' : diet, 'intolerances' : intolerances, 'recipe_types' : recipe_types},
    'user_daily_nutrients' : user_daily_nutrients, 'recipes' : diet_recipes, 'total_nutrients_taken' : total_nutrients_taken})

@app.route('/recresults', methods=['GET'])
@cross_origin()
def recompute_usr_input():

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

    cuisine_q = request.args.getlist('cuisine')
    diet_q = request.args.get('diet')
    intolerances_q = request.args.getlist('intolerances')
    recipe_types_q = request.args.getlist('recipeTypes')
    obj_q = request.args.get('obj')
    obj_nut_q = request.args.get('objNut')
    carb_low = request.args.get('carbLow')
    carb_up = request.args.get('carbUp')
    prot_low = request.args.get('protLow')
    prot_up = request.args.get('protUp')
    fat_low = request.args.get('fatLow')
    fat_up = request.args.get('fatUp')
    cal_low = request.args.get('calLow')
    cal_up = request.args.get('calUp')

    if len(cuisine_q) > 0:
        cuisine = cuisine_q
    if diet_q != '':
        diet = diet_q
    if len(intolerances_q) > 0:
        intolerances = intolerances_q
    if len(recipe_types_q)  > 0:
        print '****RECIPETYPES'
        recipe_types = recipe_types_q
    if obj_q != '':
        obj = obj_q
    if obj_nut_q != '':
        obj_nut = obj_nut_q

    if carb_low != '':
        user.daily_nutrients['carb_low'] = float(carb_low)
    if carb_up != '':
        user.daily_nutrients['carb_up'] = float(carb_up)
    if prot_low != '':
        user.daily_nutrients['prot_low'] = float(prot_low)
    if prot_up != '':
        user.daily_nutrients['prot_up'] = float(prot_up)
    if fat_low != '':
        user.daily_nutrients['fat_low'] = float(fat_low)
    if fat_up != '':
        user.daily_nutrients['fat_up'] = float(fat_up)
    if cal_low != '':
        user.daily_nutrients['cal_low'] = float(cal_low)
    if cal_up != '':
        user.daily_nutrients['cal_up'] = float(cal_up)

    req = RecipeHandler(user.daily_nutrients, cuisine, diet, intolerances, "", recipe_types)

    ress = req.get_recipes()

    lp = LinearProgrammingSolver(obj, obj_nut, ress['dict_prot'], ress['dict_fat'], ress['dict_cal'], ress['dict_carb'], ress['dict_title'], ress['recipe_types'], user.daily_nutrients)

    lp_func = lp.func_lp()

    suggested_recipes = lp_func['suggested_recipes']
    total_nutrients_taken = lp_func['total_nutrients_taken']
    diet_recipes = lp.get_lp_output(suggested_recipes)

    return render_template('recresults.html', response={'user_info' : {'age':age, 'weight' : weight, 'height' : height, 'gender' : gender, 'exercise_level' : exercise_level,
    'cuisine' : cuisine, 'diet' : diet, 'intolerances' : intolerances, 'recipe_types' : recipe_types},
    'user_daily_nutrients' : user.daily_nutrients, 'recipes' : diet_recipes, 'total_nutrients_taken' : total_nutrients_taken})

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
    'none' : 'All',
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
    'none' : 'None',
    'pescetarian' : 'Pescetarian',
    'lacto+vegetarian' : 'Lacto vegetarian',
    'ovo+vegetarian' : 'Ovo vegetarian',
    'vegan' : 'Vegan',
    'paleo' : 'Paleo',
    'primal' : 'Primal',
    'vegetarian' : 'Vegetarian'
    }

    intolerances_dictionary = {
    'none' : 'None',
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
    'Fat'
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