from .user import create_user
from App.database import db
from App.controllers import *
from App.controllers.listing import create_listing
from App.controllers.review import create_review



def initialize():
    db.drop_all()
    db.create_all()
    
    # Create test users
    admin = create_user("admin", "adminpass", "landlord")
    tenant1 = create_user("tenant1", "tenantpass", "tenant")
    tenant2 = create_user("tenant2", "tenantpass", "tenant")
    
    # Create test listings
    listing1 = create_listing("Beautiful Apartment", "Great location", 0, 1, "$100", "Penal")  # Assuming owner_id=1
    
    # Create test reviews - ADD THE RATING PARAMETER
    create_review(1, 1, 'Great place!', 5)  # listing_id=1, tenant_id=1, text, rating=5
    create_review(1, 2, 'Nice view!', 4)    # listing_id=1, tenant_id=2, text, rating=4
    
    return [admin, tenant1, tenant2, listing1]