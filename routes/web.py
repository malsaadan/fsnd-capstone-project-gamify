from flask import (
    Blueprint,
    request,
    abort, 
    jsonify,
    render_template,
    redirect,
    url_for,
    flash,
    current_app
)
from database.models import Game, Category, Developer
from auth.auth import AuthError, requires_auth
from flask_wtf import Form
from forms import *
import os

web_app = Blueprint('web_app', __name__, template_folder='templates')

# method to specify the choices of games form for both of category & developer fields
def set_game_choices():
    # Specify the form
    form = GameForm()
    # Query all categories from the db
    categories = Category.query.order_by(Category.id).all()
    # Format the categories
    formatted_categories = [category.name for category in categories]
    # Query all developers from the db
    developers = Developer.query.order_by(Developer.id).all()
    # Format the developers
    formatted_developers = [developer.name for developer in developers]

    # Set choices for category & developer fields
    form.category.choices = formatted_categories
    form.developer.choices = formatted_developers
    return form
    
# Landing page route
@web_app.route('/')
def index():
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
    auth_link='https://'+AUTH0_DOMAIN+'/authorize?audience='+AUTH0_AUDIENCE+'&response_type=token&client_id='+AUTH0_CLIENT_ID+'&redirect_uri='+AUTH0_CALLBACK_URL
    return render_template('pages/home.html', auth_link=auth_link)

@web_app.route('/callback')
def callback():
    return render_template('pages/home.html')


@web_app.route('/games')
def get_games():
    # Query all games from the db
    games = Game.query.order_by(Game.id).all()
    # Format all games
    formatted_games = [game.format() for game in games]

    return render_template('pages/games.html', games=formatted_games, games_count=len(formatted_games))
  
# Search method
@web_app.route('/', methods=['POST'])
@web_app.route('/games', methods=['POST'])
@web_app.route('/categories', methods=['POST'])
@web_app.route('/developers', methods=['POST'])
def search_game():
    # Get the search term from the submitted form
    search_term = request.form.get('search_term', '')
    # If the submitted key term is empty
    if search_term == '':
        flash('Please enter a search term.')
        return redirect(request.url)
    else:
        # Query games from the database and filter them by name which matches the key term
        search_results = Game.query.filter(Game.name.ilike(f'%{search_term.lower()}%')).all()
        # Format the results
        formatted_results = [result.format() for result in search_results]
        return render_template('pages/games.html', games=formatted_results, games_count=len(formatted_results))

@web_app.route('/games/create')
def create_game_form():
    # Set form choices
    form = set_game_choices()
    return render_template('forms/new_game.html', form=form)

@web_app.route('/games/create', methods=['POST'])
def create_game_submission():
    try:
        # Query both category & developer based on name
        category = Category.query.filter_by(name=request.form["category"].lower()).first()
        developer = Developer.query.filter_by(name=request.form["developer"].lower()).first()
        # Create a game instance
        game = Game(
            name = request.form["name"].lower(),
            age_rating = request.form["age_rating"],
            category_id = category.id,
            developer_id = developer.id,
            image_link = request.form["image_link"]
        )
        # Create the record
        game.insert()

        flash(request.form['name']+ ' game was successfully listed!')
        return redirect(url_for('web_app.get_games'))
    except:
        abort(422)

@web_app.route('/games/<game_id>')
def show_game(game_id):
    # Get the selected game
    game = Game.query.filter_by(id=game_id).one_or_none()
    # If the game does not exist then abort
    if game is None:
        abort(404)

    # Extract the name of category & developer of the game
    category_name = Category.query.get(game.category_id).name
    developer_name = Developer.query.get(game.developer_id).name
    return render_template('pages/show_game.html', game=game, category_name=category_name, developer_name=developer_name)

