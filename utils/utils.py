#!/usr/bin/env python3
"""utils"""

import hashlib


def generate_hash(text):
    """
    Generate SHA-256 hash for the given text.
    """
    return hashlib.sha256(text.encode()).hexdigest()

def format_phone_number(phone_number):
    """
    Format phone number in a standardized way.
    format to +XX XXX XXX XXX
    """
    return f"+{phone_number[:2]} {phone_number[2:5]} {phone_number[5:8]} {phone_number[8:]}"
