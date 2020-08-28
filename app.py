# import packages
import os
from flask import (
    Flask, 
    request, 
)
from database.models import setup_db
from flask_cors import CORS
from logging import Formatter, FileHandler
from routes.web import web_app
from routes.api import api_app

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('config')
    setup_db(app)
    
    # Set up Cors, allowing access for all origins (*)
    CORS(app)

    app.register_blueprint(web_app)
    app.register_blueprint(api_app)

    # Set access-control-allow for headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
  
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

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)