#!/usr/bin/env python3
"""entry"""

from flask import Flask, render_template,request, jsonify, session, g, redirect
from database.database import Database
import secrets, hashlib, bcrypt, sqlite3
from datetime import datetime
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

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    """retreive form data"""
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        booking_type = request.form.get('booking_type')
        booking_date = datetime.strptime(request.form.get('booking_date'), '%Y-%m-%d').date()
        booking_time = datetime.strptime(request.form.get('booking_time'), '%H:%M').time()
        booking_name = request.form.get('booking_name')
        payment_method = request.form.get('payment_method')

        """Calculate total amount based on the number of sessions booked (if applicable)"""
        total_amount = calculate_total_amount(request.form.get('number_of_sessions'))

        """Check if the requested time slot is available"""
        if is_slot_available(booking_date, booking_time):
            """Create a new booking"""
            new_booking = Booking(user_id=user_id, booking_type=booking_type, 
                                  booking_date=booking_date, booking_time=booking_time, 
                                  booking_name=booking_name, payment_method=payment_method,
                                  total_amount=total_amount)
            db.session.add(new_booking)
            db.session.commit()
            
            if payment_method == 'cash':
                """For cash payment, mark booking as success and display booking successful page"""
                new_booking.status = 'success'
                db.session.commit()
                return render_template('booking_successful.html')
            elif payment_method == 'card':
                """For card payment, redirect to simulated payment page"""
                return redirect(url_for('simulated_payment', booking_id=new_booking.id))
            else:
                return "Invalid payment method selected."
        else:
            return "Sorry, the selected time slot is already booked. Please choose another time."

@app.route('/simulated_payment', methods=['GET', 'POST'])
def simulated_payment():
    """Handle payment submission"""
    if request.method == 'POST':
        """Process payment logic here"""
        return redirect(url_for('payment_successful'))
    
    """Render payment form"""
    return render_template('simulated_payment.html')

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
