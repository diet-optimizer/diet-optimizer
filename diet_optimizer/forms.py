from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, RadioField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import *


def validate_intolerences(form, field):
    for value in field.data:
        if value == 'None':
            if len(field.data) > 1:
                raise ValidationError('You can''t select ''None'' and other intolerences.')

# def validate_password(form,field,user):
#     if field.data is not user.password:
#         raise ValidationError('Please enter your current password.')
def validate_nickname(form,field):
    field.Validators=[ValidationError(message='Please enter new username.')]



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

class PasswordResetRequestForm(Form):
     email = StringField('Email', validators=[DataRequired("Please enter your email address."),Email("Please enter you email address.")])
     submit = SubmitField('Reset Password')

class PasswordResetForm(Form):
     email = StringField('Email', validators=[DataRequired("Please enter your email address."),Email("Please enter you email address.")])
     password = PasswordField('New Password', validators=[DataRequired("Please enter your password."), Length(min=6, message="Password must be 6 characters or more."), EqualTo('password2', message='Passwords must match')])
     password2 = PasswordField('Confirm password', validators=[DataRequired("Please enter your password."), Length(min=6, message="Password must be 6 characters or more.")])
     submit = SubmitField('Reset Password')

     def validate_email(self, field):
         if UserDB.query.filter_by(email=field.data).first() is None:
             raise ValidationError('Unknown email address.')

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
                         validators=[DataRequired("Please select your gender.")], default='Female')
    intolerences = SelectMultipleField('Do you have any intolerences?',choices=[('None','None'), ('Dairy', 'Dairy'), ('Egg', 'Egg'),('Gluten', 'Gluten'), ('Peanut', 'Peanut'), ('Sesame', 'Sesame'),('Seafood', 'Seafood'), ('Shellfish', 'Shellfish'), ('Soy', 'Soy'),('Sulfite', 'Sulfite'), ('Tree Nut', 'Tree Nut'), ('Wheat', 'Wheat')],validators=[DataRequired("Please select an intolerence."), validate_intolerences], default='None')

    submit = SubmitField('Update')

class AccountSettingsForm(Form):
    #current_password = PasswordField('Current password', validators=[DataRequired("Please enter your current password."),EqualTo('password', message='Passwords must match.')])
    new_password = PasswordField('New password', validators=[DataRequired("Please enter a new password."),Length(min=6, message="Password must be 6 characters or more.")])
    new_password2 = PasswordField('Confirm new password', validators=[DataRequired("Please confirm your password"),EqualTo('new_password', message='Passwords must match.')])
    submit = SubmitField('Update')