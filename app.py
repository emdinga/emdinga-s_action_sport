#!/usr/bin/env python3
"""entry"""

from flask import Flask, render_template,request, jsonify, session, g, redirect, url_for
from database.database import Database
import secrets, hashlib, bcrypt, sqlite3
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///indoor_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class User(db.Model):
    """define table user"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    cell_number = db.Column(db.String(20), unique=True)
    hashed_password = db.Column(db.String(64))
    salt = db.Column(db.String(16))
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Booking(db.Model):
    """Define the Booking table"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_type = db.Column(db.String(50))
    booking_date = db.Column(db.Date)
    booking_time = db.Column(db.Time)
    booking_name = db.Column(db.String(100))
    payment_method = db.Column(db.String(50))
    total_amount = db.Column(db.Float)


def get_booked_slots_from_database(selected_date):
    """Query your database to retrieve the booked time slots for the selected date"""

    """Query bookings for the selected date"""
    bookings = Booking.query.filter_by(booking_date=selected_date).all()

    """Extract booked time slots from the bookings"""
    booked_slots = [booking.booking_time.strftime('%H:%M') for booking in bookings]

    return booked_slots

@app.route('/get_available_time_slots', methods=['POST'])
def get_available_time_slots():
    """Retrieve booked time slots for the selected date from the database"""
    selected_date = request.form['selected_date']
    booked_slots = get_booked_slots_from_database(selected_date)
    """Generate all possible time slots from 09:00 AM to 10:00 PM"""
    all_time_slots = generate_time_slots()
    """Filter out the booked time slots from the list of all possible time slots"""
    available_slots = [slot for slot in all_time_slots if slot not in booked_slots]
    return jsonify({'available_slots': available_slots})

def generate_time_slots():
    """generate all possible time slots from 09:00 AM to 10:00 PM"""
    start_time = datetime.strptime('09:00', '%H:%M')
    end_time = datetime.strptime('22:00', '%H:%M')
    time_slots = []
    current_time = start_time
    while current_time <= end_time:
        time_slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(hours=1)
    return time_slots

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    """Retrieve form data and store it in session"""
    if request.method == 'POST':
        session['booking_details'] = {
            'user_id': request.form.get('user_id'),
            'booking_type': request.form.get('booking_type'),
            'booking_date': request.form.get('booking_date'),
            'booking_time': request.form.get('booking_time'),
            'booking_name': request.form.get('booking_name'),
            'payment_method': request.form.get('payment_method'),
            'total_amount': 500
        }

        booking_details = session.get('booking_details')

        return render_template('payment.html', booking_details=booking_details)

@app.route('/save_payment', methods=['POST'])
def save_payment():
    """Process payment based on the selected method"""
    if 'booking_details' not in session:
        return redirect(url_for('index'))

    booking_details = session.pop('booking_details')
    payment_method = request.form.get('payment_method')

    if payment_method == 'cash':
        """Save booking details to the database"""
        save_booking_to_database(booking_details)
        return render_template('booking_successful.html')
    elif payment_method == 'card':
        """Process card payment"""
        card_number = request.form.get('card-number')
        expiration_date = request.form.get('expiration-date')
        cvv = request.form.get('cvv')

        """Perform payment processing here"""
        if payment_successful(card_number, expiration_date, cvv):
            """Save booking details to the database"""
            save_booking_to_database(booking_details)
            return render_template('booking_successful.html')
        else:
            return "Payment failed. Please try again."
    else:
        return "Invalid payment method selected."


def save_booking_to_database(booking_details):
    """Save booking details to the database"""
    new_booking = Booking(
        user_id=booking_details['user_id'],
        booking_type=booking_details['booking_type'],
        booking_date=datetime.strptime(booking_details['booking_date'], '%Y-%m-%d').date(),
        booking_time=datetime.strptime(booking_details['booking_time'], '%H:%M').time(),
        booking_name=booking_details['booking_name'],
        payment_method=booking_details['payment_method'],
        total_amount=booking_details['total_amount']
    )
    db.session.add(new_booking)
    db.session.commit()



@app.route('/payment_successful')
def payment_successful():
    """render confirmation"""
    return render_template('payment_successful.html')

@app.route('/book_online')
def book_online():
    """ book online page """
    return render_template('booking_form.html')


@app.route('/register_user', methods=['POST'])
def register_user():
    """Register a new user"""
    name = request.form.get('name')
    surname = request.form.get('surname')
    cell_number = request.form.get('cell_number')
    password = request.form.get('password')

    """Check if a user with the same cell number already exists"""
    existing_user = User.query.filter_by(cell_number=cell_number).first()
    if existing_user:
        return jsonify({'message': 'User with the same cell phone number already exists'}), 409

    """Generate salt and hash password"""
    salt = secrets.token_hex(8)
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    """Create a new user record"""
    new_user = User(name=name, surname=surname, cell_number=cell_number,
                    hashed_password=hashed_password, salt=salt)
    db.session.add(new_user)
    db.session.commit()

    """Set user_name in session after registration"""
    session['user_name'] = name

    return jsonify({'message': 'User registered successfully'}), 200


@app.route('/login_user', methods=['POST'])
def login_user():
    """ Login route """
    cell_number = request.form.get('cell_number')
    password = request.form.get('password')

    """ Query user from database """
    user = User.query.filter_by(cell_number=cell_number).first()

    if user:
        """ Hash input password with retrieved salt """
        hashed_input_password = hashlib.sha256((password + user.salt).encode()).hexdigest()
        if hashed_input_password == user.hashed_password:
            """Set the user's name in the session"""
            session['user_name'] = user.name
            """Redirect to the dashboard"""
            return redirect('/dashboard')

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
        return render_template('dashbaord.html', user_name=user_name)
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
        db.create_all()
        app.run(host='0.0.0.0', port=5000, debug=True)
