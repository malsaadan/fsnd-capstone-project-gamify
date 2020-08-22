import os
from flask import (
    Flask, 
    request, 
    abort, 
    jsonify,
    render_template,
    flash
)
from database.models import setup_db, Game, Category, Developer
from flask_cors import CORS
from logging import Formatter, FileHandler

# I used a small number just to test it out
GAMES_PER_PAGE = 3

def paginate_games(request, selection):
    # Get the current page, if not provided use 1 as default
    page = request.args.get('page', 1, type=int)
    # Define the first games
    start = (page - 1) * GAMES_PER_PAGE
    # Define last game
    end = start + GAMES_PER_PAGE

    # Format games to be retrieved as JSON
    games = [game.format() for question in selection]
    current_games = games[start:end]

    return current_games

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # Set up Cors, allowing access for all origins (*)
  CORS(app)

  # Set access-control-allow for headers
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response
  
  @app.route('/')
  def index():
      return render_template('pages/home.html')

  @app.route('/games')
  def get_games():
      games = Game.query.order_by(Game.id).all()
      return jsonify({
          'games': games
      })
  

  @app.route('/categories')
  def get_categories():
      categories = Category.query.order_by(Category.id).all()
      return jsonify({
          'categories': categories
      })

  @app.route('/developers')
  def get_developers():
      developers = Developer.query.order_by(Developer.id).all()
      return jsonify({
          'developers': developers
      })

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

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)