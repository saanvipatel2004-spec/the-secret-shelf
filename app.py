from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import sqlite3
import requests
import random
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "thesecretshelf_secret_key"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_TIMEOUT"] = 10


mail = Mail(app)

DATABASE = "bookstore.db"


def get_backup_books():
    return [
        {
            "id": "gatsby",
            "title": "The Great Gatsby",
            "authors": "F. Scott Fitzgerald",
            "description": "A classic American novel about wealth, love, and the American Dream.",
            "image": "https://covers.openlibrary.org/b/title/The%20Great%20Gatsby-M.jpg",
            "rating": 4.4,
            "price": 12.99
        },
        {
            "id": "mockingbird",
            "title": "To Kill a Mockingbird",
            "authors": "Harper Lee",
            "description": "A powerful novel about justice, morality, and growing up in the American South.",
            "image": "https://covers.openlibrary.org/b/title/To%20Kill%20a%20Mockingbird-M.jpg",
            "rating": 4.8,
            "price": 14.99
        },
        {
            "id": "nineteen84",
            "title": "1984",
            "authors": "George Orwell",
            "description": "A dystopian novel about surveillance, control, and political power.",
            "image": "https://covers.openlibrary.org/b/title/1984-M.jpg",
            "rating": 4.7,
            "price": 11.99
        },
        {
            "id": "pride",
            "title": "Pride and Prejudice",
            "authors": "Jane Austen",
            "description": "A romantic classic about manners, family, and social expectations.",
            "image": "https://covers.openlibrary.org/b/title/Pride%20and%20Prejudice-M.jpg",
            "rating": 4.6,
            "price": 10.99
        },
        {
            "id": "moby",
            "title": "Moby-Dick",
            "authors": "Herman Melville",
            "description": "A famous adventure novel about obsession, revenge, and the sea.",
            "image": "https://covers.openlibrary.org/b/title/Moby-Dick-M.jpg",
            "rating": 4.1,
            "price": 13.99
        },
        {
            "id": "janeeyre",
            "title": "Jane Eyre",
            "authors": "Charlotte Brontë",
            "description": "A classic novel about independence, love, and personal strength.",
            "image": "https://covers.openlibrary.org/b/title/Jane%20Eyre-M.jpg",
            "rating": 4.5,
            "price": 12.49
        },
        {
            "id": "frankenstein",
            "title": "Frankenstein",
            "authors": "Mary Shelley",
            "description": "A gothic novel about science, ambition, creation, and responsibility.",
            "image": "https://covers.openlibrary.org/b/title/Frankenstein-M.jpg",
            "rating": 4.3,
            "price": 9.99
        },
        {
            "id": "dracula",
            "title": "Dracula",
            "authors": "Bram Stoker",
            "description": "A famous gothic horror novel about Count Dracula and supernatural fear.",
            "image": "https://covers.openlibrary.org/b/title/Dracula-M.jpg",
            "rating": 4.2,
            "price": 10.49
        },
        {
            "id": "wuthering",
            "title": "Wuthering Heights",
            "authors": "Emily Brontë",
            "description": "A dramatic novel about love, revenge, class, and emotional conflict.",
            "image": "https://covers.openlibrary.org/b/title/Wuthering%20Heights-M.jpg",
            "rating": 4.0,
            "price": 11.49
        },
        {
            "id": "hobbit",
            "title": "The Hobbit",
            "authors": "J.R.R. Tolkien",
            "description": "A fantasy adventure novel about Bilbo Baggins and his unexpected journey.",
            "image": "https://covers.openlibrary.org/b/title/The%20Hobbit-M.jpg",
            "rating": 4.9,
            "price": 15.99
        },
        {
            "id": "catcher",
            "title": "The Catcher in the Rye",
            "authors": "J.D. Salinger",
            "description": "A coming-of-age novel about identity, alienation, and growing up.",
            "image": "https://covers.openlibrary.org/b/title/The%20Catcher%20in%20the%20Rye-M.jpg",
            "rating": 4.1,
            "price": 12.25
        },
        {
            "id": "f451",
            "title": "Fahrenheit 451",
            "authors": "Ray Bradbury",
            "description": "A dystopian novel about censorship, books, technology, and society.",
            "image": "https://covers.openlibrary.org/b/title/Fahrenheit%20451-M.jpg",
            "rating": 4.6,
            "price": 13.49
        }
    ]


