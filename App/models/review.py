from App.database import db
from App.models import User, Listing  # Make sure Listing model exists and is imported

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    text = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    tenant = db.relationship('User', backref='reviews')
    listing = db.relationship('Listing', backref='reviews')

    def __init__(self, tenant_id, listing_id, text, rating):
        self.tenant_id = tenant_id
        self.listing_id = listing_id
        self.text = text
        self.rating = rating

    def get_json(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'listing_id': self.listing_id,
            'text': self.text,
            'rating': self.rating,
            'tenant_username': self.tenant.username if self.tenant else None
        }

    def __repr__(self):
        return f"<Review {self.id} - Tenant {self.tenant_id} - {self.rating}⭐>"
