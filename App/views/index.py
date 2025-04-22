from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
from App.controllers.listing import get_all_public_listings, search_listings  # added for search functionality
from App.models import User, Listing

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/')
def index_page():
    # Get search parameters
    location = request.args.get('location')
    bedrooms = request.args.get('bedrooms', type=int)
    bathrooms = request.args.get('bathrooms', type=int)
    # Determine listings based on filters
    if location or bedrooms or bathrooms:
        listings = search_listings(location=location, bedrooms=bedrooms, bathrooms=bathrooms)
    else:
        listings = Listing.query.all()
    # Pass current filters to template for form persistence
    filters = {'location': location, 'bedrooms': bedrooms, 'bathrooms': bathrooms}
    return render_template('index.html', listings=listings, filters=filters)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})