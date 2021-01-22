#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Show(db.Model):
    __tablename__ = 'Show'
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)

    start_time = db.Column(db.DateTime, nullable=False)

    venue = db.relationship('Venue', backref=db.backref('venues'))
    artist = db.relationship('Artist', backref=db.backref('artists'))

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(1000))
    genres = db.Column(db.ARRAY(db.String))
    past_shows = db.Column(db.ARRAY(MutableDict.as_mutable(HSTORE)))
    upcoming_shows = db.Column(db.ARRAY(MutableDict.as_mutable(HSTORE)))
    past_shows_count = db.Column(db.Integer)
    upcoming_shows_count = db.Column(db.Integer)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website =  website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(1000))
    genres = db.Column(db.ARRAY(db.String))
    past_shows = db.Column(db.ARRAY(MutableDict.as_mutable(HSTORE)))
    upcoming_shows = db.Column(db.ARRAY(MutableDict.as_mutable(HSTORE)))
    past_shows_count = db.Column(db.Integer)
    upcoming_shows_count = db.Column(db.Integer)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  areas = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state).order_by('state').all()
  data = []
  for area in areas:
      venues = Venue.query.filter_by(state=area.state).filter_by(city=area.city).order_by('name').all()
      venue_data = []
      for venue in venues:
        shows = Venue.query.join(Show).join(Artist).filter((Show.venue_id == Venue.id) & (Show.artist_id == Artist.id)).all()
        venue_data.append({
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': len(shows)
        })  
      data.append({
        'city': area.city,
        'state': area.state,
        'venues': venue_data
      })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form['search_term']
  search = "%{}%".format(search_term)
  venues = Venue.query.filter(Venue.name.ilike(search)).all()
  venueList = []

  for venue in venues:
    upcoming_shows_DB = db.session.query(Show).join(Artist).join(Venue).filter(
      Show.artist_id == Artist.id,
      Show.venue_id == Venue.id,
      Show.start_time > datetime.now()
    ).filter_by(id=venue.id).count()
    print(upcoming_shows_DB)
    venueList.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": upcoming_shows_DB
    })

  response={
    "count": len(venues),
    "data": venueList
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  venue = Venue.query.get(venue_id)

  date_format = '%Y-%m-%d %H:%M:%S'
  past_shows = []
  upcoming_shows = []

  past_shows_DB = db.session.query(Show).join(Artist).join(Venue).filter(
    Show.artist_id == Artist.id,
    Show.venue_id == Venue.id,
    Show.start_time < datetime.now()
  ).filter_by(id=venue_id).all()

  upcoming_shows_DB = db.session.query(Show).join(Artist).join(Venue).filter(
    Show.artist_id == Artist.id,
    Show.venue_id == Venue.id,
    Show.start_time > datetime.now()
  ).filter_by(id=venue_id).all()

  for upShow in upcoming_shows_DB:
    upcoming_shows.append({
      "artist_id": upShow.artist.id,
      "artist_name": upShow.artist.name,
      "artist_image_link": upShow.artist.image_link,
      "start_time": datetime.strftime(upShow.start_time, date_format),
      "venue_id": upShow.venue.id,
      "venue_name": upShow.venue.name,
    })

  for show in past_shows_DB:
    past_shows.append({
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": datetime.strftime(show.start_time, date_format),
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
    })
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  data = {}
  try:
      test = request.form
      print(request.form['genres'])
      name = request.form['name']
      state = request.form['state']
      city = request.form['city']
      address = request.form['address']
      phone = request.form['phone']
      genres = request.form.getlist('genres')
      facebook_link = request.form['facebook_link']
      venue = Venue(name=name, city=city, state=state, address=address, phone=phone, facebook_link=facebook_link, genres=genres)
      db.session.add(venue)
      db.session.commit()
      data['id'] = venue.id
      data['name'] = venue.name
      data['city'] = venue.city
      data['state'] = venue.state
      data['address'] = venue.address
      data['phone'] = venue.phone
      data['facebook_link'] = venue.facebook_link
      data['genres'] = venue.genres
  except:
      error = True
      db.session.rollback()
      flash('An error occurred. Venue ' + request.data.name + ' could not be listed.')
  finally:
      db.session.close()
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form['search_term']
  search = "%{}%".format(search_term)
  artists = Artist.query.filter(Artist.name.ilike(search)).all()
  artistList = []

  for artist in artists:
    upcoming_shows_DB = db.session.query(Show).join(Venue).join(Artist).filter(
      Show.artist_id == Artist.id,
      Show.venue_id == Venue.id,
      Show.start_time > datetime.now()
    ).filter_by(id=artist.id).count()
    print(upcoming_shows_DB)
    artistList.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": upcoming_shows_DB
    })
  response={
    "count": len(artists),
    "data": artistList
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  artist = Artist.query.get(artist_id)
  date_format = '%Y-%m-%d %H:%M:%S'
  past_shows = []
  upcoming_shows = []

  past_shows_DB = db.session.query(Show).join(Venue).join(Artist).filter(
    Show.artist_id == Artist.id,
    Show.venue_id == Venue.id,
    Show.start_time < datetime.now()
  ).filter_by(id=artist_id).all()

  upcoming_shows_DB = db.session.query(Show).join(Venue).join(Artist).filter(
    Show.artist_id == Artist.id,
    Show.venue_id == Venue.id,
    Show.start_time > datetime.now()
  ).filter_by(id=artist_id).all()

  for upShow in upcoming_shows_DB:
    upcoming_shows.append({
      "artist_id": upShow.artist.id,
      "artist_name": upShow.artist.name,
      "artist_image_link": upShow.artist.image_link,
      "start_time": datetime.strftime(upShow.start_time, date_format),
      "venue_id": upShow.venue.id,
      "venue_name": upShow.venue.name,
    })

  for show in past_shows_DB:
    past_shows.append({
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": datetime.strftime(show.start_time, date_format),
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
    })

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    for key in request.form.to_dict():
      artist[key] = request.form[key]
    
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    for key in request.form.to_dict():
      venue[key] = request.form[key]
    
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  data = {}
  try:
      test = request.form
      print(request.form['genres'])
      name = request.form['name']
      state = request.form['state']
      city = request.form['city']
      phone = request.form['phone']
      genres = request.form.getlist('genres')
      facebook_link = request.form['facebook_link']
      artist = Artist(name=name, city=city, state=state, phone=phone, facebook_link=facebook_link, genres=genres)
      db.session.add(artist)
      db.session.commit()
      data['id'] = artist.id
      data['name'] = artist.name
      data['city'] = artist.city
      data['state'] = artist.state
      data['phone'] = artist.phone
      data['facebook_link'] = artist.facebook_link
      data['genres'] = artist.genres
  except:
      error = True
      db.session.rollback()
      flash('An error occurred. Artist ' + request.data.name + ' could not be listed.')
  finally:
      db.session.close()
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = db.session.query(Show).join(Venue).join(Artist).filter(
    Show.artist_id == Artist.id,
    Show.venue_id == Venue.id,
  ).all()
  date_format = '%Y-%m-%d %H:%M:%S'
  data = []
  print(shows)
  for show in shows:
    data.append({
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image": show.artist.image_link,
      "start_time": datetime.strftime(show.start_time, date_format)
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  error = False
  date_format = '%Y-%m-%d %H:%M:%S'
  data = {}
  try:
    show = Show(
      artist_id=request.form['artist_id'],
      venue_id=request.form['venue_id'],
      start_time=datetime.strptime(request.form['start_time'], date_format))
    venue = Venue.query.get(request.form['venue_id'])
    artist = Artist.query.get(request.form['artist_id'])
    artist.shows = [show]
    venue.shows = [show]
    db.session.add_all([artist, venue, show])
    db.session.commit()
  except Exception as e:
      error = True
      db.session.rollback()
      print(f'Error ==> {e}')
      flash('Show was not successfully listed!')
  finally:
      db.session.close()
  if not error:
    flash('Show was successfully listed!')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
