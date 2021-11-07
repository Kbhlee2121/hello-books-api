from werkzeug.exceptions import MethodNotAllowed
from app import db
from app.models.book import Book
from app.models.author import Author
from app.models.genre import Genre
from flask import Blueprint, jsonify, make_response, request

hello_world_bp = Blueprint("hello_world", __name__)
books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors",__name__,url_prefix="/authors")
genres_bp = Blueprint("genres", __name__, url_prefix="/genres")

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


        new_book = Book(
            title=request_body["title"],
            description = request_body["description"]
            )


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
        title_query = request.args.get("title")
        description_query = request.args.get("description")
        if title_query:
            books = Book.query.filter_by(title=title_query)
        else:
            books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return jsonify(books_response)

@books_bp.route("/<book_id>", methods = ["GET", "PUT", "DELETE"])
def handle_book(book_id):
    book = Book.query.get(book_id)
    # Edge case: if requested book_id not found
    if book is None:
            return make_response(f"Book {book_id} not found", 404)
    if request.method == "GET":
        # Flask returns dict into a response obj for us
        return {
            "id":book.id,
            "title":book.title,
            "description": book.description
        }
    elif request.method == "PUT":
        form_data = request.get_json()
        if "title" not in form_data or "description" not in form_data:
            return {"message": "Request requires both title and description"}, 400
        elif book is None:
            return make_response(f"Book {book_id} not found", 404)

        else:
            book.title = form_data["title"]
            book.description = form_data["description"]

            # Save action
            db.session.commit()

            return make_response(f"Book #{book.id} successfully updated")  

    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response (f"Book #{book.id} successfully deleted", 200)  

# AUTHOR ROUTES

@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    if "name" not in request_body:
        return make_response("Invalid Request", 400)

    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()
    return make_response(f"Author {new_author.name} successfully created", 201)

@authors_bp.route("", methods = ["GET"])
def read_all_authors():
    authors = Author.query.all()
    authors_response = []
    for author in authors:
        authors_response.append({
            "id": author.id,
            "name":author.name
        })
    return jsonify(authors_response)

@authors_bp.route("/<author_id>/books", methods=["GET","POST"])
def handle_authors_books(author_id):
    author = Author.query.get(author_id)
    if author is None:
        return make_response("Author not found", 404)
    if request.method == "POST":
        request_body = request.get_json()
        new_book = Book(
            title=request_body["title"],
            description=request_body["description"],
            author=author
        )

        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} by {new_book.author.name} successfully created", 201)

    elif request.method == "GET":
        books_response = []
        for book in author.books:
            books_response.append({
                "id":book.id,
                "title":book.title,
                "description": book.description,

            })
        return jsonify(books_response)
        



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

