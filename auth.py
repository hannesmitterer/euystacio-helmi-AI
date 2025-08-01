"""
Authentication and user management for Euystacio Dashboard
"""
import json
import os
import hashlib
import secrets
from datetime import datetime
from functools import wraps
from flask import session, request, jsonify, redirect, url_for

class UserManager:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.admin_users = {'seedbringer', 'alfred', 'dietmar', 'cofounders'}
        self.ensure_users_file()
    
    def ensure_users_file(self):
        """Create users file if it doesn't exist"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def load_users(self):
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def hash_password(self, password):
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{hashed.hex()}"
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        try:
            salt, hash_hex = hashed_password.split(':')
            hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return hash_hex == hashed.hex()
        except:
            return False
    
    def register_user(self, email, password, username=None):
        """Register a new user"""
        users = self.load_users()
        
        if email in users:
            return {'success': False, 'message': 'Email already registered'}
        
        # Use email as username if not provided
        if not username:
            username = email.split('@')[0]
        
        # Check if username is admin
        is_admin = username.lower() in self.admin_users
        
        user_data = {
            'email': email,
            'username': username,
            'password': self.hash_password(password),
            'is_admin': is_admin,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        users[email] = user_data
        self.save_users(users)
        
        return {'success': True, 'message': 'User registered successfully', 'is_admin': is_admin}
    
    def authenticate_user(self, email, password):
        """Authenticate user"""
        users = self.load_users()
        
        if email not in users:
            return {'success': False, 'message': 'Invalid email or password'}
        
        user = users[email]
        if not self.verify_password(password, user['password']):
            return {'success': False, 'message': 'Invalid email or password'}
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        users[email] = user
        self.save_users(users)
        
        return {
            'success': True, 
            'user': {
                'email': user['email'],
                'username': user['username'],
                'is_admin': user['is_admin']
            }
        }
    
    def get_user(self, email):
        """Get user by email"""
        users = self.load_users()
        return users.get(email)

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('index'))
        
        user_manager = UserManager()
        user = user_manager.get_user(session['user_email'])
        if not user or not user.get('is_admin', False):
            if request.is_json:
                return jsonify({'error': 'Admin privileges required'}), 403
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current logged in user"""
    if 'user_email' not in session:
        return None
    
    user_manager = UserManager()
    return user_manager.get_user(session['user_email'])