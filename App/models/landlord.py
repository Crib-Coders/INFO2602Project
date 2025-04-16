from App.database import db
from .user import User

class Landlord(User):
    __tablename__ = 'landlord'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)

  
    def __init__(self, name, email, phone, city):
        self.name = name
        self.email = email
        self.phone = phone
        self.city = city

    def __repr__(self):
        return f'<Landlord {self.name}>'
    def get_json(self):
        return { 'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'city': self.city
                }
