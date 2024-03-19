#!/usr/bin/env python3
"""database"""
import sqlite3


class Database:
    def __init__(self, db_name='indoor_booking.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create User table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                surname TEXT,
                cell_number TEXT,
                password TEXT
            )
        ''')

        """Create Booking table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Booking (
                booking_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                facility_id INTEGER,
                booking_type TEXT,
                duration INTEGER,
                payment_method TEXT,
                payment_status TEXT,
                FOREIGN KEY (user_id) REFERENCES User(user_id)
            )
        ''')

        """Create Payment Transaction table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PaymentTransaction (
                transaction_id INTEGER PRIMARY KEY,
                booking_id INTEGER,
                amount REAL,
                payment_method TEXT,
                transaction_status TEXT,
                timestamp TEXT,
                FOREIGN KEY (booking_id) REFERENCES Booking(booking_id)
            )
        ''')

        """Create Indoor Game Facility table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS IndoorGameFacility (
                facility_id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT,
                capacity INTEGER,
                availability TEXT
            )
        ''')

        self.conn.commit()

    def close_connection(self):
        self.conn.close()
