from flask import Blueprint, request, jsonify
from App.models import Review, db
from flask_jwt_extended import jwt_required, get_jwt_identity

review_routes = Blueprint('review_routes', __name__)

@review_routes.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    data = request.get_json()
    user_id = get_jwt_identity()

    listing_id = data.get('listing_id')
    text = data.get('text')
    rating = data.get('rating')

    if not listing_id or not text or not rating:
        return jsonify({"error": "Missing fields"}), 400

    try:
        review = Review(tenant_id=user_id, listing_id=listing_id, text=text, rating=int(rating))
        db.session.add(review)
        db.session.commit()
        return jsonify(review.get_json()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

