#!/usr/bin/env python3
"""entry"""

from flask import Flask, render_template,request, jsonify
from database.database import Database

app = Flask(__name__)

@app.route('/')
def index():
    """root of the project"""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
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
    with app.app_context():
        app.run(host='0.0.0.0', port=5000, debug=True)