@web_app.route('/games/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    # Query the game to be deleted
    game = Game.query.get(game_id)
    # If the given id does not exist then abort 404 (was not found)
    if game is None:
        abort(404)
    try:
        # If the game was found delete it and return to home page
        game.delete()
        flash('Game with id '+game_id+' has been deleted successfully!')
        return redirect(url_for('web_app.index'))
    except:
        abort(422)

@web_app.route('/games/<game_id>/edit')
def edit_game(game_id):
    game = Game.query.get(game_id)
    # If the game does not exist then abort
    if game is None:
        abort(404)

    # Assign the choices of category & developer form fields
    form = set_game_choices()
    # Set the default value for each one of them
    form.age_rating.process_data(game.age_rating)
    category_name = Category.query.get(game.category_id).name
    form.category.process_data(category_name)
    developer_name = Developer.query.get(game.developer_id).name
    form.developer.process_data(developer_name)
    return render_template('forms/edit_game.html', form=form, game=game)
      
@web_app.route('/games/<game_id>/edit', methods=['POST'])
def edit_game_submission(game_id):
    try:
        game = Game.query.get(game_id)
        # Get each variable to be updated from the request form
        game.name = request.form["name"].lower()
        game.age_rating = request.form["age_rating"]
        category_id = Category.query.filter_by(name=request.form["category"].lower()).first().id
        game.category_id = category_id
        developer_id = Developer.query.filter_by(name=request.form["developer"].lower()).first().id
        game.developer_id = developer_id
        game.image_link = request.form["image_link"]
        # Update the instance
        game.update()
        flash('The game with id '+game_id+' has been successfully updated!')
        return redirect(url_for('web_app.show_game', game_id=game_id))
    except:
        abort(422)

@web_app.route('/categories')
def get_categories():
    # Query all categories
    categories = Category.query.order_by(Category.id).all()
    # Format categories
    formatted_categories = [category.format() for category in categories]
    # Render corresponding page
    return render_template('pages/categories.html', categories=formatted_categories, categories_count=len(formatted_categories))

@web_app.route('/categories/create')
def create_category():
    # specify the form to be shown
    form = CategoryForm()
    return render_template('forms/new_category.html', form=form)

@web_app.route('/categories/create', methods=['POST'])
def create_category_submission():
    try:
        # Create Category instance with user inputs
        category = Category(
            name = request.form["name"].lower(),
            description = request.form["description"]
        )
        # Insert the instance into the db
        category.insert()
        flash(request.form['name']+' category was successfully listed!')
        return redirect(url_for('web_app.get_categories'))
    except:
        abort(422)

@web_app.route('/categories/<category_id>')
def show_category(category_id):
    # Query the category
    category = Category.query.get(category_id)
    if category is None:
        abort(404)
    # Query the games that are associated with the passed category id
    games = Game.query.filter_by(category_id=category_id).all()
    # Format games
    formatted_games = [game.format() for game in games]
    return render_template('pages/show_category.html', category=category, games=formatted_games, games_count=len(formatted_games))
    
@web_app.route('/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    # Query the category to be deleted
    category = Category.query.get(category_id)
    # If the given id does not exist
    if category is None:
        abort(404)
    try:
        # If the category was found delete it and return to home page
        category.delete()
        flash('Category with id '+category_id+' has been deleted successfully!')
        return redirect(url_for('web_app.index'))
    except:
        abort(422)

@web_app.route('/categories/<category_id>/edit')
def edit_category(category_id):
    category = Category.query.get(category_id)
    # If the category does not exist
    if category is None:
        abort(404)
    # Specify the form to be shown
    form = CategoryForm()
    return render_template('forms/edit_category.html', form=form, category=category)
      
@web_app.route('/categories/<category_id>/edit', methods=['POST'])
def edit_category_submission(category_id):
    try:
        # Query the category
        category = Category.query.get(category_id)
        # Get each variable to be updated from the request form
        category.name = request.form["name"].lower()
        category.description = request.form["description"]
        # Update the instance
        category.update()
        flash('The Category with id '+category_id+' has been successfully updated!')
        return redirect(url_for('web_app.show_category', category_id=category_id))
    except:
        abort(422)

@web_app.route('/developers')
def get_developers():
    # Query all developers
    developers = Developer.query.order_by(Developer.id).all()
    # Format developers
    formatted_developers = [developer.format() for developer in developers]
    # Render corresponding page
    return render_template('pages/developers.html', developers=formatted_developers, developers_count=len(formatted_developers))

@web_app.route('/developers/create')
def create_developer():
    # Specify form to be shown
    form = DeveloperForm()
    return render_template('forms/new_developer.html', form=form)

@web_app.route('/developers/create', methods=['POST'])
def create_developer_submission():
    try:
        # Create a Developer instance with the passed inputs
        developer = Developer(
            name = request.form["name"].lower(),
            website = request.form["website"]
        )
        # Insert the instance into the db
        developer.insert()
        flash(request.form['name']+' developer was successfully listed!')
        return redirect(url_for('web_app.get_developers'))
    except:
        abort(422)

@web_app.route('/developers/<developer_id>')
def show_developer(developer_id):
    # Query the developer
    developer = Developer.query.get(developer_id)
    # If developer does not exist
    if developer is None:
        abort(404)
    # Query games associated with the developer
    games = Game.query.filter_by(developer_id=developer_id).all()
    # Format games
    formatted_games = [game.format() for game in games]
    return render_template('pages/show_developer.html', developer=developer, games=formatted_games, games_count=len(formatted_games))
    
@web_app.route('/developers/<developer_id>', methods=['DELETE'])
def delete_developer(developer_id):
    try:
        # Query the developer to be deleted
        developer = Developer.query.get(developer_id)
        # If the given id does not exist
        if developer is None:
            abort(404)
        else:
            # If the developer was found delete it and return to home page
            developer.delete()
            flash('Developer with id '+developer_id+' has been deleted successfully!')
            return redirect(url_for('web_app.index'))
    except:
        abort(422)

@web_app.route('/developers/<developer_id>/edit')
def edit_developer(developer_id):
    # Query & filter Developer 
    developer = Developer.query.get(developer_id)
    # If the developer does not exist
    if developer is None:
        abort(404)
    # Specify form to be shown
    form = DeveloperForm()
    return render_template('forms/edit_developer.html', form=form, developer=developer)

@web_app.route('/developers/<developer_id>/edit', methods=['POST'])
def edit_developer_submission(developer_id):
    try:
        # Query the developer
        developer = Developer.query.get(developer_id)
        # Get each variable to be updated from the request form
        developer.name = request.form["name"].lower()
        developer.website = request.form["website"]
        # Update the instance
        developer.update()
        flash('The Developer with id '+developer_id+' has been successfully updated!')
        return redirect(url_for('web_app.show_developer', developer_id=developer_id))
    except:
        abort(422)

# Error Handlers
@web_app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404
    
@web_app.errorhandler(500)
def internal_server(error):
    return render_template('errors/500.html'), 500

@web_app.errorhandler(422)
def unprocessable(error):
    return render_template('errors/422.html'), 422

@web_app.errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html'), 400

@web_app.errorhandler(AuthError)
def auth_error(error):
    return render_template('errors/auth_errors.html', title=error.status_code, message=error.args[0]["description"])