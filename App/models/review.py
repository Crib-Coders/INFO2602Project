from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models import User

class Review(db.Model):
    __tablename__ = 'review'


    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Changed from user_id to tenant_id    
    #user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)  # Added foreign key for listing
    text = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Added rating column
    #username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)  # Added username column

    # Relationships (corrected)
    tenant = db.relationship('User', backref='reviews')
    #user = db.relationship('User', back_populates='reviews')
#    listing = db.relationship('Listing', back_populates='reviews')

def __init__(self, tenant_id, listing_id, text):
    self.tenant_id = tenant_id
    self.listing_id = listing_id
    self.text = text

def _repr_(self):
    return f'<Review {self.text}>'

def get_json(self):
    return {
        'id': self.id,
        'user_id': self.user_id,
        'text': self.text,
        'user': self.user.get_json()
    }

def get_username(self, tenant_id):
    """Get the username of the tenant who wrote the review."""
    user = User.query.get(tenant_id)
    if user:
        return user.username
    return None
