import os
import pwd
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
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
    db.create_all()

    # To setup the migration
    migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

# a persistent Game entity, extends the base SQLAlchemy Model
class Game(db.Model):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age_rating = Column(String)
    release_date = Column(DateTime)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    developer_id = Column(Integer, ForeignKey('developers.id'), nullable=False)

    def __init__(self, name, age_rating, release_date, category_id, developer_id):
        self.name = name
        self.age_rating = age_rating
        self.release_date = release_date
        self.category_id = category_id
        self.developer_id = developer_id

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
            'release_date': self.release_date, 
            'category_id': self.category_id,
            'developer_id': self.developer_id
        }

    def __repr__(self):
        return json.dumps(self.format())


# a persistent Category entity, extends the base SQLAlchemy Model
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    games = db.relationship('Game', backref='category', lazy='dynamic')

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
            'name': self.description,
            'description': self.description
        }

    def __repr__(self):
        return json.dumps(self.format())


# a persistent Developer entity, extends the base SQLAlchemy Model
class Developer(db.Model):
    __tablename__ = 'developers'

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    website = Column(String(120))
    games = db.relationship('Game', backref='developer', lazy='dynamic')

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