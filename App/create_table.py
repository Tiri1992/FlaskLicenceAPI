"""
Run this once in order to create table DriverModel on DB.
"""
from App import db

db.create_all()
