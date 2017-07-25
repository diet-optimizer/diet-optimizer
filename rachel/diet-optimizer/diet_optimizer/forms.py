from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, RadioField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import db
#from views import *

def validate_intolerences(form, field):
    for value in field.data:
        if value == 'None':
            if len(field.data) > 1:
                raise ValidationError('You can''t select ''None'' and other intolerences.')


class SignupForm(Form):
    nick_name = StringField('User name', validators=[DataRequired("Please enter a unique user name.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter you email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter your password."), Length(min=6, message="Password must be 6 characters or more.")])
    password2 = PasswordField('Confirm password', validators=[DataRequired("Please confirm your password"),EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Next')


class PersonalDetailsForm(Form) :
    first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
    last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
    height = IntegerField('Height', validators=[DataRequired("Please enter your height.")])
    weight = IntegerField('Weight', validators=[DataRequired("Please enter your weight.")])
    birth_date = DateField('Birth date', validators=[DataRequired("Please enter your birth date.")], format = '%m-%d-%Y')
    activity_level = SelectField('Activity level', choices=[('Sedentary', 'Sedentary'), ('Low Active', 'Low Active'),('Active', 'Active'), ('Very Active', 'Very Active')],validators=[DataRequired("Please select your activity level.")], default='Sedentary')
    diet = SelectField('Which diet are you following?', choices=[('None','None'),('pescetarian','Pescetarian'), ('Lacto Vegetarian','Lacto Vegetarian'), ('Ovo Vegetarian', 'Ovo Vegetarian'), ('Vegan', 'Vegan'), ('Paleo','Paleo'), ('Primal','Primal'), ('Vegetarian', 'Vegetarian')], validators=[DataRequired("Please select a diet.")], default='None')
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')],validators=[DataRequired("Please select your gender.")], default='Male')
    intolerences = SelectMultipleField('Do you have any intolerences?', choices=[('None','None'),('Dairy','Dairy'), ('Egg','Egg'), ('Gluten', 'Gluten'), ('Peanut', 'Peanut'), ('Sesame','Sesame'), ('Seafood','Seafood'), ('Shellfish', 'Shellfish'), ('Soy','Soy'),('Sulfite','Sulfite'),('Tree Nut','Tree Nut'),('Wheat','Wheat')], validators=[DataRequired("Please select an intolerence."), validate_intolerences], default='None')
    submit = SubmitField('Sign up')


class LoginForm(Form):
	# email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter you email address.")])
	nick_name = StringField('User name', validators=[DataRequired("Please enter your user name.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
	submit = SubmitField("Sign In")

class SettingsForm(Form):

    height = IntegerField('Height', validators=[DataRequired("Please enter your height.")])
    weight = IntegerField('Weight', validators=[DataRequired("Please enter your weight.")])
    birth_date = DateField('Birth date', validators=[DataRequired("Please enter your birth date.")])
    activity_level = SelectField('Activity level', choices=[('Sedentary', 'Sedentary'), ('Low Active', 'Low Active'),
                                                            ('Active', 'Active'), ('Very Active', 'Very Active')],
                                 validators=[DataRequired("Please select your activity level.")], default='Sedentary')
    diet = SelectField('Which diet are you following?', choices=[('None', 'None'), ('pescetarian', 'Pescetarian'),
                                                                 ('Lacto Vegetarian', 'Lacto Vegetarian'),
                                                                 ('Ovo Vegetarian', 'Ovo Vegetarian'),
                                                                 ('Vegan', 'Vegan'), ('Paleo', 'Paleo'),
                                                                 ('Primal', 'Primal'), ('Vegetarian', 'Vegetarian')],
                       validators=[DataRequired("Please select a diet.")], default='None')
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')],
                         validators=[DataRequired("Please select your gender.")], default='Male')
    intolerences = SelectMultipleField('Do you have any intolerences?',choices=[('None','None'), ('Dairy', 'Dairy'), ('Egg', 'Egg'),('Gluten', 'Gluten'), ('Peanut', 'Peanut'), ('Sesame', 'Sesame'),('Seafood', 'Seafood'), ('Shellfish', 'Shellfish'), ('Soy', 'Soy'),('Sulfite', 'Sulfite'), ('Tree Nut', 'Tree Nut'), ('Wheat', 'Wheat')],validators=[DataRequired("Please select an intolerence."), validate_intolerences], default='None')

    submit = SubmitField('Update')

class FeedbackForm(Form) :
    recipe = SelectField('recipe')
    mark = SelectField('mark',choices=[('1',u"\u2605"),('2',u"\u2605"u"\u2605"),('3',u"\u2605"u"\u2605"u"\u2605"),('4',u"\u2605"u"\u2605"u"\u2605"u"\u2605"),('5',u"\u2605"u"\u2605"u"\u2605"u"\u2605"u"\u2605")])
    submit = SubmitField('Submit')