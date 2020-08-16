from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# Initialise app
app = Flask(__name__)

api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# This is to avoid circular imports
from App import models
from App import create_table
from App import resources