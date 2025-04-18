from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Listing(db.Model):
    __tablename__ = 'listing'


    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Changed from user_id to landlord_id
    title = db.Column(db.String(120), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False, default=1)
    bathrooms = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    #reviews = db.relationship('Review', backref='listing', lazy=True)
     # Relationship with Review
    reviews = db.relationship('Review', backref='listing', lazy=True, cascade='all, delete-orphan')



def __init__(self, landlord_id, title, bedrooms, bathrooms, price, location, image):
    self.landlord_id = landlord_id
    self.title = title
    self.bedrooms = bedrooms
    self.bathrooms = bathrooms
    self.price = price
    self.location = location
    self.image = image

def _repr_(self):
    return f'<Listing {self.title}>'

def get_json(self):
    return{ 'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'price': self.price,
            'location': self.location,
            'image': self.image
            }