from App.models import Review
from App.database import db
from App.models import *
from App.controllers import *
from App.controllers.listing import get_all_listings


def create_review(user_id, listing_id, text, rating=None):
    temp = User.query.filter_by(id=user_id).first()
    if not temp:
        db.session.rollback()
        print(" User not found")
    if temp.role != 'landlord':
        
        """Create a new review for an apartment"""
        new_review = Review(
            tenant_id=user_id,
            listing_id=listing_id,
            text=text,
            rating=rating
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review
    else:
        db.session.rollback()
        print(" Landlord is not authorized to create a review")
        return None

def get_review(id):
    """Get a single review by ID"""
    return Review.query.get(id)

def get_all_reviews():
    """Get all reviews"""
    return Review.query.all()

def get_all_reviews_json():
    """Get all reviews in JSON format"""
    reviews = Review.query.all()
    if not reviews:
        return []
    return [review.get_json() for review in reviews]

def get_reviews_for_listing(listing_id):
    """Get all reviews for a specific listing"""
    return Review.query.filter_by(listing_id=listing_id).all()

def update_review(id, text=None):
    """Update review text"""
    review = get_review(id)
    if review:
        if text: review.text = text
        db.session.add(review)
        db.session.commit()
        return review
    return None

def delete_review(id):
    """Delete a review"""
    review = get_review(id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    return False



#Review Controller Tests

def test_reviews():
    # Create test tenant
    tenant, _ = register('testtenant', 'tenantpass', 'tenant')
    
    # Get first listing
    listing = get_all_listings()[0]
    if not listing:
        print("No listings available for testing.")
        return False
    
    # Test create review
    print("Testing create review...")
    review = create_review(
        user_id=tenant.id,
        listing_id=listing.id,
        text="Great apartment!"
    )
    assert review is not None, "Create review failed"
    print(f"✓ Created review: {review.text}")
    
    # Test get reviews for listing
    print("Testing get reviews for listing...")
    reviews = get_reviews_for_listing(listing.id)
    assert len(reviews) > 0, "No reviews found"
    print(f"✓ Found {len(reviews)} reviews")