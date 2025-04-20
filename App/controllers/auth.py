from functools import wraps
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request
)
from flask import flash, redirect, url_for
from App.controllers.user import get_user_by_id 
from werkzeug.security import generate_password_hash, check_password_hash
from App.models import User
from App.database import db
from App.controllers.user import get_user_by_id

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Create token with additional claims
        additional_claims = {
            'role': user.role,
            'is_verified': user.is_verified
        }
        return create_access_token(identity=user.id, additional_claims=additional_claims)
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
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return User.query.get(user_id)
    except:
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
    """Make authentication status available to templates"""
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            current_user = User.query.get(user_id)
            is_authenticated = True
        except:
            is_authenticated = False
            current_user = None
        return dict(is_authenticated=is_authenticated, current_user=current_user)

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


def verify_tenant_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = get_user_by_id(user_id)  # Implement this function
        
        if not user or user.role != 'tenant':  # Check user role
            flash('Tenant access required', 'error')
            return redirect(url_for('index_views.index_page'))
            
        return f(*args, **kwargs)
    return wrapper


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