#!/usr/bin/env python3
"""entry"""

from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    """root of the project"""
    return render_template('frontend/static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
