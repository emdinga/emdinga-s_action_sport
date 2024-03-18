#!/usr/bin/env python3
""" middllewear"""

from flask import request, jsonify


def authenticate_user(request):
    """
    Middleware function to authenticate user.
    """
    auth_token = request.headers.get('Authorization')

    if not auth_token:
        return jsonify({"error": "Authorization token is missing"}), 401

    return None

def log_request(request):
    """
    Middleware function to log requests.
    """
    print(f"Request received: {request.method} {request.path}")
