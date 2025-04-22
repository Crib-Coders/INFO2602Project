from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies


from.index import index_views

from App.controllers import (
    login,
    create_user,
    get_all_users,
    register,
    get_user_by_username  # needed for session store
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    
@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')
    
@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    if not token:
        flash('Invalid username or password', 'error')
        return redirect(url_for('auth_views.login_page'))

    response = redirect(url_for('index_views.index_page'))  # Redirect to home page
    set_access_cookies(response, token)
    # Set session user_id for fallback auth
    user = get_user_by_username(data['username'])
    if user:
        session['user_id'] = user.id
    flash('Login successful!', 'success')
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    # Clear session fallback
    session.pop('user_id', None)
    return response

@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    user, error = register(data['username'], data['password'])
    if error:
        flash(error, 'error')
        return redirect(url_for('auth_views.signup_page'))
    flash('Signup successful! Please login.', 'success')
    return redirect(url_for('auth_views.login_page'))

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response