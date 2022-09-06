
from asyncio.windows_events import NULL
import os
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename
from flask import send_from_directory,render_template
import sqlite3
from tools.Books import books, displayAllBooks
from tools.Customers import customers
from tools.Loans import loans
from tools.DAL import init_db


app = Flask(__name__)
app.register_blueprint(customers)
app.register_blueprint(books)
app.register_blueprint(loans)

init_db()

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

con = sqlite3.connect('Library.db',check_same_thread = False)
cur = con.cursor()



if __name__ == '__main__':
    app.run(debug=True, port = 9000)
