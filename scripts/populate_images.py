import os
import sys

# Adjust the path to find the 'app' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Flask app and required modules
from app import app, db, Image

# List of image URLs (update with your image file paths)
image_urls = [
    'static/images/ana.jpg',
    'static/images/dakota.jpg',
    'static/images/emma.jpg',
    'static/images/jennifer.jpg',
    'static/images/kate.jpg',
    'static/images/natalie.jpg',
    'static/images/alexandra.png',
]

# Function to populate images in the database
def populate_images():
    # Establish application context
    with app.app_context():
        # Iterate over each image URL
        for url in image_urls:
            # Create a new Image instance with an initial Elo rating of 1400
            new_image = Image(url=url, elo_rating=1400)
            # Add the new Image instance to the session
            db.session.add(new_image)
        
        # Commit the session to save changes to the database
        db.session.commit()

# Run the function to populate images
if __name__ == "__main__":
    populate_images()
