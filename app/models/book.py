from app import db

# like any other class, but creating a __init__ func is not necessary
# can use the func that it inherits
# can also create own class functions like any other class
class Book (db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column (db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author", back_populates="books")
    # SQLAlchemy prefers singular tablenames
    # can change table name by this: 
    # __tablename = "books"

def to_string(self):
    return f"{self.id}: {self.title} Description: {self.description}"