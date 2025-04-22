from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
import os
import uuid  # added to generate unique image filenames
from werkzeug.utils import secure_filename
from App.controllers import get_listing, get_all_public_listings
from App.controllers.review import get_reviews_for_listing, create_review as create_review_controller
from App.controllers.auth import get_current_user

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

@listing_views.route('/listings', methods=['GET', 'POST'])
def view_all_listings():
    user = get_current_user()
    if not user or user.role != 'landlord':
        flash('Only landlords can add listings.', 'error')
        return redirect(url_for('index_views.index_page'))
    if request.method == 'POST':
        title = request.form.get('title')
        bedrooms = request.form.get('bedrooms', type=int)
        bathrooms = request.form.get('bathrooms', type=int)
        price = request.form.get('price', type=float)
        location = request.form.get('location')
        description = request.form.get('description')
        # Process uploaded image with unique naming
        image_file = request.files.get('image')
        if image_file:
            orig = secure_filename(image_file.filename)
            ext = os.path.splitext(orig)[1]
            new_filename = f"{uuid.uuid4().hex}{ext}"
            dest = os.path.join(current_app.static_folder, 'images', new_filename)
            image_file.save(dest)
            filename = new_filename
        else:
            filename = ''
        # Create listing with image filename
        from App.controllers.listing import create_listing
        listing = create_listing(user.id, title, bedrooms, bathrooms, price, location, filename, description)
        if listing:
            flash('Listing added successfully!', 'success')
            return redirect(url_for('listing_views.view_listing', id=listing.id))
        else:
            flash('Failed to add listing. Please check your input.', 'error')
    return render_template('create_listing.html')

@listing_views.route('/listings/<int:id>', methods=['GET'])
def view_listing(id):
    listing = get_listing(id)
    reviews = get_reviews_for_listing(id) if listing else []
    return render_template('listing_details.html', listing=listing, reviews=reviews)

@listing_views.route('/listings/<int:listing_id>/reviews/create', methods=['GET', 'POST'])
def create_review(listing_id):
    listing = get_listing(listing_id)
    user = get_current_user()
    if not user:
        flash('Please login to leave a review', 'error')
        return redirect(url_for('auth_views.login_page'))
    if not listing:
        abort(404)

    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        text = request.form.get('text')
        review = create_review_controller(user.id, listing_id, text, rating)
        if review:
            flash('Review submitted successfully!', 'success')
        else:
            flash('Could not submit review. Please try again.', 'error')
        return redirect(url_for('listing_views.view_listing', id=listing_id))

    # GET displays form
    return render_template('create_review.html', listing=listing)


