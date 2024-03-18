#!/usr/bin/env python3
"""payments"""

from flask import Flask, request, jsonify
from database.database import Database

app = Flask(__name__)
db = Database('indoor_booking.db')


@app.route('/api/process_payment', methods=['POST'])
def process_payment():
    """Simulated payment processing logic"""
    data = request.json
    amount = data.get('amount')
    payment_method = data.get('payment_method')
    
    """Insert payment transaction into database (for logging purposes)"""
    db.cursor.execute('''
        INSERT INTO PaymentTransaction (amount, payment_method, transaction_status)
        VALUES (?, ?, ?)
    ''', (amount, payment_method, 'success'))
    
    db.conn.commit()
    
    return jsonify({"message": "Payment processed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
