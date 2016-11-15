#!flask/bin/python
from flask import *
from flask_restful import *
from diet_optimizer import *
from flask.ext.cors import CORS, cross_origin
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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


    # if cuisine != None:
    #     cuisine = cuisine.split(',')
    # if recipe_types != None:
    #     recipe_types = recipe_types.split(',')
    # if intolerances != None:
    #     intolerances = intolerances.split(',')
    # if exclude_ingredients != None:
    #     exclude_ingredients = exclude_ingredients.split(',')

    user = User(age, weight, height, gender, exercise_level)

    user_daily_nutrients = user.daily_nutrients
    
    print "*****USER DAILY NUTRIENTS"
    # print user_daily_nutrients

    # session['cuisine'] = cuisine
    # session['diet'] = diet
    # session['intolerances'] = intolerances
    # session['recipe_types'] = recipe_types
    # session['obj'] = obj
    # session['obj_nut'] = obj_nut

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
    print "*****USER DAILY NUTRIENTS"
    print user_daily_nutrients

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

@app.route('/recompute', methods=['GET'])
@cross_origin()
def recompute_usr_input():
    cuisine = request.args.getlist('cuisine')
    diet = request.args.get('diet')
    intolerances = request.args.getlist('intolerances')
    recipe_types = request.args.getlist('recipeTypes')
    obj = request.args.get('obj')
    obj_nut = request.args.get('objNut')
    carb_low = float(request.args.get('carbLow'))
    carb_up = float(request.args.get('carbUp'))
    prot_low = float(request.args.get('protLow'))
    prot_up = float(request.args.get('protUp'))
    fat_low = float(request.args.get('fatLow'))
    fat_up = float(request.args.get('fatUp'))
    cal_low = float(request.args.get('calLow'))
    cal_up = float(request.args.get('calUp'))


    user_daily_nutrients = user.daily_nutrients

    if carb_low != None:
        user_daily_nutrients['carb_low'] = carb_low
    if carb_up != None:
        user_daily_nutrients['carb_up'] = carb_up
    if prot_low != None:
        user_daily_nutrients['prot_low'] = prot_low
    if prot_up != None:
        user_daily_nutrients['prot_up'] = prot_up
    if fat_low != None:
        user_daily_nutrients['fat_low'] = fat_low
    if fat_up != None:
        user_daily_nutrients['fat_up'] = fat_up
    if cal_low != None:
        user_daily_nutrients['cal_low'] = cal_low
    if cal_up != None:
        user_daily_nutrients['cal_up'] = cal_up

    session['user'] = user

    print "*****USER"
    print user

    print "*****USER DAILY NUTRIENTS"
    print user_daily_nutrients


if __name__ == '__main__':
    # app.run(threaded=True, debug=True)
    port = int(os.environ.get("PORT", 55214))
    app.run(threaded=True, debug=True, host='0.0.0.0', port=port)
