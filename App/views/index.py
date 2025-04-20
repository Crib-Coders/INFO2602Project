from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
from App.controllers.listing import get_all_public_listings

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/')
def index_page():
    listings = get_all_public_listings()
    print(f"Listings data: {listings}")  # Debug output
    if not listings:
        listings = []
        print("No listings found")  # Debug output
    return render_template('index.html', listings=listings)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})