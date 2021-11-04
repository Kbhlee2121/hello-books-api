from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# db is a SQLAlchemy obj that is acting as a connection to the database
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

# postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development

def create_app(test_config=None):
    app = Flask(__name__)

    #DB Config
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if not test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')

    # Initializes SQLAlchemy and tells which application to work with
    db.init_app(app)
    # Tells Migrate which application to work with and the way to the database
    migrate.init_app(app, db)
    # Book needs to be imported after app.config so it is placed in this function
    # and not at the top
    # Imports models here:
    from app.models.book import Book
    from app.models.author import Author

    # Register Blueprints here
    from .routes import hello_world_bp
    app.register_blueprint(hello_world_bp)

    from .routes import books_bp
    app.register_blueprint(books_bp)

    from .routes import authors_bp
    app.register_blueprint(authors_bp)
    
    return app
