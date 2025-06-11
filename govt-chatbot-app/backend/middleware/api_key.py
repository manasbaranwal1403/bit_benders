from functools import wraps
from flask import request, jsonify
import os
from datetime import datetime, timedelta
from models.user import User

VALID_API_KEY = 'ShUjoYzro150LhcEVxaNif2uDLdxjhdLeD-tdeG2HQA2'

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'message': 'API key is missing!'}), 401
            
        # Check if API key is valid
        if api_key != VALID_API_KEY:
            return jsonify({'message': 'Invalid API key!'}), 401
            
        return f(*args, **kwargs)
    return decorated

def generate_api_key():
    """Generate a secure API key"""
    import secrets
    return secrets.token_urlsafe(32)

def set_api_key_expiry():
    """Set API key expiry to 30 days from now"""
    return datetime.utcnow() + timedelta(days=30) 