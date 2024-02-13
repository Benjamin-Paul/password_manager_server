from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.database.config import config

app = Flask(__name__)
params = config()
try:
    uri = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
except:
    print("fatal error. Unable to connect to database.")
app.config['SQLALCHEMY_DATABASE_URI'] = uri

db = SQLAlchemy(app)

from app import routes