from flask import (
    Blueprint,
    request, 
    abort, 
    jsonify,
    render_template,
    redirect,
    url_for,
    flash
)
from database.models import Game, Category, Developer
from auth.auth import AuthError, requires_auth
from flask_wtf import Form
from forms import *

api_app = Blueprint('api_app', __name__)

@api_app.route('/api/games')
def get_games():
    # Query all games from the db
    games = Game.query.order_by(Game.id).all()
    # Format all games
    formatted_games = [game.format() for game in games]

    return jsonify({
        'success': True,
        'total_games': len(formatted_games),
        'games': formatted_games
    })
  
# Search method
@api_app.route('/api/search')
def search_game():
    # Get the search term from parameter
    search_term = request.args['q']
    # If the submitted key term is empty
    if search_term == '':
        abort(400)

    else:
        # Query games from the database and filter them by name which matches the search term
        search_results = Game.query.filter(Game.name.ilike(f'%{search_term}%')).all()
        # Format the results
        formatted_results = [result.format() for result in search_results]
        return jsonify({
            'success': True,
            'search_results': formatted_results,
            'num_results': len(formatted_results)
        })

@api_app.route('/api/games', methods=['POST'])
@requires_auth('post:games')
def create_game(payload):
    body = request.get_json()
    # If the request doesn't contain the below keys return 400
    if not ('name' in body and 'age_rating' in body and 'category_id' in body and 'developer_id' in body and 'image_link' in body):
        abort(400)
    try:
        # Create a game instance
        game = Game(
            name = body.get('name'),
            age_rating = body.get('age_rating'),
            category_id = body.get('category_id'),
            developer_id = body.get('developer_id'),
            image_link = body.get('image_link')
        )
        # Create the record
        game.insert()

        return jsonify({
            "success": True,
            "game": game.format()
        })
    except:
        abort(422)

@api_app.route('/api/games/<game_id>')
@requires_auth('get:game-details')
def show_game(payload, game_id):
    # Get the selected game
    game = Game.query.filter_by(id=game_id).one_or_none()
    # If the game does not exist then abort
    if game is None:
        abort(404)

    return jsonify({
        "success": True,
        "game": game.format()
    })

@api_app.route('/api/games/<game_id>', methods=['DELETE'])
@requires_auth('delete:games')
def delete_game(payload, game_id):
    # Query the game to be deleted
    game = Game.query.get(game_id)
    # If the given id does not exist then abort 404 (was not found)
    if game is None:
        abort(404)
    try:
        game.delete()
        games = Game.query.all()
        return jsonify({
            "success": True,
            "deleted": game.id,
            "games": [game.format() for game in games]
        })
    except:
        abort(422)
      
@api_app.route('/api/games/<game_id>', methods=['PATCH'])
@requires_auth('edit:games')
def edit_game(payload, game_id):
    # Query the game
    game = Game.query.get(game_id)
    # If the game does not exist
    if game is None:
        abort(404)
    # Get body from the request
    body = request.get_json()
    # If the request doesn't contain the below keys return 400
    if not ('name' in body and 'age_rating' in body and 'category_id' in body and 'developer_id' in body and 'image_link' in body):
        abort(400)

    try:
        # Get each variable to be updated from the body
        game.name = body.get('name')
        game.age_rating = body.get('age_rating')
        game.category_id = body.get('category_id')
        game.developer_id = body.get('developer_id')
        game.image_link = body.get('image_link')
        # Update the instance
        game.update()
        # Query all games to return it in the response
        games = Game.query.order_by(Game.id).all()
        return jsonify({
            'success': True,
            'updated': game_id,
            'games': [game.format() for game in games]
            })
    except:
        abort(422)

@api_app.route('/api/categories')
def get_categories():
    # Query all categories
    categories = Category.query.order_by(Category.id).all()
    # Format categories
    formatted_categories = [category.format() for category in categories]
    return jsonify({
        "success": True,
        "categories": formatted_categories,
        "total_categories": len(formatted_categories)
    })

@api_app.route('/api/categories', methods=['POST'])
@requires_auth('post:categories')
def create_category(payload):
    body = request.get_json()
    # If the request doesn't contain the below keys return 400
    if not ('name' in body and 'description' in body):
        abort(400)
    try:
        # Create Category instance
        category = Category(
            name = body.get('name'),
            description = body.get('description')
        )
        # Insert the instance into the db
        category.insert()
        return jsonify({
            "success": True,
            "category": category.format()
        })
    except:
        abort(422)

