#!/usr/bin/env python3
"""validation"""

from database.database import Database


db = Database('indoor_booking.db')

def validate_registration_data(data):
    """Validate user registration data"""
    name = data.get('name')
    surname = data.get('surname')
    cell_number = data.get('cell_number')

    if not name or not surname or not cell_number:
        return False, "Name, surname, and cell number are required fields"

    """Check if cell number already exists in the database"""
    db.cursor.execute('SELECT * FROM User WHERE cell_number = ?', (cell_number,))
    existing_user = db.cursor.fetchone()
    if existing_user:
        return False, "User with this cell number already exists"

    return True, ""

def validate_login_data(data):
    """Validate user login data"""
    cell_number = data.get('cell_number')

    if not cell_number:
        return False, "Cell number is required field"

    return True, ""
