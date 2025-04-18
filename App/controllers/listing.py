from App.models import Listing
from App.database import db

def create_listing(user_id, title, bedrooms, bathrooms, price, location, image):
    """Create a new apartment listing"""
    new_listing = Listing(
        user_id=user_id,
        title=title,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        price=price,
        location=location,
        image=image
    )
    db.session.add(new_listing)
    db.session.commit()
    return new_listing

def get_listing(id):
    """Get a single listing by ID"""
    return Listing.query.get(id)

def get_all_listings():
    """Get all apartment listings"""
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

def search_listings(location=None, min_price=None, max_price=None, bedrooms=None):
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
    
    return query.all()