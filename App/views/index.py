from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize

index_views = Blueprint('index_views', __name__, template_folder='../templates')
from App.controllers import (
    get_listing,
    get_all_listing,
    initialize,
)

@index_views.route('/', methods=['GET'])
def index_page():
    listings = get_all_listing()
    return render_template('index.html', listings=listings)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/<int:listing_id>', methods=['GET'])
def get_listing_page(listing_id):
    listing = get_listing(listing_id)
    return render_template('detail.html', listing=listing)