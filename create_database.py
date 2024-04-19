from cs50 import SQL
import os


db_path = "images.db"


if not os.path.exists(db_path):
    
    open(db_path, 'w').close()


db = SQL(f"sqlite:///{db_path}")


db.execute("""
CREATE TABLE IF NOT EXISTS image (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL,
    elo_rating REAL DEFAULT 1400
)
""")

image_urls = [
    'static/images/ana.jpg',
    'static/images/dakota.jpg',
    'static/images/emma.jpg',
    'static/images/jennifer.jpg',
    'static/images/kate.jpg',
    'static/images/natalie.jpg',
    'static/images/alexandra.png',
]

for url in image_urls:
    
    db.execute("INSERT INTO image (url) VALUES (?)", url)
