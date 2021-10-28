import pytest 
from app import create_app
from app import db
from app.models.book import Book

# Creating own instance of app for testing
@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        # where we're going to return the instance of the app and pause
        yield app

    # drops all data from test (cleans up)
    with app.app_context():
        db.drop_all()

    # how we are going to call our routes
    # app parameter is coming from the other fixture
    # fixtures can depend on other fixtures
    @pytest.fixture
    def client(app):
        return app.test_client()

    @pytest.fixture
    def two_saved_books(app):
        # Arrange
        ocean_book = Book(title="Ocean Book",
                      description="watr 4evr")
        mountain_book = Book(title="Mountain Book",
                         description="i luv 2 climb rocks")

        db.session.add_all([ocean_book, mountain_book])
        # Alternatively, we could do
        # db.session.add(ocean_book)
        # db.session.add(mountain_book)
        db.session.commit()