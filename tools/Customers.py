from asyncio.windows_events import NULL
from distutils.log import debug
import os
from flask import Flask, flash, request, redirect, url_for, Blueprint
from werkzeug.utils import secure_filename
from flask import send_from_directory,render_template
import sqlite3
import datetime

customers = Blueprint('customers',__name__,url_prefix='/customers')
con = sqlite3.connect('Library.db', check_same_thread=False)
cur = con.cursor()

@customers.route("/CUSTOMERS/Customers", methods=['GET', 'POST'])
def Customers():
    Query = "SELECT * FROM Customers"
    cur.execute(Query)
    Customers = cur.fetchall()
    return render_template("/CUSTOMERS/Customers.html", Customers = Customers)
    
@customers.route('/CUSTOMERS/deleteCust/<custid>')
def deleteCust(custid):
    SQL =f"delete from Customers where Id={custid}"
    cur.execute(SQL)
    con.commit()
    return Customers()
    

@customers.route('/CUSTOMERS/addCust',methods=['GET','POST'])
def addCust():
        if request.method == 'POST':
            custId = request.form.get('custId')
            custName = request.form.get('custName')
            custAge = request.form.get('custAge')
            try:
                cur.execute('INSERT INTO Customers VALUES (? ,?, ?)',(custId, custName, custAge))
                con.commit()
            except:pass
            return Customers()
        return render_template("/CUSTOMERS/AddCust.html")

@customers.route('/CUSTOMERS/searchCust',methods=['GET','POST'])
def searchcust():
    if request.method == 'POST':
        custName = request.form.get('custName')
        print(custName)
        cur.execute('SELECT Id, Name, Age FROM Customers where Name = ?', [custName])
        Customers = cur.fetchall()
        print (Customers)
        return render_template("/CUSTOMERS/Customers.html", Customers = Customers)
    return render_template("/CUSTOMERS/Customers.html")