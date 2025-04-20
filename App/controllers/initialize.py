from .user import create_user
from App.database import db
from App.controllers import *
from App.controllers.listing import create_listing
from App.controllers.review import *



def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', 'tenant', True) #is_verified is set to False by default but bob is set to true 
    create_user('brad', 'bradpass', 'landlord') #is_verified doesnt matter for landlords
    create_listing(2, 'Apartment 1', 1, 1, 1000, 'New York', 'images/apartment1.jpg', 'Nice') #create listing for brad
    create_listing(2, 'Apartment 2', 1, 1, 1000, 'New York', 'images/apartment1.jpg', 'Nice')
    create_review(1, 1, 'Great place!', 5) #create review for listing 1 by tenant 1
    create_review(1, 1, 'Nice place!', 4) #create review for listing 1 by tenant 2
     #create review for listing 1 by tenant 2
