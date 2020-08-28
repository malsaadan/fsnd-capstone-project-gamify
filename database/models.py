import os
import pwd
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "gamify"
username = pwd.getpwuid(os.getuid())[0]

database_path = "postgres://{}@{}/{}".format(username, 'localhost:5432', database_name)

db = SQLAlchemy()

# binds a flask application and a SQLAlchemy service
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()

    # To setup the migration
    migrate = Migrate(app, db)

    seed()

#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

# a persistent Game entity, extends the base SQLAlchemy Model
class Game(db.Model):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age_rating = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    developer_id = Column(Integer, ForeignKey('developers.id'), nullable=False)
    image_link = Column(String)

    def __init__(self, name, age_rating, category_id, developer_id, image_link):
        self.name = name
        self.age_rating = age_rating
        self.category_id = category_id
        self.developer_id = developer_id
        self.image_link = image_link

    # inserts a new model into a database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # deletes a model from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # updates a model in the database
    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age_rating': self.age_rating,
            'category_id': self.category_id,
            'developer_id': self.developer_id,
            'image_link': self.image_link
        }

    def __repr__(self):
        return json.dumps(self.format())


# a persistent Category entity, extends the base SQLAlchemy Model
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    games = db.relationship('Game', cascade="all,delete", backref='category', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    # inserts a new model into a database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # deletes a model from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # updates a model in the database
    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def __repr__(self):
        return json.dumps(self.format())


# a persistent Developer entity, extends the base SQLAlchemy Model
class Developer(db.Model):
    __tablename__ = 'developers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    website = Column(String)
    games = db.relationship('Game', cascade="all,delete", backref='developer', lazy='dynamic')

    def __init__(self, name, website):
        self.name = name
        self.website = website

    # inserts a new model into a database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # deletes a model from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # updates a model in the database
    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website
        }

    def __repr__(self):
        return json.dumps(self.format())

# Add seed data to the database
def seed():
    category1 = Category(
        name='Role-playing',
        description='The only other game genre based on the name of the game that inspired it, rogue was a 2d computer game and dungeon crawler from 1980. the game featured a text interface and random level generation. players overcame enemies and obstacles to increase their player stats.'
    )
    category2 = Category(
        name='Fps',
        description='First-person shooters (fps) are played from the main character’s viewpoint; call of duty, half-life, and halo are good examples.'
    )
    category1.insert()
    category2.insert()

    developer = Developer(
        name='blizzard',
        website='www.blizzard.com'
    )
    developer.insert()

    game = Game(
        name='league of legends',
        age_rating='+18',
        category_id=1,
        developer_id=1,
        image_link='https://sm.ign.com/t/ign_mear/screenshot/default/league-of-legends_6d7q.h960.jpg'
    )
    game.insert()