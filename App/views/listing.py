from flask import Blueprint, render_template
from App.controllers import get_listing, get_all_public_listings
from App.controllers.review import get_reviews_for_listing

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

@listing_views.route('/listings', methods=['GET'])
def view_all_listings():
    listings = get_all_public_listings()
    return render_template('index.html', listings=listings)

@listing_views.route('/listings/<int:id>', methods=['GET'])
def view_listing(id):
    listing = get_listing(id)
    reviews = get_reviews_for_listing(id) if listing else []
    return render_template('listing_details.html', listing=listing, reviews=reviews)

@listing_views.route('/listings/<int:listing_id>/reviews/create', methods=['GET', 'POST'])
def create_review(listing_id):
    listing = get_listing(listing_id)
    if not listing:
        return render_template('404.html'), 404
    return render_template('create_review.html', listing=listing)


