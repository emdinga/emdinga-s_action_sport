#!/usr/bin/env python3
"""api"""

from flask import Flask, request, jsonify
from database.database import Database


app = Flask(__name__)
db = Database('indoor_booking.db')


@app.route('/api/booking', methods=['POST'])
def create_booking():
    """Route to create a new booking"""
    data = request.json
    """Extract data from request"""
    user_id = data.get('user_id')
    facility_id = data.get('facility_id')
    booking_type = data.get('booking_type')
    duration = data.get('duration')
    payment_method = data.get('payment_method')
    payment_status = data.get('payment_status')
    """Insert booking data into database"""
    db.cursor.execute('''
        INSERT INTO Booking (user_id, facility_id, booking_type, duration, payment_method, payment_status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, facility_id, booking_type, duration, payment_method, payment_status))
    db.conn.commit()
    return jsonify({"message": "Booking created successfully"}), 201


@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    """Route to retrieve all bookings"""
    db.cursor.execute('''
        SELECT * FROM Booking
    ''')
    bookings = db.cursor.fetchall()
    if not bookings:
        return jsonify({"message": "No bookings found"}), 404
    bookings_list = []
    for booking in bookings:
        booking_dict = {
            "booking_id": booking[0],
            "user_id": booking[1],
            "facility_id": booking[2],
            "booking_type": booking[3],
            "duration": booking[4],
            "payment_method": booking[5],
            "payment_status": booking[6]
        }
        bookings_list.append(booking_dict)
    return jsonify({"bookings": bookings_list}), 200

if __name__ == '__main__':
    app.run(debug=True)
