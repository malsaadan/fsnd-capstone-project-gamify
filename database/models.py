import os
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "gamify"

# local host path
database_path = "postgres://{}@{}/{}".format('mashaelmohammed', 'localhost:5432', database_name)
# heroku path
# database_path = "postgres://vwlmcqzupzkxkj:bf43c8dc10d4b854edb653c98b58df225ebb65e9cdc76902bbe49ee0db9b4101@ec2-3-215-207-12.compute-1.amazonaws.com:5432/dek8claq8cift1"
db = SQLAlchemy()

# binds a flask application and a SQLAlchemy service
def setup_db(app, database_path=database_path, database_name=database_name):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # Drop all records
    # db.drop_all()

    # Seed the db with data (from a backup file)
    # os.system("psql -U mashaelmohammed  -d {0} -f  {1}".format(database_name, 'gamify.psql') )


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