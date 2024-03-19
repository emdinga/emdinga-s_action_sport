#!/usr/bin/env python3
"""entry"""

from flask import Flask, render_template,request, jsonify
from database.database import Database


db = Database('indoor_booking.db')
app = Flask(__name__)

@app.route('/')
def index():
    """root of the project"""
    return render_template('index.html')

from flask import render_template

@app.route('/login')
def login_page():
    """Render the login page"""
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def show_registration_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        """Extract registration data from the request"""
        name = request.form['name']
        surname = request.form['surname']
        cell_number = request.form['cell_number']
        password = request.form['password']

        """Check if the cell number already exists in the database"""
        db.cursor.execute('''
            SELECT * FROM User WHERE cell_number = ?
        ''', (cell_number,))
        existing_user = db.cursor.fetchone()

        if existing_user:
            """If user already exists, return alert with message"""
            return jsonify({"message": "User already exists. Please recover your password."}), 400

        """Insert user data into the database"""
        db.cursor.execute('''
            INSERT INTO User (name, surname, cell_number, password)
            VALUES (?, ?, ?, ?)
        ''', (name, surname, cell_number, password))
        db.conn.commit()

        """Redirect to registration successful page"""
        return redirect('/registration-successful')
    except Exception as e:
        return f'Error occurred: {str(e)}'

@app.route('/registration-successful')
def registration_success():
    return render_template('registration_succ.html')


if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0', port=5000, debug=True)
