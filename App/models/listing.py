from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Listing(db.Model):
    __tablename__ = 'listing'

    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False, default=1)
    bathrooms = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    reviews = db.relationship('Review', backref='listing', lazy=True, cascade='all, delete-orphan')

    def __init__(self, landlord_id, title, bedrooms, bathrooms, price, location, image, description=None):
        self.landlord_id = landlord_id
        self.title = title
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.price = price
        self.location = location
        self.image = image
        self.description = description

    def __repr__(self):
        return f'<Listing {self.title}>'

    def get_json(self):
        return {
            'id': self.id,
            'landlord_id': self.landlord_id,
            'title': self.title,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'price': self.price,
            'location': self.location,
            'image': self.image,
            'description': self.description
        }