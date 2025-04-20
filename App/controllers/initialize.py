from .user import create_user
from App.database import db



def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', 'tenant', True) #is_verified is set to False by default but bob is set to true 
    create_user('brad', 'bradpass', 'landlord')
