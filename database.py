import os
import json
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ["DATABASE_URL"]
"""
TODO: uncomment to test locally
database_path = "postgres://postgres:passwd123@localhost:5432/dungeon"
also:
create database dungeon on postgresql database
    and uncomment db.create_all()
"""

db = SQLAlchemy()


"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()
