#!/usr/bin/env python3
"""entry"""

from flask import Flask, render_template,request, jsonify, session
from database.database import Database
import secrets, hashlib, bcrypt


db = Database('indoor_booking.db')
app = Flask(__name__)

@app.route('/')
def index():
    """root of the project"""
    return render_template('index.html')

@app.route('/dasgboard')
def dashboard():
    """dashboard of the project"""
    return render_template('dashbaord.html')

@app.route('/login')
def login_page():
    """Render the login page"""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    """Handle POST request to authenticate user login"""
    data = request.json
    cell_number = data.get('cell_number')
    password = data.get('password')

    """Query database to retrieve user data by cell number"""
    db.cursor.execute('''
        SELECT user_id, name, hashed_password, salt FROM User WHERE cell_number = ?
    ''', (cell_number,))
    user_data = db.cursor.fetchone()

    if user_data:
        user_id, user_name, hashed_password, salt = user_data
        """Hash the password provided by the user with the retrieved salt"""
        hashed_input_password = hashlib.sha256((password + salt).encode()).hexdigest()
        if hashed_input_password == hashed_password:
            """Save the user's name and ID in the session"""
            session['user_name'] = user_name
            session['user_id'] = user_id
            return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Login failed"}), 401

@app.route('/register', methods=['GET'])
def show_registration_form():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_user():
    try:
        """Extract registration data from the request"""
        name = request.form['name']
        surname = request.form['surname']
        cell_number = request.form['cell_number']
        password = request.form['password']

        """Hash and salt the password"""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

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
        ''', (name, surname, cell_number, hashed_password.decode('utf-8')))
        db.conn.commit()

        """ Store user name in the session """
        session['user_name'] = name

        """ Redirect to registration successful page"""
        return redirect('/registration-successful')

    except Exception as e:
        return f'Error occurred: {str(e)}'


@app.route('/registration-successful')
def registration_success():
    return render_template('registration_succ.html')


if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0', port=5000, debug=True)
