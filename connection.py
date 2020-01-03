import sqlite3


def connection():
    conn = sqlite3.connect('test.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    return conn, c

#conn = sqlite3.connect('test.db')

#Cursor which is used to execute SQL queries.
#c = conn.cursor()

#Wrap SQL in three quotation marks: allows a string to be multiple lines
#without needing special breaks.


#print(c.fetchall())

#conn.commit()

#conn.close()