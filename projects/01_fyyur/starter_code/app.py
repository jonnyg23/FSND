#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.orm import aliased
import re

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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
    seeking_description = db.Column(db.String(500), default='')
    seeking_talent = db.Column(db.Boolean, default=False)
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    shows = db.relationship('Show', backref='Venue', lazy='dynamic')

    def __init__(self, name, genres, address, city, state, phone, website, facebook_link, image_link, seeking_talent=False, seeking_description=""):
      self.name = name
      self.genres = genres
      self.city = city
      self.state = state
      self.address = address
      self.phone = phone
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.website = website
      self.seeking_talent = seeking_talent
      self.seeking_description = seeking_description

    def short(self):
      """
      Method displays only id and name from Venues.
      """
      return{
        "id": self.id,
        "name": self.name
      }

    def long(self):
      """
      Method displays id, name, city, and state from Venues.
      """
      return{
        "id": self.id,
        "name": self.name,
        "city": self.city,
        "state": self.state
      }
    
    def info(self):
      return{
        "id": self.id,
        "name": self.name,
        "genres": self.genres,
        "address": self.address,
        "city": self.city,
        "phone": self.phone,
        "website": self.website,
        "facebook_link": self.facebook_link,
        "seeking_talent": self.seeking_talent,
        "seeking_description": self.seeking_description,
        "image-link": self.image_link
      }

    def __repr__(self):
        return f'<Venue ID: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, website: {self.website}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, seeking_talent: {self.seeking_talent}, seeking_description: {self.seeking_description}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), default=' ')
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Artist', lazy=True)

    def __init__(self, name, genres, city, state, phone, image_link, website, facebook_link, seeking_venue=False, seeking_description=""):
      self.name = name
      self.genres = genres
      self.city = city
      self.state = state
      self.phone = phone
      self.website = website
      self.facebook_link = facebook_link
      self.seeking_venue = seeking_venue
      self.seeking_description = seeking_description
      self.image_link = image_link

    def short(self):
      """
      Method displays id and name of Artist.
      """
      return{
        'id': self.id,
        'name':self.name,
      }

    def info(self):
      return{
        "id": self.id,
        "name": self.name,
        "genres": self.genres,
        "city": self.city,
        "state": self.state,
        "phone": self.phone,
        "website": self.website,
        "facebook_link": self.facebook_link,
        "seeking_venue": self.seeking_venue,
        "seeking_description": self.seeking_description,
        "image_link": self.image_link
      }

    def __repr__(self):
        return f'<Artist ID: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, phone: {self.phone}, genres: {self.genres}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, seeking_venue: {self.seeking_venue}, seeking_description: {self.seeking_description}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# Added Shows object with Many-to-many relationship with Artists and Venues
