import unittest
import os
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Game, Category, Developer

TOKEN = str('Bearer ' + os.environ['OWNER_TOKEN'])


class GamifyTestCase(unittest.TestCase):
    '''
    This class represents the gamify test case
    '''

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': TOKEN}
        self.database_name = "gamify_test"
        self.database_path = "postgres://{}@{}/{}".format(
            'mashaelmohammed', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path, self.database_name)

        # bind the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        ''' Executed after each test '''
        pass

    # Success behavior of retrieving paginated games
    def test_get_paginated_games(self):
        res = self.client().get('/api/games')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_games'])
        self.assertTrue(len(data['games']))

    # Failure behavior of sending a beyond valid page request
    def test_404_games_request_beyond_valid_page(self):
        res = self.client().get('/api/games?page=20')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of searching for a game
    def test_search_game(self):
        res = self.client().get('/api/search?q=v')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Failure behavior of searching with an empty input
    def test_search_with_empty_term(self):
        res = self.client().get('/api/search?q=')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # success behavior of creating a new game
    def test_create_new_game(self):
        new_game = {
            'name': 'overwatch',
            'age_rating': '+16',
            'category_id': 2,
            'developer_id': 1,
            'image_link': 'https://upload.wikimedia.org/wikipedia/en/5/51/'
            'Overwatch_cover_art.jpg'
        }

        res = self.client().post(
            '/api/games',
            json=new_game,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['game'])

    # Failure behavior of creating a game with missing information
    def test_400_game_creation_fails(self):
        new_game = {
            'name': 'black ops',
            'age_rating': '+18'
        }

        res = self.client().post(
            '/api/games',
            json=new_game,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Success behavior of retrieving game details
    def test_show_game(self):
        res = self.client().get('/api/games/2', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['game'])

    # Failure behavior of retrieving a game's details that doesn't exist
    def test_show_404_game_not_found(self):
        res = self.client().get('/api/games/100', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of deleting a game
    def test_delete_game(self):
        res = self.client().delete('/api/games/3', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    # Failure behavior of deleting a game
    def test_delete_404_game_not_found(self):
        res = self.client().delete('/api/games/100', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of editting a game
    def test_edit_game(self):
        updated_game = {
            'name': 'ow',
            'age_rating': '+18',
            'category_id': 2,
            'developer_id': 2,
            'image_link': 'https://www.gametutorials.com/wp-content/'
            'uploads/2020/08/overwatch-characters.jpg'
        }
        res = self.client().patch(
            '/api/games/2',
            json=updated_game,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    # Failure behavior of editing a game (sending missing information)
    def test_400_game_edit_fails(self):
        updated_game = {
            'name': 'ow',
            'age_rating': '+18'
        }

        res = self.client().patch(
            '/api/games/2',
            json=updated_game,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Failure behavior of editing a game (edit a game that does not exist)
    def test_edit_404_game_not_found(self):
        updated_game = {
            'name': 'ow',
            'age_rating': '+18',
            'category_id': 1,
            'developer_id': 1,
            'image_link': 'https://www.gametutorials.com/wp-content/'
            'uploads/2020/08/overwatch-characters.jpg'
        }

        res = self.client().patch(
            '/api/games/100',
            json=updated_game,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of retrieving paginated categories
    def test_get_paginated_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    # Failure behavior by sending a beyond valid page request
    def test_404_categories_request_beyond_valid_page(self):
        res = self.client().get('/api/categories?page=20')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of creating a new category
    def test_create_new_category(self):
        new_category = {
            'name': 'Simulation',
            'description': 'they\'re all designed to emulate real or'
            'fictional reality, to simulate a real situation or event.'
        }

        res = self.client().post(
            '/api/categories',
            json=new_category,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['category'])

    # Failure behavior of creating a category (sending missing information)
    def test_400_category_creation_fails(self):
        new_category = {
            'name': 'Action'
        }

        res = self.client().post(
            '/api/categories',
            json=new_category,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Success behavior of retrieving a category's details
    def test_show_category(self):
        res = self.client().get('/api/categories/2', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['category'])

    # Failure behavior of retrieving category details (retrieving the details
    # of a category that doesn't exist)
    def test_show_404_category_not_found(self):
        res = self.client().get('/api/categories/100', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of deleting a category
    def test_delete_category(self):
        res = self.client().delete('/api/categories/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    # Failure behavior of deleting a category (category doesn't exist)
    def test_delete_404_category_not_found(self):
        res = self.client().delete('/api/categories/100', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of editing a category
    def test_edit_category(self):
        updated_category = {
            'name': 'Puzzle Games',
            'description': 'Puzzle or logic games usually take place'
            'on a single screen or playfield and require the player'
            'to solve a problem to advance the action.'
        }
        res = self.client().patch(
            '/api/categories/2',
            json=updated_category,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    # Failure behavior of editing a category (missing information)
    def test_400_category_edit_fails(self):
        updated_category = {
            'name': 'Strategy'
        }

        res = self.client().patch(
            '/api/categories/2',
            json=updated_category,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Failure behavior of editing a category (category doesn't exist)
    def test_edit_404_category_not_found(self):
        updated_category = {
            'name': 'Strategy',
            'description': 'With gameplay is based on traditional'
            'strategy board games, strategy games give players a godlike'
            'access to the world and its resources. These games require'
            'players to use carefully developed strategy and tactics to'
            'overcome challenges. More recently, these type of games have'
            'moved from turn-based systems to real-time gameplay in'
            'response to player feedback.'
        }

        res = self.client().patch(
            '/api/categories/100',
            json=updated_category,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of retrieving paginated developers
    def test_get_paginated_developers(self):
        res = self.client().get('/api/developers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_developers'])
        self.assertTrue(len(data['developers']))

    # Failure behavior of retrieving developers (request a beyond valid page)
    def test_404_developers_request_beyond_valid_page(self):
        res = self.client().get('/api/developers?page=20')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of creating a developer
    def test_create_new_developer(self):
        new_developer = {
            'name': 'riot',
            'website': 'www.riotgames.com'
        }
        res = self.client().post(
            '/api/developers',
            json=new_developer,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['developer'])

    # Failure behavior of creating a developer
    def test_400_developer_creation_fails(self):
        new_developer = {
            'name': 'bungie'
        }

        res = self.client().post(
            '/api/developers',
            json=new_developer,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Success behavior of retrieving a developer details
    def test_show_developer(self):
        res = self.client().get('/api/developers/2', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['developer'])

    # Failure behavior of retrieving details of developer (developer doesn't
    # exist)
    def test_show_404_developer_not_found(self):
        res = self.client().get('/api/developers/100', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of deleting a developer
    def test_delete_developer(self):
        res = self.client().delete('/api/developers/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    # Failure behavior of deleting a developer (developer doesn't exist)
    def test_delete_404_developer_not_found(self):
        res = self.client().delete('/api/developers/100', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Success behavior of editing a developer
    def test_edit_developer(self):
        updated_developer = {
            'name': 'epic games',
            'website': 'www.epicgames.com'
        }
        res = self.client().patch(
            '/api/developers/2',
            json=updated_developer,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    # Failure behavior for edit a developer (missing information)
    def test_400_developer_edit_fails(self):
        updated_developer = {
            'name': 'bungie'
        }
        res = self.client().patch(
            '/api/developers/2',
            json=updated_developer,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Failure behavior of editing a developer (developer doesn't exist)
    def test_edit_404_developer_not_found(self):
        updated_developer = {
            'name': 'bungie',
            'website': 'www.bungie.net'
        }
        res = self.client().patch(
            '/api/developers/100',
            json=updated_developer,
            headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
