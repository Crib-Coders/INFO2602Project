from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_db():
    # This will create all tables based on the models
    db.create_all()

def init_db(app):
    db.init_app(app)
