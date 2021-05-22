from sqlalchemy import Integer, Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

# database_name = "capstone"
# database_path = "postgres://{}:{}@{}/{}".format('lyuben', 'temp123!','localhost:5432', database_name)
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
class Person(db.Model):  
  __tablename__ = 'People'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'catchphrase': self.catchphrase}

class Event(db.Model):  
  __tablename__ = 'Events'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  location = Column(String)

  def __init__(self, name, location=""):
    self.name = name
    self.location = location

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'location': self.location}

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()

class Location(db.Model):  
  __tablename__ = 'Location'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  location = Column(String)

  def __init__(self, name, location=""):
    self.name = name
    self.location = location

  def insert(self):
    db.session.add(self)
    db.session.commit()
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'location': self.location}

