from flask import Blueprint, render_template
from App.controllers import get_listing, get_all_public_listings

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

@listing_views.route('/listings', methods=['GET'])
def view_all_listings():
    listings = get_all_public_listings()
    return render_template('index.html', listings=listings)

@listing_views.route('/listings/<int:id>', methods=['GET'])
def view_listing(id):
    listing = get_listing(id)
    return render_template('listing_details.html', listing=listing)