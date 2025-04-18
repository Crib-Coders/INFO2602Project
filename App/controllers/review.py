from App.models import Review
from App.database import db

def create_review(user_id, listing_id, text):
    """Create a new review for an apartment"""
    new_review = Review(
        user_id=user_id,
        listing_id=listing_id,
        text=text
    )
    db.session.add(new_review)
    db.session.commit()
    return new_review

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