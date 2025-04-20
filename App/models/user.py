from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'user'


    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False, default='tenant')
    is_verified = db.Column(db.Boolean, nullable=False, default=False) #changed default to false as if it was true, every new tenant uswer would be verified

    # Relationships
    listings = db.relationship('Listing', backref='landlord', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='tenant', lazy=True, cascade='all, delete-orphan')

    def __init__(self, username, password, role='tenant', is_verified=None):  # Updated init
        self.username = username
        self.set_password(password)
        self.role = role
        # Set verification status based on role if not explicitly provided
        self.is_verified = is_verified if is_verified is not None else (role != 'tenant')

    def can_review(self):
        """Check if user can leave reviews"""
        return self.role == 'tenant' and self.is_verified
        
    def __repr__(self):
        return f'<User {self.username}>'

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'role': self.role
        }
    def is_authenticated(self):
        return True

    def is_admin(self):
        return self.role == 'admin'
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

