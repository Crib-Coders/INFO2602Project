from App.controllers.auth import verify_tenant_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import create_review, get_listing

review_views = Blueprint('review_views', __name__, template_folder='../templates')

@review_views.route('/listings/<int:listing_id>/reviews/new')
@jwt_required()  # Replace @login_required
@verify_tenant_required
def new_review(listing_id):
    current_user_id = get_jwt_identity()  # Get user ID from JWT
    listing = get_listing(listing_id)
    
    if not listing:
        flash('Listing not found', 'error')
        return redirect(url_for('listing_views.view_all_listings'))
    
    return render_template('add_review.html', listing=listing)

@review_views.route('/listings/<int:listing_id>/reviews', methods=['POST'])
@jwt_required()
def create_review_action(listing_id):
    """Handle review submission"""
    review_text = request.form.get('review_text')
    rating = request.form.get('rating')
    
    # Create the review
    create_review(listing_id, current_user.id, review_text, rating)
    
    flash('Review added successfully!', 'success')
    return redirect(url_for('listing_views.view_listing', id=listing_id))

@review_views.route('/reviews/add/<int:listing_id>', methods=['GET'])
@jwt_required()
def add_review_page(listing_id):
    return render_template('add_review.html', listing_id=listing_id)

@review_views.route('/reviews/add/<int:listing_id>', methods=['POST'])
@jwt_required()
def add_review_action(listing_id):
    # Handle form submission here
    return redirect(url_for('listing_views.view_listing', id=listing_id))