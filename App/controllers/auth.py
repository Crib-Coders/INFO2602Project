from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request
)
from flask import session  # added session fallback
from werkzeug.security import generate_password_hash, check_password_hash
from App.models import User
from App.controllers import *
from App.database import db

def login(username, password):
    """Authenticate user and return token if successful"""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        print(user.get_role())
        return create_access_token(identity=user.id)
    return None

def register(username, password, role='tenant'):
    """Register a new user"""
    if User.query.filter_by(username=username).first():
        return None, "Username already exists"
    
    try:
        user = User(
            username=username,
            password=password,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def get_current_user():
    """Get the currently authenticated user"""
    # Try JWT first
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        # Fallback to session-based login
        user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def change_password(user_id, old_password, new_password):
    """Change user password"""
    user = User.query.get(user_id)
    if not user or not user.check_password(old_password):
        return False
    
    user.set_password(new_password)
    db.session.commit()
    return True

def setup_jwt(app):
    """Configure JWT settings"""
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.get(identity)
        return user.id if user else None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt

def add_auth_context(app):
    """Make authentication status available to templates, using session and JWT fallback"""
    @app.context_processor
    def inject_user():
        # Determine current user via JWT or session
        user = get_current_user()
        return dict(is_authenticated=bool(user), current_user=user)

def get_user_by_id(user_id):
    """Get user by ID"""
    return User.query.get(user_id)

def get_user_by_username(username):
    """Get user by username"""
    return User.query.filter_by(username=username).first()

def verify_tenant(user_id):
    """Verify a tenant account (admin only)"""
    user = User.query.get(user_id)
    if user and user.role == 'tenant':
        user.is_verified = True
        db.session.commit()
        return True
    return False


#Auth Controller Tests

def test_auth():
    # Test registration
    print("Testing registration...")
    user, error = register('testuser', 'testpass', 'tenant')
    assert user is not None and user.role == 'tenant' and not user.is_verified, "Tenant registration failed"
    print(f"✓ Registered tenant: {user.username} (verified: {user.is_verified})")
    
    # Test landlord registration
    landlord, error = register('testlandlord', 'landlordpass', 'landlord')
    assert landlord is not None and landlord.role == 'landlord' and landlord.is_verified, "Landlord registration failed"
    print(f"✓ Registered landlord: {landlord.username} (verified: {landlord.is_verified})")

    # Test login
    print("Testing login...")
    token = login('testuser', 'testpass')
    assert token is not None, "Login failed"
    print("✓ Login successful")
    
    # Test invalid login
    print("Testing invalid login...")
    token = login('testuser', 'wrongpass')
    assert token is None, "Invalid login test failed"
    print("✓ Invalid login rejected")