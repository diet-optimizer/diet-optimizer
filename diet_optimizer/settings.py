# settings.py
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# settings.py

SPOONACULAR_KEY = os.environ.get("SPOONACULAR_KEY")
APP_KEY = os.environ.get("APP_KEY")

