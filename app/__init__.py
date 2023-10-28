from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.database.config import config
import os
from dotenv import load_dotenv

load_dotenv(".env")

app = Flask(__name__)
params = config()
try:
    uri = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
except:
    print("fatal error. Unable to connect to database.")
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.jwt_signing_key = os.environ["JWT_KEY"]

db = SQLAlchemy(app)

from app import routes