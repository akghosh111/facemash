from app import db, Image


image_urls = [
    'static/images/image1.jpg',
    'static/images/image2.jpg',
    
]


for url in image_urls:
    new_image = Image(url=url)
    db.session.add(new_image)

db.session.commit()
