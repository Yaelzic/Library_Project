import sqlite3


con = sqlite3.connect('Library.db',check_same_thread = False)
cur = con.cursor()

def init_db():
    try:
        cur.execute('''CREATE TABLE Books 
            (Id INTEGER PRIMARY KEY AUTOINCREMENT, File_Name text,
            Name text, Author text, Year_Published INTEGER, Type INTEGER)''')
    
        cur.execute('''CREATE TABLE Customers 
           (Id INTEGER PRIMARY KEY, Name text,  Age INTEGER)''')
   
        #cur.execute('INSERT INTO Customers VALUES (? ,?, ?)',(318787546, 'yael', 24))
        #con.commit()
        #cur.execute('INSERT INTO Customers VALUES (? ,?, ?)',(312492168, 'yair', 28))
        #con.commit()
        #cur.execute('INSERT INTO Customers VALUES (? ,?, ?)',(226651271, 'shani', 20))
        #con.commit()
        cur.execute('''CREATE TABLE Loans 
           (CustID  INTEGER, BookID INTEGER, Loandate DATE, Returndate DATE,
            FOREIGN KEY(CustID) REFERENCES Customers(Id),
           FOREIGN KEY(BookID) REFERENCES Books(id))''')
    
    except:
            pass
    
    con.commit()
    #con.close()


def execute_sql(sql):
    return cur.execute(sql).fetchall()


def execute_sql_one_res(sql):
    return cur.execute(sql).fetchone()


def upd_sql(sql):
    cur.execute(sql)
    con.commit()      