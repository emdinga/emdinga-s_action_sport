from database import Database

# Create an instance of the Database class with the database name
db = Database('indoor_booking.db')

# Create tables in the database
db.create_tables()

# Insert some data into the User table
db.cursor.execute('''
    INSERT INTO User (name, surname, cell_number, hashed_password, salt)
    VALUES (?, ?, ?, ?, ?)
''', ('John', 'Doe', '123456789', '', '',))

# Commit the changes
db.conn.commit()

# Fetch data from the User table
db.cursor.execute('SELECT * FROM User')
users = db.cursor.fetchall()
print(users)

# Close the database connection
db.close_connection()
