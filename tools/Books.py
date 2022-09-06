from asyncio.windows_events import NULL
from distutils.log import debug
import os
from flask import Flask, flash, request, redirect, url_for, Blueprint, current_app
from werkzeug.utils import secure_filename
from flask import send_from_directory,render_template
import sqlite3
import datetime

app = Flask(__name__)
books = Blueprint('books',__name__,url_prefix='/books')
con = sqlite3.connect('Library.db', check_same_thread=False)
cur = con.cursor()



@books.route("/BOOKS/Books", methods=['GET', 'POST'])
def displayAllBooks():
    Books=[]
    for row in cur.execute('SELECT * FROM Books'):
        Books.append([row[0],row[1],row[2],row[3],row[4],row[5]])
    return render_template("/BOOKS/Books.html",Books = Books)


UPLOAD_FOLDER = 'UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@books.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@books.route('/upbook', methods=['GET', 'POST'])
def addBook():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sql =f'''INSERT INTO Books VALUES (NULL, '{filename}',
            '{request.form.get('name')}','{request.form.get('author')}',
            '{request.form.get('year')}','{request.form.get('type')}')'''
            cur.execute(sql)
            con.commit()
            return displayAllBooks()
    return render_template("/BOOKS/AddBook.html")


@books.route('/BOOKS/deleteBook/<bookid>')
def deleteBook(bookid):
    SQL =f"delete from Books where Id={bookid}"
    cur.execute(SQL)
    con.commit()
    return displayAllBooks()



@books.route('/BOOKS/searchBook',methods=['GET','POST'])
def searchbook():
    if request.method == 'POST':
        bookName = request.form.get('bookName')
        Books=[]
        for row in cur.execute('SELECT * FROM Books where Name = ?', [bookName]):
            Books.append([row[0],row[1],row[2],row[3],row[4],row[5]])
        print (Books)
        return render_template("/BOOKS/Books.html", Books = Books)
    return render_template("/BOOKS/Books.html")


#@app.route('/return/<bookid>')
#def returnBook(bookid):
#    return (f"return book : {bookid }" )