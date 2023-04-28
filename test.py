
import sqlite3


connection = sqlite3.connect('recipes.db')
curs = connection.cursor()
curs.execute('delete from Requests where id = ? ', (2,))
connection.commit()