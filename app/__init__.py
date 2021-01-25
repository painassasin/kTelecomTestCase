from flask import Flask
from config import Config

# Creating the application
app = Flask(__name__)
app.config.from_object(Config)

# Import views
from app import views
