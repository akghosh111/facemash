from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///images.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    elo_rating = db.Column(db.Float, default=1400)  # Base rating of 1400


db.create_all()


def get_random_pair():
    images = Image.query.all()
    return random.sample(images, 2)

# Elo rating calculation function
def calculate_elo(rating1, rating2, outcome, k=32):
    
    expected1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
    expected2 = 1 / (1 + 10 ** ((rating1 - rating2) / 400))

    
    new_rating1 = rating1 + k * (outcome - expected1)
    new_rating2 = rating2 + k * ((1 - outcome) - expected2)

    return new_rating1, new_rating2


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        
        image1_id = int(request.form.get("image1_id"))
        image2_id = int(request.form.get("image2_id"))
        voted_image_id = int(request.form.get("voted_image_id"))
        
        
        image1 = Image.query.get(image1_id)
        image2 = Image.query.get(image2_id)
        
        if voted_image_id == image1_id:
            outcome = 1  
        else:
            outcome = 0 
        
        new_rating1, new_rating2 = calculate_elo(image1.elo_rating, image2.elo_rating, outcome)
        
        
        image1.elo_rating = new_rating1
        image2.elo_rating = new_rating2
        db.session.commit()
        
      
        return redirect(url_for("index"))

    
    image1, image2 = get_random_pair()
    
    return render_template("index.html", image1=image1, image2=image2)


@app.route("/leaderboard")
def leaderboard():
    # Retrieve images sorted by Elo rating in descending order
    images = Image.query.order_by(Image.elo_rating.desc()).all()
    
    # Render the leaderboard template with the images data
    return render_template("leaderboard.html", images=images)


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
