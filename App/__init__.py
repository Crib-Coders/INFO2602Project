from flask import Flask
from .database import db, init_db, create_db
from flask_jwt_extended import JWTManager
from .controllers.review import review_routes

# Initialize the Flask app
app = Flask(__name__)

# Set up app configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database.db'  # Use your actual DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your actual secret key

# Initialize extensions
init_db(app)  # Initialize the database

jwt = JWTManager(app)  # Initialize JWT manager

# Create the database and tables (if needed)
create_db()  # This will create tables based on the models

# Register Blueprints (controllers)
app.register_blueprint(review_routes)

# Main entry point to run the app
if __name__ == '__main__':
    app.run(debug=True)

