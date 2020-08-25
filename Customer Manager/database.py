import sqlite3 as sql   #imports the sql module for python

class Database:

    def __init__(self, db):    #i create a database class which will hold all the data for the customer

        self.conn = sql.connect(db)  #i connect the database to sql
        self.cursor = self.conn.cursor() #create a cursor to go through sql queiryes
        self.cursor.execute("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, cname text, clocation text, macid text, portal text, payment real, payrecieved integer)")  #i create a table called customers that has the following elements/types of values
        self.conn.commit() #commit the table



    def grab(self):

        self.cursor.execute("SELECT * FROM customers")     #it will select all the values from the table and return all of them 
        rows = self.cursor.fetchall() #returns rows in table
        return rows


    def add(self, name, location, macid, portal, payment, payrecieved ):

        with self.conn: #context manager --> commits the changes to the sql database
            self.cursor.execute("INSERT INTO customers VALUES (NULL, :name, :location, :macid, :portal, :payment,:payrecieved)", {'name': name, 'location': location, 
            'macid': macid, 'portal': portal, 'payment': payment, 'payrecieved': payrecieved})   #inserts the values of the following elements into the table


    def remove(self, id):

        with self.conn:    #removes the certain id from the table
            
            self.cursor.execute("DELETE FROM customers WHERE id = :id", {'id':id})


    def update(self, id, name, location, macid, portal, payment, payrecieved ):   #updates the table with new values 

        with self.conn:

            self.cursor.execute("UPDATE customers SET cname  = ?, clocation = ?, macid = ?, portal = ?, payment = ?, payrecieved = ? WHERE id = ?", (name, 
            location, macid, portal, payment, payrecieved, id))


    def __del__(self):

        self.conn.close()

 
class MoneyBase:       #same thing as database class, but this holds the money data 

    def __init__(self, db):

        self.conn = sql.connect(db)
        self.cursor = self.conn.cursor() #creates another table called moneystorage which will hold the money earned through the customers
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS moneystorage (    

                money real

        )""")


        self.conn.commit()

    def insert(self):

        with self.conn:
 
            self.cursor.execute("INSERT INTO moneystorage VALUES(0.0)")      #starts the money off with a 0

    def restart(self):

        with self.conn:
            self.cursor.execute("UPDATE moneystorage SET money = ?", (0.0,))   #everytimee a clear button is clicked, it will restart the money from 0

    def update_money(self, addedmoney):

        with self.conn:
            self.cursor.execute("UPDATE moneystorage SET money = ?", (addedmoney,))   #updates the money to the new value

    def grab_money(self):
 
        self.cursor.execute("SELECT money FROM moneystorage")  #returns the value of the money to be displayed
        return self.cursor.fetchone()

    def __del__(self):

        self.conn.close()


    

