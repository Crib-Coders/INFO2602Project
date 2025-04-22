from App.models import *
from App.models import Listing
from App.database import db
from App.controllers import *

def create_listing(user_id, title, bedrooms, bathrooms, price, location, image, description=None):
    """Create a new apartment listing"""
    temp = User.query.filter_by(id=user_id).first()
    if not temp:
        db.session.rollback()
        print(" User not found")
        return None
    if temp.role != 'tenant':
        new_listing = Listing(
            landlord_id=user_id,
            title=title,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            price=price,
            location=location,
            image=image,
            description=description  # Initialize description
        )
        db.session.add(new_listing)
        db.session.commit()
        return new_listing
    else:
        db.session.rollback()
        print(" Tenant is not authorized to create a listing")
        return None

def get_listing(id):
    """Get a single listing by ID"""
    return Listing.query.get(id)

def get_all_listings():
    """Get all apartment listings"""
    return Listing.query.all()

def get_all_public_listings():
    return Listing.query.all()

def get_all_listings_json():
    """Get all listings in JSON format"""
    listings = Listing.query.all()
    if not listings:
        return []
    return [listing.get_json() for listing in listings]

def update_listing(id, title=None, bedrooms=None, bathrooms=None, price=None, location=None, image=None):
    """Update listing details"""
    listing = get_listing(id)
    if listing:
        if title: listing.title = title
        if bedrooms: listing.bedrooms = bedrooms
        if bathrooms: listing.bathrooms = bathrooms
        if price: listing.price = price
        if location: listing.location = location
        if image: listing.image = image
        db.session.add(listing)
        db.session.commit()
        return listing
    return None

def delete_listing(id):
    """Delete a listing"""
    listing = get_listing(id)
    if listing:
        db.session.delete(listing)
        db.session.commit()
        return True
    return False

def search_listings(location=None, min_price=None, max_price=None, bedrooms=None, bathrooms=None):
    """Search listings with filters"""
    query = Listing.query
    
    if location:
        query = query.filter(Listing.location.ilike(f'%{location}%'))
    if min_price:
        query = query.filter(Listing.price >= min_price)
    if max_price:
        query = query.filter(Listing.price <= max_price)
    if bedrooms:
        query = query.filter(Listing.bedrooms >= bedrooms)
    if bathrooms:
        query = query.filter(Listing.bathrooms >= bathrooms)
    
    return query.all()




#Listing Test

def test_listings():
    # Create test landlord - use the auth controller's register function
    from App.controllers.auth import register
    
    print("Creating test landlord...")
    landlord, error = register('testlandlord1', 'landlordpass', 'landlord1')
    if not landlord:
        print(f"✗ Failed to create landlord: {error}")
        return
    
    print(f"✓ Created landlord: {landlord.username} (ID: {landlord.id})")
    
    # Test create listing
    print("Testing create listing...")
    listing = create_listing(
        user_id=landlord.id,
        title="Test Listing",
        bedrooms=2,
        bathrooms=1,
        price=1500,
        location="Kingston",
        image="test.jpg"
    )
    
    if not listing:
        print("✗ Failed to create listing")
        return
    
    print(f"✓ Created listing: {listing.title} (ID: {listing.id})")
    
    # Test get all listings
    print("Testing get all listings...")
    listings = get_all_listings()
    if not listings:
        print("✗ No listings found")
        return
    
    print(f"✓ Found {len(listings)} listings")
    for l in listings:
        print(f"  - {l.title} (ID: {l.id})")