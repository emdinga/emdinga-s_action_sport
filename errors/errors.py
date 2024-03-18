#!/usr/bin/env python3
"""errors"""


def create_error_response(message, status_code):
    """
    Helper function to create error response in JSON format.
    """
    return {"error": message}, status_code
