"""
Run this once in order to create table DriverModel on DB.
"""
from app import db

db.create_all()
