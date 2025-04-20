from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import create_listing, get_all_public_listings, get_listing

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

@listing_views.route('/listings/create', methods=['GET'])
@jwt_required()
def create_listing_page():
    return render_template('create_listing.html')

@listing_views.route('/listings/create', methods=['POST'])
@jwt_required()
def create_listing_action():
    # Handle form submission here
    return redirect(url_for('listing_views.view_all_listings'))

@listing_views.route('/listings', methods=['GET'])
def view_all_listings():
    listings = get_all_public_listings()
    return render_template('index.html',  # Using the same template as homepage
                         listings=listings,
                         current_user=current_user)

@listing_views.route('/listings/<int:id>', methods=['GET'])
def view_listing(id):
    listing = get_listing(id)
    return render_template('listing_details.html', listing=listing)