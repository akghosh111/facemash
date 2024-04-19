from flask import Flask, render_template, request, redirect, url_for
from cs50 import SQL
import random

app = Flask(__name__)


db = SQL("sqlite:///images.db")

def get_random_pair():
    images = db.execute("SELECT * FROM image")
    if len(images) < 2:
        return None, None
    return random.sample(images, 2)

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

      
        image1 = db.execute("SELECT * FROM image WHERE id = ?", image1_id)[0]
        image2 = db.execute("SELECT * FROM image WHERE id = ?", image2_id)[0]

   
        outcome = 1 if voted_image_id == image1_id else 0
        
  
        new_rating1, new_rating2 = calculate_elo(image1['elo_rating'], image2['elo_rating'], outcome)



        db.execute("UPDATE image SET elo_rating = ? WHERE id = ?", new_rating1, image1_id)
        db.execute("UPDATE image SET elo_rating = ? WHERE id = ?", new_rating2, image2_id)

       
        print(f"Updated ratings: Image 1 ({image1_id}) new rating = {new_rating1}, Image 2 ({image2_id}) new rating = {new_rating2}")

        
        return redirect(url_for("index"))

    image1, image2 = get_random_pair()
    
  
    if not image1 or not image2:
        return "Not enough images in the database to vote"

    
    return render_template("index.html", image1=image1, image2=image2)

@app.route("/leaderboard")
def leaderboard():
    
    images = db.execute("SELECT * FROM image ORDER BY elo_rating DESC")


    return render_template("leaderboard.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)
