from asyncio.windows_events import NULL
from distutils.log import debug
import os
from flask import Flask, flash, request, redirect, url_for,Blueprint
from werkzeug.utils import secure_filename
from flask import send_from_directory,render_template
import sqlite3
import datetime

loans = Blueprint('loans',__name__,url_prefix='/loans')
con = sqlite3.connect('Library.db', check_same_thread=False)
cur = con.cursor()


@loans.route("/LOANS/CustLoans/<custid>")
def custDetails(custid, msg = ''):
    Query = f'''SELECT Customers.Id, Customers.Name, Books.Id, Books.Name, 
                Books.Type, Loandate, Returndate
                FROM Loans
                INNER JOIN Customers ON Loans.CustID = Customers.Id
                INNER JOIN Books ON Loans.BookID = Books.Id
                WHERE CustID = {custid}
                ORDER BY 3'''
    cur.execute(Query)
    custLoans = cur.fetchall()
    lateLoans = []
    goodLoans = []
    for custLoan in custLoans:
        if custLoan[6] != 0:
            goodLoans.append(custLoan)
        else:    
            now = datetime.datetime.now()
            then = datetime.datetime.strptime(custLoan[5], '%d-%m-%Y')
            diff = now - then
            if custLoan[4] == 1:
                if diff.days > 10:
                    lateLoans.append(custLoan)
                else:
                    goodLoans.append(custLoan)   
            elif custLoan[4] == 2:
                if diff.days > 5:
                    lateLoans.append(custLoan)
                else:
                    goodLoans.append(custLoan)    
            elif custLoan[4] == 3:
                if diff.days > 2:
                    lateLoans.append(custLoan)
                else:
                    goodLoans.append(custLoan)    
    return render_template("/LOANS/CustLoans.html", lateLoans = lateLoans, 
    goodLoans = goodLoans, custid = custid, msg = msg)

@loans.route("/LOANS/LoanBook/<custid>", methods=['GET', 'POST'])
def chooseBooks(custid):
    Books=[]
    for row in cur.execute('SELECT * FROM Books'):
        Books.append([row[0],row[1],row[2],row[3],row[4],row[5]])
    return render_template("/LOANS/LoanBook.html",Books = Books, custid = custid)

@loans.route("/Loan/<custid>/<bookid>")  
def loan(custid, bookid):
    global msg
    msg = ''
    # check if the book is on loan, else loan the book
    cur.execute('SELECT BookID FROM Loans WHERE BookID = ? AND Returndate = ?', (bookid, NULL))
    bookloan = cur.fetchall()
    if len(bookloan) == 0:
        today = datetime.datetime.now()
        fulltoday = today.strftime("%d-%m-%Y")
        #fulltoday = '26-04-2022'
        cur.execute('INSERT INTO Loans VALUES ( ?, ?, ?, ?)',(custid, bookid, fulltoday, NULL))
        con.commit()
    else:
        msg = "The book is on loan, please select anothr book"
    return custDetails(custid, msg)

@loans.route("/Return/<custid>/<bookid>")  
def returnbook(custid, bookid):
    global msg
    today = datetime.datetime.now()
    fulltoday = today.strftime("%d-%m-%Y")
    cur.execute('UPDATE Loans SET Returndate = ? WHERE CustID = ? AND BookID = ?',(fulltoday, custid, bookid))
    con.commit()
    msg = ''
    return custDetails(custid, msg)