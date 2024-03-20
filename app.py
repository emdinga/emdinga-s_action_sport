#!/usr/bin/env python3
"""entry"""

from flask import Flask, render_template,request, jsonify, session, g, redirect
from database.database import Database
import secrets, hashlib, bcrypt, sqlite3
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///indoor_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    """define table user"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    cell_number = db.Column(db.String(20), unique=True)
    hashed_password = db.Column(db.String(64))
    salt = db.Column(db.String(16))

@app.route('/register_user', methods=['POST'])
def register_user():
    """register new user"""
    name = request.form.get('name')
    surname = request.form.get('surname')
    cell_number = request.form.get('cell_number')
    password = request.form.get('password')

    """Generate salt and hash password"""
    salt = secrets.token_hex(8)
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    """Create new user record"""
    new_user = User(name=name, surname=surname, cell_number=cell_number,
                    hashed_password=hashed_password, salt=salt)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/login_user', methods=['POST'])
def login_user():
    """ login route"""
    data = request.json
    cell_number = data.get('cell_number')
    password = data.get('password')

    """Query user from database"""
    user = User.query.filter_by(cell_number=cell_number).first()

    if user:
        """Hash input password with retrieved salt"""
        hashed_input_password = hashlib.sha256((password + user.salt).encode()).hexdigest()
        if hashed_input_password == user.hashed_password:
            return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Login failed'}), 401

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

@app.route('/register', methods=['GET'])
def show_registration_form():
    return render_template('register.html')

@app.route('/registration-successful')
def registration_success():
    return render_template('registration_succ.html')


if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0', port=5000, debug=True)
