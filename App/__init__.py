# Import necessary modules and components
from flask import Flask
from .database import db
from flask_jwt_extended import JWTManager

# Import all models, controllers, views, and main logic (add this here)
from .models import *  # Import all models (User, Listing, Review, etc.)
from .views import *  # Import all views/templates (optional)
from .controllers import *  # Import all controllers (routes)
from .main import *  # Import any main logic or app setup if necessary

# Initialize Flask app
app = Flask(__name__)

# Set up configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database.db'  # Update to your DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key

# Initialize database and JWT manager
db.init_app(app)
jwt = JWTManager(app)

# Register Blueprints for routes (your controllers should be here)
from .controllers.review import review_routes
app.register_blueprint(review_routes)

# Additional blueprint registrations can go here for other controllers like user routes
# from .controllers.user import user_routes
# app.register_blueprint(user_routes)

# Main entry point for running the app
if __name__ == '__main__':
    app.run(debug=True)
