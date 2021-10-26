from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# db is a SQLAlchemy obj that is acting as a connection to the database
db = SQLAlchemy()
migrate = Migrate()

# postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development

def create_app(test_config=None):
    app = Flask(__name__)

    #DB Config
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    # Initializes SQLAlchemy and tells which application to work with
    db.init_app(app)
    # Tells Migrate which application to work with and the way to the database
    migrate.init_app(app, db)
    # Book needs to be imported after app.config so it is placed in this function
    # and not at the top
    # Imports models here:
    from app.models.book import Book

    # Register Blueprints here
    from .routes import hello_world_bp
    app.register_blueprint(hello_world_bp)

    from .routes import books_bp
    app.register_blueprint(books_bp)
    
    return app
