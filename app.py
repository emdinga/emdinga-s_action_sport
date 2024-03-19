#!/usr/bin/env python3
"""entry"""

from flask import Flask, render_template,request, jsonify, session, g, redirect
from database.database import Database
import secrets, hashlib, bcrypt, sqlite3


app = Flask(__name__)
app.config['DATABASE'] = 'database/indoor_booking.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

db = Database(app.config['DATABASE'])
"""Create tables in the database"""
db.create_tables()

@app.route('/')
def index():
    """root of the project"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Render the dashboard page"""
    user_name = session.get('user_name')
    if user_name:
        return render_template('dashboard.html', user_name=user_name)
    else:
        return redirect('/login')


@app.route('/login')
def login_page():
    """Render the login page"""
    return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    """Handle POST request to authenticate user login"""
    cell_number = request.form.get('cell_number')
    password = request.form.get('password')

    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT user_id, name, hashed_password, salt FROM User WHERE cell_number = ?
    ''', (cell_number,))
    user_data = cursor.fetchone()

    if user_data:
        user_id, user_name, hashed_password, salt = user_data
        """Hash the password provided by the user with the retrieved salt"""
        hashed_input_password = hashlib.sha256((password + salt).encode()).hexdigest()
        if hashed_input_password == hashed_password:
            """Save the user's name and ID in the session"""
            session['user_name'] = user_name
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))

    return jsonify({"message": "Login failed"}), 401


@app.route('/register', methods=['GET'])
def show_registration_form():
    return render_template('register.html')


@app.route('/register_user', methods=['POST'])
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
            INSERT INTO User (name, surname, cell_number, hashed_password)
            VALUES (?, ?, ?, ?)
        ''', (name, surname, cell_number, hashed_password.decode('utf-8')))
        db.conn.commit()

        """ Fetch the user's name from the database """
        db.cursor.execute('''
            SELECT name FROM User WHERE cell_number = ?
        ''', (cell_number,))
        user_name = db.cursor.fetchone()[0]

        """ Store user name in the session """
        session['user_name'] = user_name

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
