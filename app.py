from flask import Flask, request, jsonify
import json

app = Flask(__name__)


BOOKS_FILE = 'books.json'


def read_books():

    try:
        with open(BOOKS_FILE, 'r') as f:
            books = json.load(f)
    except FileNotFoundError:
        books = []
    return books



def write_books(books):

    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f, )



def find_book_by_id(book_id):
    books = read_books()
    for book in books:
        if book['id'] == book_id:
            return book
    return None



@app.route('/books', methods=['GET'])
def get_all_books():
    books = read_books()
    return jsonify(books)



@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_details(book_id):
    book = find_book_by_id(book_id)
    if book:
        return jsonify(book)
    return jsonify({"message": "წიგნი ვერ მოიძებნა"}), 404



@app.route('/books', methods=['POST'])
def add_new_book():
    new_book_data = request.get_json()
    books = read_books()


    if not books:
        new_id = 1
    else:
        new_id = max([int(book['id']) for book in books]) + 1

    new_book_data['id'] = new_id


    required_fields = ['title', 'author', 'rate', 'status']
    for field in required_fields:
        if field not in new_book_data:
            return jsonify({"message": f"აუცილებელია ველის '{field}' მითითება"}), 400

    books.append(new_book_data)
    write_books(books)
    return jsonify({"message": "წიგნი წარმატებით დაემატა", "book": new_book_data}), 201



@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_data = request.get_json()
    books = read_books()
    found = False
    for i in range(len(books)):
        if books[i]['id'] == book_id:

            for key, value in updated_data.items():
                books[i][key] = value
            found = True
            break

    if found:
        write_books(books)
        return jsonify({"message": "წიგნი წარმატებით განახლდა", "book": books[1]})
    return jsonify({"message": "წიგნი ვერ მოიძებნა"}), 404


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    books = read_books()
    initial_len = len(books)

    books = [book for book in books if book['id'] != book_id]

    if len(books) < initial_len:
        write_books(books)
        return jsonify({"message": "წიგნი წარმატებით წაიშალა"})
    return jsonify({"message": "წიგნი ვერ მოიძებნა"}), 404



@app.route('/books/read', methods=['GET'])
def get_read_books():
    books = read_books()
    read_books_list = [book for book in books if book['status'] == 'read']
    return jsonify(read_books_list)



@app.route('/books/reading', methods=['GET'])
def get_reading_books():
    books = read_books()
    reading_books_list = [book for book in books if book['status'] == 'reading']
    return jsonify(reading_books_list)



@app.route('/books/to_read', methods=['GET'])
def get_to_read_books():
    books = read_books()
    to_read_books_list = [book for book in books if book['status'] == 'to-read']
    return jsonify(to_read_books_list)


if __name__ == '__main__':

    app.run(debug=True)
