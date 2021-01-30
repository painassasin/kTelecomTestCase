from flask import Flask
from config import Config
from flask_wtf.csrf import CSRFProtect

# Creating the application
app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)

# Import views
from app import views
