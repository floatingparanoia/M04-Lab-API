from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# set up SQLAchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Book{self.book_name}>'
 
 
 # CRUD routes
@app.route('/books', methods=['POST'])
# Create new book
def add_book():
    data = request.get_json()
    new_book = Book(
        book_name=data['book_name'],
        author=data['author'],
        publisher=data['publisher']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/books', methods=['GET'])
# Retrieve All Books
def get_books():
    books = Book.query.all()
    books_list = []
    for book in books:
        books_list.append({
            'id': book.id,
            'book_name': book.book_name,
            'author': book.author,
            'publisher': book.publisher
        })
    return jsonify(books_list)

@app.route('/books/<int:id>', methods=['GET'])
# retrieve a single book
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'book_name': book.book_name,
        'author': book.author,
        'publisher': book.publisher
    })
    
@app.route('/books/<int:id>', methods=['PUT'])
# Update a book
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    
    book.book_name = data.get('book_name', book.book_name)
    book.author = data.get('author', book.author)
    book.publisher = data.get('publisher', book.publisher)
    
    db.session.commit()
    return jsonify({'message': 'Book update successful'})

@app.route('/books/<int:id>', methods=['DELETE'])
# delete a book
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Deleted Book'})

# Run Application
if __name__ == '__main__':
    app.run(debug=True)