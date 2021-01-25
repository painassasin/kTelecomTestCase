from dotenv import load_dotenv
import os

load_dotenv('.env')


class Config(object):

    # "Cross-site Request Forgery (CSRF) protection"
    CSRF_ENABLED = True

    # Secret key for data signature
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Database credentials
    DB_CREDENTIALS = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': 'K-Telecom',
    }