@api_app.route('/api/categories/<category_id>')
@requires_auth('get:category-details')
def show_category(payload, category_id):
    # Query the category
    category = Category.query.get(category_id)
    if category is None:
        abort(404)
    # Query the games that are associated with the passed category id
    games = Game.query.filter_by(category_id=category_id).all()
    # Format games
    formatted_games = [game.format() for game in games]
    return jsonify({
        "success": True,
        "category": category.format(),
        "total_games": len(formatted_games),
        "games": formatted_games
    })
    
@api_app.route('/api/categories/<category_id>', methods=['DELETE'])
@requires_auth('delete:games')
def delete_category(payload, category_id):
    # Query the category to be deleted
    category = Category.query.get(category_id)
    # If the given id does not exist
    if category is None:
        abort(404)
    try:
        # If the category was found delete it 
        category.delete()
        categories = Category.query.all()
        return jsonify({
            "success": True,
            "deleted": category.id,
            "categories": [category.format() for category in categories]
        })
    except:
        abort(422)
 
@api_app.route('/api/categories/<category_id>', methods=['PATCH'])
@requires_auth('edit:games')
def edit_category(payload, category_id):
    # Query the category
    category = Category.query.get(category_id)
    # If the category does not exist
    if category is None:
        abort(404)
    body = request.get_json()
    # If the request doesn't contain the below keys return 400
    if not ('name' in body and 'description' in body):
        abort(400)
    try:
        # Get each variable to be updated from the body 
        category.name = body.get('name')
        category.description = body.get('description')
        # Update the instance
        category.update()
        categories = Category.query.order_by(Category.id).all()
        return jsonify({
            "success": True,
            "updated": category_id,
            "categories": [category.format() for category in categories]
        })
    except:
        abort(422)

@api_app.route('/api/developers')
def get_developers():
    # Query all developers
    developers = Developer.query.order_by(Developer.id).all()
    # Format developers
    formatted_developers = [developer.format() for developer in developers]
    return jsonify({
        "success": True,
        "developers": formatted_developers,
        "total_developers": len(formatted_developers)
    })

@api_app.route('/api/developers', methods=['POST'])
@requires_auth('post:games')
def create_developer(payload):
    body = request.get_json()
    # If the request doesn't contain the below keys return 400
    if not ('name' in body and 'website' in body):
        abort(400)
    try:
        # Create a Developer instance
        developer = Developer(
            name = body.get('name'),
            website = body.get('website')
        )
        # Insert the instance into the db
        developer.insert()
        return jsonify({
            "success": True,
            "developer": developer.format()
        })
    except:
        abort(422)

@api_app.route('/api/developers/<developer_id>')
@requires_auth('get:developer-details')
def show_developer(payload, developer_id):
    print(developer_id)
    # Query the developer
    developer = Developer.query.get(developer_id)
    # If developer does not exist
    if developer is None:
        abort(404)
    # Query games associated with the developer
    games = Game.query.filter_by(developer_id=developer_id).all()
    # Format games
    formatted_games = [game.format() for game in games]
    return jsonify({
        "success": True,
        "developer": developer.format(),
        "total_games": len(formatted_games),
        "games": formatted_games
    })

@api_app.route('/api/developers/<developer_id>', methods=['DELETE'])
@requires_auth('delete:developers')
def delete_developer(payload, developer_id):
    # Query the developer to be deleted
    developer = Developer.query.get(developer_id)
    # If the given id does not exist
    if developer is None:
        abort(404)
    try:
        # If the developer was found delete it
        developer.delete()
        developers = Developer.query.all()
        return jsonify({
            "success": True,
            "deleted": developer_id,
            "developers": [developer.format() for developer in developers]
        })
    except:
        abort(422)
    
@api_app.route('/api/developers/<developer_id>', methods=['PATCH'])
@requires_auth('edit:developers')
def edit_developer(payload, developer_id):
    # Query the developer
    developer = Developer.query.filter_by(id=developer_id).one_or_none()
    # If the developer does not exist 
    if developer is None:
        abort(404)
    body = request.get_json()
    # If the request doesn't contain the below keys return 400
    if not ('name' in body and 'website' in body):
        abort(400)
    try:
        # Get each variable to be updated from body
        developer.name = body.get("name")
        developer.website = body.get("website")
        # Update the instance
        developer.update()
        developers = Developer.query.order_by(Developer.id).all()
        return jsonify({
            "success": True,
            "updated": developer_id,
            "developers": [developer.format() for developer in developers]
        })
    except:
        abort(422)

# Error Handlers
@api_app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource Not Found'
    }), 404
    
@api_app.errorhandler(500)
def internal_server(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500

@api_app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
    }), 422

@api_app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

@api_app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.args[0]["description"]
    }), error.status_code