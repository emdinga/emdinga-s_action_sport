def main():
    # Create an instance of the Database class with the database name
    db = Database()

    # Create tables in the database
    db.create_tables()

    # Insert some data into the User table
    db.insert_user('John', 'Doe', '123456789', '', '')

    # Fetch data from the User table
    users = db.fetch_users()
    print(users)

    # Close the database connection
    db.close_connection()
