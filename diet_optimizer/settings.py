# settings.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import smtplib

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# settings.py

SPOONACULAR_KEY = os.environ.get("SPOONACULAR_KEY")
APP_KEY = os.environ.get("APP_KEY")
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
DIET_OPTIMIZER_ADMIN = os.environ.get('DIET_OPTIMIZER_ADMIN')
DIET_OPTIMIZER_MAIL_SUBJECT_PREFIX = os.environ.get('[DIET-OPTIMIZER]')
MAIL_SERVER = smtplib.SMTP("smtp.gmail.com", 587, None, 30)
MAIL_PORT = 587