class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  start_time = db.Column(db.String, nullable=False)

  def __init__(self, venue_id, artist_id, start_time):
    self.venue_id = venue_id
    self.artist_id = artist_id
    self.start_time = start_time

  def venue_info(self):
    """
    Shows Venue id, name, image_link, and start_time.
    """
    return{
      "venue_id": self.venue_id,
      "venue_name": self.Venue.name,
      "venue_image_link": self.Venue.image_link,
      "start_time": self.start_time
    }

  def artist_info(self):
    """
    Shows Artist id, name, image_link, and start time.
    """
    return{
      "artist_id": self.venue_id,
      "artist_name": self.Artist.name,
      "artist_image_link": self.Artist.image_link,
      "start_time": self.start_time
    }

  def info(self):
    return{
      "venue_id": self.venue_id,
      "venue_name": self.Venue.name,
      "artist_id": self.artist_id,
      "artist_name": self.Artist.name,
      "artist_image_link": self.Artist.image_link,
      "start_time": self.start_time
    }

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]

  data = []
  venue_query = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  venue_location = ''
  current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
  
  for venue in venue_query:
    # show upcoming shows
    upcoming_shows = venue.shows.filter(Show.start_time > current_time).all()
    if venue_location == venue.state + venue.city:
      data[len(data) - 1]["venues"].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(upcoming_shows)
      })
    else:
      venue_location == venue.state + venue.state
      data.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(upcoming_shows)
        }]
      })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  search_term = request.form.get('search_term', '').strip()
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%'))
  venue_list = list(map(Venue.short, venues))
  response = {
    "count": len(venue_list),
    "data": venue_list
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }

  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

  venue_query = Venue.query.get(venue_id)

  if venue_query:
    current_time = datetime.now().strftime('&Y-%m-%d %H:%M:%S')
    venue_info = Venue.info(venue_query)
    new_shows_query = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id).filter(Show.start_time > current_time).all()
    past_shows_query = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id).filter(Show.start_time <= current_time).all()
    
    new_shows = list(map(Show.artist_info, new_shows_query))
    past_shows = list(map(Show.artist_info, past_shows_query))
    
    venue_info["upcoming_shows"] = new_shows
    venue_info["upcoming_shows_count"] = len(new_shows)
    venue_info["past_shows"] = past_shows
    venue_info["past_shows_count"] = len(past_shows)

    return render_template('pages/show_venue.html', venue=venue_info)

  else:
    return render_template('errors/404.html')

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = VenueForm()

  name = form.name.data.strip()
  city = form.city.data.strip()
  state = form.state.data
  address = form.address.data.strip()
  phone = form.phone.data
  phone = re.sub('\D','', phone) # Take away anything that isn't a #
  genres = form.genres.data
  seeking_talent = True if form.seeking_talent.data == 'Yes' else False
  seeking_description = form.seeking_description.data.strip()
  image_link = form.image_link.data.strip()
  facebook_link = form.facebook_link.data.strip()
  website = form.website.data.strip()

  # Redirects to form if there are errors in the form validation
  if not form.validate():
    flash( form.errors )
    return redirect(url_for('create_venue_submission'))

  else:
    try:
      error_inserting = False
      venue_submission = Venue(name=name,city=city,state=state,address=address,phone=phone,genres=genres,image_link=image_link,facebook_link=facebook_link, seeking_description=seeking_description,seeking_talent=seeking_talent,website=website)
      db.session.add(venue_submission)
      db.session.commit()

    except Exception as e:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      error_inserting = True
      print(f'Exception "{e}" in create_venue_submission()')
      db.session.rollback()
    
    finally:
      db.session.close()

    if not error_inserting:
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      return redirect(url_for('index'))
      
    else:
      flash('An error occurred. Venue ' + request.form['name'] + 'could not be listed.')
      print("Error in create_venue_submission()")
      abort(500)

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # Deletes venue based on AJAX call

  error_deleting = False
  venue2Delete = Venue.query.get(venue_id)
  venue2Delete_name = venue2Delete.name
  if not venue2Delete:
    # Redirect home - URL doesn't exist
    return redirect(url_for('index'))

  else:  
    try:
        db.session.delete(venue2Delete)
        db.session.commit()
    except():
        error_deleting = True
        db.session.rollback()
    finally:
        db.session.close()
    if error_deleting:
        print("Error in delete_venue()")
        flash(f'An error occurred while deleting venue {venue2Delete_name}.')
        abort(500)
    else:
        return jsonify({
          'deleted': True,
          'url': url_for('venues')
        })

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]

  data = []
  artists = Artist.query.order_by(Artist.name).all()
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  search_term = request.form.get('search_term', '').strip()
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%'))
  artist_list = list(map(Artist.short, artists))
  response={
    "count": len(artist_list),
    "data": artist_list
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

  artist_query = Artist.query.get(artist_id)

  if artist_query:
    current_time = datetime.now().strftime('&Y-%m-%d %H:%M:%S')
    artist_info = Artist.info(artist_query)
    new_shows_query = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id).filter(Show.start_time > current_time).all()
    past_shows_query = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id).filter(Show.start_time <= current_time).all()
    
    new_shows = list(map(Show.venue_info, new_shows_query))
    past_shows = list(map(Show.venue_info, past_shows_query))
    
    artist_info["upcoming_shows"] = new_shows
    artist_info["upcoming_shows_count"] = len(new_shows)
    artist_info["past_shows"] = past_shows
    artist_info["past_shows_count"] = len(past_shows)

    return render_template('pages/show_artist.html', artist=artist_info)

  else:
    return render_template('errors/404.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  artist_data = Artist.query.get(artist_id)
  if not artist_data:
    # Redirect home - URL doesn't exist
    return redirect(url_for('index'))
  else:
    # Artist is valid, proceed to populate form
    form = ArtistForm()
  
  if artist_data:

    artist_info = Artist.info(artist_data)
    form.name.data = artist_info["name"]
    form.genres.data = artist_info["genres"]
    form.city.data = artist_info["city"]
    form.state.data = artist_info["state"]
    form.phone.data = artist_info["phone"]
    form.website.data = artist_info["website"]
    form.facebook_link = artist_info["facebook_link"]
    form.seeking_venue = artist_info["seeking_venue"]
    form.seeking_description = artist_info["seeking_description"]
    form.image_link = artist_info["image_link"]
    
    return render_template('forms/edit_artist.html', form=form, artist=artist_info)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()

  name = form.name.data.strip()
  city = form.city.data.strip()
  state = form.state.data
  phone = form.phone.data
  phone = re.sub('\D','', phone) # Take away anything that isn't a #
  genres = form.genres.data
  seeking_venue = True if form.seeking_venue.data == 'Yes' else False
  seeking_description = form.seeking_description.data.strip()
  image_link = form.image_link.data.strip()
  facebook_link = form.facebook_link.data.strip()
  website = form.website.data.strip()

  if not form.validate():
    flash( form.errors )
    return redirect(url_for('edit_artist_submission', artist_id=artist_id))

  else:
    error_updating = False
    try:
      artist = Artist.query.get(artist_id)

      artist.name = name
      artist.city = city
      artist.state = state
      artist.phone = phone
      artist.genres = genres
      artist.seeking_venue = seeking_venue
      artist.seeking_description = seeking_description
      artist.image_link = image_link
      artist.website = website
      artist.facebook_link = facebook_link

      db.session.commit()

    except Exception as e:
      error_updating = True
      print(f'Exception "{e}" in edit_artist_submission()')
      db.session.rollback()
    finally:
      db.session.close()

    if not error_updating:
      flash('Artist ' + request.form['name'] + ' was updated successfully!')
      return redirect(url_for('show_artist', artist_id=artist_id))
    else:
      flash('An error occurred. Artist ' + name + ' could not be updated.')
      abort(500)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO: populate form with values from venue with ID <venue_id>

  venue = Venue.query.get(venue_id)

  if not venue:
    # Redirect home - URL doesn't exist
    return redirect(url_for('index'))
  
  else:
    form = VenueForm()
    venue_info = Venue.info(venue)
    form.name.data = venue_info["name"]
    form.genres.data = venue_info["genres"]
    form.address.data = venue_info["address"]
    form.city.data = venue_info["city"]
    form.state.data = venue_info['"state']
    form.phone.data = venue_info["phone"]
    form.website.data = venue_info["website"]
    form.facebook_link.data = venue_info["facebook_link"]
    form.seeking_talent.data = venue_info["seeking_talent"]
    form.seeking_description.data = venue_info["seeking_description"]
    form.image_link.data = venue_info["image_link"]

    return render_template('form/edit_venue.html', form=form, Venue=venue_info)

  

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  # Similar to edit_artist_submission above

  form = VenueForm()
  
  name = form.name.data.strip()
  city = form.city.data.strip()
  state = form.state.data
  address = form.address.data.strip()
  phone = form.phone.data
  phone = re.sub('\D','', phone) # Take away anything that isn't a #
  genres = form.genres.data
  seeking_talent = True if form.seeking_talent.data == 'Yes' else False
  seeking_description = form.seeking_description.data.strip()
  image_link = form.image_link.data.strip()
  facebook_link = form.facebook_link.data.strip()
  website = form.website.data.strip()
  
  if not form.validate():
    flash( form.errors )
    return redirect(url_for('edit_venue_submission', venue_id=venue_id))
  
  else:
    error_updating = False
    try:
      venue = Venue.query.get(venue_id)
  
      venue.name = name
      venue.city = city
      venue.state = state
      venue.address = address
      venue.phone = phone
      venue.genres = genres
      venue.seeking_talent = seeking_talent
      venue.seeking_description = seeking_description
      venue.image_link = image_link
      venue.website = website
      venue.facebook_link = facebook_link
  
      db.session.commit()
  
    except Exception as e:
      error_updating = True
      print(f'Exception "{e}" in edit_venue_submission()')
      db.session.rollback()
    finally:
      db.session.close()
  
    if not error_updating:
      flash('Venue ' + request.form['name'] + ' was updated successfully!')
      return redirect(url_for('show_venue', venue_id=venue_id))
    else:
      flash('An error occurred. Venue ' + name + ' could not be updated.')
      abort(500)
  
  
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm()

  name = form.name.data.strip()
  city = form.city.data.strip()
  state = form.state.data
  phone = form.phone.data
  phone = re.sub('\D','', phone) # Take away anything that isn't a #
  genres = form.genres.data
  seeking_venue = True if form.seeking_venue.data == 'Yes' else False
  seeking_description = form.seeking_description.data.strip()
  image_link = form.image_link.data.strip()
  facebook_link = form.facebook_link.data.strip()
  website = form.website.data.strip()

  # Redirects to form if there are errors in the form validation
  if not form.validate():
    flash( form.errors )
    return redirect(url_for('create_artist_submission'))

  else:
    try:
      error_inserting = False
      artist_submission = Artist(name=name,city=city,state=state,phone=phone,genres=genres,image_link=image_link,facebook_link=facebook_link, seeking_description=seeking_description,seeking_venue=seeking_venue,website=website)
      db.session.add(artist_submission)
      db.session.commit()

    except Exception as e:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      error_inserting = True
      print(f'Exception "{e}" in create_artist_submission()')
      db.session.rollback()
    
    finally:
      db.session.close()

    if not error_inserting:
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      return redirect(url_for('index'))
      
    else:
      flash('An error occurred. Artist ' + request.form['name'] + 'could not be listed.')
      print("Error in create_artist_submission()")
      abort(500)

@app.route('/artists/<artist_id>/delete', methods=['DELETE'])
def delete_artist(artist_id):

  # Code Similar to delete_venue

  error_deleting = False
  artist2Delete = Artist.query.get(artist_id)
  artist2Delete_name = artist2Delete.name
  if not artist2Delete:
    # Redirect home - URL doesn't exist
    return redirect(url_for('index'))

  else:  
    try:
        db.session.delete(artist2Delete)
        db.session.commit()
    except():
        error_deleting = True
        db.session.rollback()
    finally:
        db.session.close()
    if error_deleting:
        print("Error in delete_artist()")
        flash(f'An error occurred while deleting artist {artist2Delete_name}.')
        abort(500)
    else:
        return jsonify({
          'deleted': True,
          'url': url_for('artists')
        })


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  body = {}
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    # db.session.query(db.exists().where(Artist.id == artist_id)).scalar()

    show = Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
    db.session.add(show)
    db.session.commit()

    body['artist_id'] = show.artist_id
    body['venue_id'] = show.venue_id
    body['start_time'] = show.start_time

    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except():
    db.session.rollback()
    error = True
  finally:
      db.session.close()
  if error:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    flash('An error occurred. Show could not be listed.')
  else:
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
