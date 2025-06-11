from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models.user import User
from utils.email_service import EmailService
import os

# Initialize email service
email_service = EmailService()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])
            current_user = User.objects(id=data['user_id']).first()
            if not current_user:
                return jsonify({'message': 'Invalid token!'}), 401
        except:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def register():
    data = request.get_json()
    
    # Check if user already exists
    if User.objects(email=data['email']).first():
        return jsonify({'message': 'Email already registered!'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        role='user'
    )
    user.save()
    
    # Send welcome email
    email_service.send_welcome_email(user)
    
    return jsonify({'message': 'User registered successfully!'}), 201

def login():
    data = request.get_json()
    
    # Find user by email
    user = User.objects(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password!'}), 401
    
    # Generate token
    token = jwt.encode({
        'user_id': str(user.id),
        'exp': datetime.utcnow() + timedelta(days=1)
    }, os.getenv('JWT_SECRET_KEY'))
    
    return jsonify({
        'token': token,
        'user': {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    })

def get_profile(current_user):
    return jsonify({
        'id': str(current_user.id),
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role
    })

def request_password_reset():
    data = request.get_json()
    user = User.objects(email=data['email']).first()
    
    if not user:
        return jsonify({'message': 'If an account exists with this email, you will receive a password reset link.'}), 200
    
    # Generate reset token
    reset_token = jwt.encode({
        'user_id': str(user.id),
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, os.getenv('JWT_SECRET_KEY'))
    
    # Send password reset email
    email_service.send_password_reset_email(user, reset_token)
    
    return jsonify({'message': 'If an account exists with this email, you will receive a password reset link.'}), 200

def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    if not token or not new_password:
        return jsonify({'message': 'Token and new password are required!'}), 400
    
    try:
        # Verify token
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])
        user = User.objects(id=payload['user_id']).first()
        
        if not user:
            return jsonify({'message': 'Invalid token!'}), 401
        
        # Update password
        user.password = generate_password_hash(new_password)
        user.save()
        
        return jsonify({'message': 'Password has been reset successfully!'}), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Password reset link has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401 