from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    text = db.Column(db.String(120), nullable=False)

def __init__(self, user_id, text, user):
    self.user_id = user_id
    self.text = text
    self.user = user

def _repr_(self):
    return f'<Review {self.text}>'

def get_json(self):
    return {
        'id': self.id,
        'user_id': self.user_id,
        'text': self.text,
        'user': self.user.get_json()
    }
    
