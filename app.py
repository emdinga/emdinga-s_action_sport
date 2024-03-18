#!/usr/bin/env python3
"""entry"""

from flask import Flask, render_template,request, jsonify
from database.database import Database

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


if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0', port=5000, debug=True)
