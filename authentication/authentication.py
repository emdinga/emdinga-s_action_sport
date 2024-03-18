#!/usr/bin/env python3
"""authentication"""

from flask import Flask, request, jsonify
from database.database import Database


app = Flask(__name__)
db = Database('indoor_booking.db')

@app.route('/api/register', methods=['POST'])
def register_user():
    """Handle POST request to register a new user"""
    """Extract user data from request"""
    data = request.json
    name = data.get('name')
    surname = data.get('surname')
    cell_number = data.get('cell_number')
    """Insert user data into database"""
    db.cursor.execute('''
        INSERT INTO User (name, surname, cell_number)
        VALUES (?, ?, ?)
    ''', (name, surname, cell_number))
    db.conn.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login_user():
    """Handle POST request to authenticate user login"""
    """"Extract login credentials from request"""
    data = request.json
    cell_number = data.get('cell_number')
    """Query database to retrieve user data by cell number"""
    db.cursor.execute('''
        SELECT * FROM User WHERE cell_number = ?
    ''', (cell_number,))
    user = db.cursor.fetchone()
    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Login failed"}), 401

if __name__ == '__main__':
    app.run(debug=True)
