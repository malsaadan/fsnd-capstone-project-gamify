import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Game, Category, Developer

class GamifyTestCase(unittest.TestCase):
    '''
    This class represents the gamify test case
    '''

    def setup(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        
        # bind the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()