from App.models import User
from App.database import db

def create_user(username, password, role="tenant", is_verified=False):
    newuser = User(username=username, password=password, role=role, is_verified=is_verified)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_user_details(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return None
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "is_verified": user.is_verified,
    }

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None


    