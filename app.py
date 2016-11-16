#!flask/bin/python
from flask import *
from flask_restful import *
from diet_optimizer import *
from flask.ext.cors import CORS, cross_origin
from flask_bootstrap import Bootstrap
import settings

app = Flask(__name__)
Bootstrap(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = settings.APP_KEY


@app.route('/', methods=['GET'])
@cross_origin()
def user_form():
    return render_template('form.html')

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
    return render_template('newform.html')

if __name__ == '__main__':
    # app.run(threaded=True, debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True, debug=True, host='0.0.0.0', port=port)
