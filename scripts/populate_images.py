from app import db, Image


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
    new_image = Image(url=url)
    db.session.add(new_image)

db.session.commit()