def get_books():
    books = []

    url = "https://openlibrary.org/search.json"

    params = {
        "q": "classic novels",
        "limit": 100
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        print("Open Library Status Code:", response.status_code)
        print("Books found from Open Library:", len(data.get("docs", [])))

        for index, item in enumerate(data.get("docs", [])):
            title = item.get("title", "Unknown Title")

            authors_list = item.get("author_name", ["Unknown Author"])
            authors = ", ".join(authors_list[:2])

            first_year = item.get("first_publish_year", "Unknown Year")
            cover_id = item.get("cover_i")

            if cover_id:
                image = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
            else:
                image = "https://via.placeholder.com/150x220?text=No+Cover"

            rating = round(random.uniform(3.7, 5.0), 1)
            price = round(random.uniform(8.99, 29.99), 2)

            book = {
                "id": f"api_book_{index}",
                "title": title,
                "authors": authors,
                "description": f"A popular novel first published in {first_year}. This book is part of the The Secret Shelf online bookstore catalog.",
                "image": image,
                "rating": rating,
                "price": price
            }

            books.append(book)

        if len(books) == 0:
            return get_backup_books()

        return books

    except Exception as e:
        print("API failed, using backup books instead:", e)
        return get_backup_books()


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            total REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def send_confirmation_email(email, username, cart, total):
    book_list = ""

    for book in cart:
        book_list += f"- {book['title']} by {book['authors']} - ${book['price']}\n"

    subject = "Your The Secret Shelf Order Confirmation"

    body = f"""
Hello {username},

Thank you for shopping with The Secret Shelf!

Your order includes:

{book_list}

Order Total: ${total}

Thank you,
The Secret Shelf
"""

    print("")
    print("====================================")
    print("The Secret Shelf ORDER CONFIRMATION EMAIL")
    print("====================================")
    print(f"To: {email}")
    print(body)
    print("====================================")
    print("")

    try:
        msg = Message(
            subject,
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )

        msg.body = body
        mail.send(msg)

        print("Real email sent successfully.")

    except Exception as e:
        print("Real email failed to send.")
        print("Error:", e)


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/create_profile", methods=["GET", "POST"])
def create_profile():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()

        try:
            conn.execute("""
                INSERT INTO users (username, password)
                VALUES (?, ?)
            """, (username, hashed_password))

            conn.commit()
            conn.close()

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            conn.close()
            return "That username already exists. Go back and choose another username."

    return render_template("create_profile.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            session["cart"] = []
            return redirect(url_for("books"))

        return "Invalid username or password. Go back and try again."

    return render_template("login.html")


@app.route("/books")
def books():
    if "username" not in session:
        return redirect(url_for("login"))

    books = get_books()

    return render_template("books.html", books=books)


@app.route("/add_to_cart/<book_id>")
def add_to_cart(book_id):
    if "username" not in session:
        return redirect(url_for("login"))

    if "cart" not in session:
        session["cart"] = []

    # Get the full book catalog again
    catalog = get_books()

    selected_book = None

    for book in catalog:
        if book["id"] == book_id:
            selected_book = book
            break

    if selected_book:
        cart = session.get("cart", [])
        cart.append(selected_book)
        session["cart"] = cart
        session.modified = True
        print("Book added to cart:", selected_book["title"])
        print("Cart now has:", len(session["cart"]), "items")
    else:
        print("Book was not found. ID:", book_id)

    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    if "username" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", [])

    total = 0

    for book in cart:
        total += book["price"]

    total = round(total, 2)

    return render_template("cart.html", cart=cart, total=total)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "username" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", [])

    if len(cart) == 0:
        return redirect(url_for("cart"))

    total = 0

    for book in cart:
        total += book["price"]

    total = round(total, 2)

    if request.method == "POST":
        email = request.form["email"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO orders (username, email, total)
            VALUES (?, ?, ?)
        """, (session["username"], email, total))

        conn.commit()
        conn.close()

        send_confirmation_email(email, session["username"], cart, total)

        session["cart"] = []

        return render_template("confirmation.html", total=total, email=email)

    return render_template("checkout.html", cart=cart, total=total)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


create_database()

if __name__ == "__main__":
    app.run(debug=True)
