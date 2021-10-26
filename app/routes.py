from werkzeug.exceptions import MethodNotAllowed
from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request

hello_world_bp = Blueprint("hello_world", __name__)
books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods = ["POST", "GET"])
def handle_books():
    if request.method == "POST":
    # .get_json is a method that will give us the body of our request
        request_body = request.get_json()
        # Edge case: if description isn't included in request body

        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid Request", 400)

        # try: 
        #     if request_body["description"]:
        #         description_body = request["description"]
        # except:
        #     description_body = "no description"


        new_book = Book(title=request_body["title"],
                        description = request_body["description"])


        # staging changes like git add
        db.session.add(new_book)
        # committing changes
        db.session.commit()

        # explicit way of returning response: make_response
        return make_response(f"Book {new_book.title} successfully created", 201)
        # implicit way is by returning a tuple
        # return f"Book {new_book.title} successfully created", 201

    elif request.method == "GET":
        # query method returns a list of instances of books
        books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return jsonify(books_response)

@books_bp.route("/<book_id>", methods = ["GET"])
def handle_book(book_id):
    book = Book.query.get(book_id)
    # Edge case: if requested book_id not found
    if book is None:
        return make_response(f"Book {book_id} not found", 404)
    # Flask returns dict into a response obj for us
    return {
        "id":book.id,
        "title":book.title,
        "description": book.description
    }

# only accepts GET requests
@hello_world_bp.route("/hello-world", methods = ["GET"])
def get_hello_world():
    my_response = "Hello, World!"
    return my_response

@hello_world_bp.route("/hello-world/JSON", methods = ["GET"])
def hello_world_json():
    return {
        "name": "Kristin Lee", 
        "message": "Wassup!",
        "hobbies": ["Watching anime", "Traveling", "Eating dessert"],
    }, 200

@hello_world_bp.route("/broken-endpoint-with-broken-server-code")
def broken_endpoint():
    response_body = {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    new_hobby = "Surfing"
    response_body["hobbies"].append(new_hobby)
    return response_body
