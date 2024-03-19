import sqlite3

class Database:
    def __init__(self, db_name='indoor_booking.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create tables in the database"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                surname TEXT,
                cell_number TEXT,
                hashed_password TEXT,
                salt TEXT
            )
        ''')
        # Add other table creation statements here

        self.conn.commit()

    def insert_user(self, name, surname, cell_number, hashed_password, salt):
        """Insert a user into the User table"""
        self.cursor.execute('''
            INSERT INTO User (name, surname, cell_number, hashed_password, salt)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, surname, cell_number, hashed_password, salt))
        self.conn.commit()

    def fetch_users(self):
        """Fetch all users from the User table"""
        self.cursor.execute('SELECT * FROM User')
        return self.cursor.fetchall()

    def close_connection(self):
        """Close the database connection"""
        self.conn.close()
