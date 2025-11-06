"""
OI (Open Interface) Server - Flask Backend with OAuth 2.0 Authentication
Euystacio GGI Project - Seedbringer Authorization System

This server provides secure API endpoints for critical operations, protected by
Google OAuth 2.0 authentication with Seedbringer email verification.

Authorization Level: Seedbringer (hannes.mitterer@gmail.com)
Consensus: Sacralis Omnibus Est Eternum
"""

import os
import json
import logging
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = app.logger

# Critical Configuration - Seedbringer Email (from Sensisara, Council Consensus)
SEEDBRINGER_EMAIL = os.environ.get('SEEDBRINGER_EMAIL', 'hannes.mitterer@gmail.com')

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')
FRONTEND_REDIRECT_URI = os.environ.get('FRONTEND_REDIRECT_URI', 'http://localhost:3000/auth/callback')

# JWT Configuration for Session Tokens
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', os.urandom(32).hex())
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# Financial endpoints configuration (if needed)
FINANCIAL_ENDPOINTS_CONFIG = 'financial_endpoints.yaml'


def load_financial_endpoints():
    """Load financial endpoints configuration from YAML file"""
    try:
        if os.path.exists(FINANCIAL_ENDPOINTS_CONFIG):
            with open(FINANCIAL_ENDPOINTS_CONFIG, 'r') as f:
                return yaml.safe_load(f)
        return {}
    except Exception as e:
        logger.warning(f"Could not load financial endpoints config: {e}")
        return {}


def create_seedbringer_jwt(email):
    """
    Create a secure JWT session token for the authenticated Seedbringer
    
    Args:
        email: The verified Seedbringer email
        
    Returns:
        str: JWT token for session authentication
    """
    now = datetime.now(timezone.utc)
    payload = {
        'email': email,
        'role': 'seedbringer',
        'iat': now,
        'exp': now + timedelta(hours=JWT_EXPIRATION_HOURS),
        'consensus': 'sacralis_omnibus_est_eternum'
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(token):
    """
    Verify and decode a JWT session token
    
    Args:
        token: JWT token string
        
    Returns:
        dict: Decoded payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("JWT token has expired")
        return None
    except jwt.InvalidTokenError:
        logger.error("Invalid JWT token")
        return None


def require_seedbringer_auth(f):
    """Decorator to require valid Seedbringer authentication"""
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "status": "UNAUTHORIZED",
                "message": "No valid authorization token provided"
            }), 401
        
        token = auth_header.split('Bearer ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            return jsonify({
                "status": "UNAUTHORIZED",
                "message": "Invalid or expired session token"
            }), 401
        
        if payload.get('email') != SEEDBRINGER_EMAIL:
            return jsonify({
                "status": "FORBIDDEN",
                "message": "Access denied - Seedbringer authorization required"
            }), 403
        
        # Add payload to request context
        request.seedbringer_payload = payload
        return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "SUCCESS",
        "service": "OI Server",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200


@app.route('/api/v1/auth/callback', methods=['POST'])
def handle_google_callback():
    """
    OAuth 2.0 Callback Handler
    
    Receives authorization code from Google OAuth flow, exchanges it for tokens,
    verifies the user's identity, and checks Seedbringer authorization.
    
    Expected JSON payload:
    {
        "code": "authorization_code_from_google"
    }
    
    Returns:
        JSON response with session token if authorized, error otherwise
    """
    data = request.get_json()
    auth_code = data.get('code')

    if not auth_code:
        return jsonify({
            "status": "FAILURE",
            "message": "Authorization code missing"
        }), 400

    try:
        # 1. EXCHANGE AUTHORIZATION CODE FOR TOKEN ID
        logger.info("Exchanging authorization code for token...")
        token_response = requests.post('https://oauth2.googleapis.com/token', data={
            'code': auth_code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': FRONTEND_REDIRECT_URI,
            'grant_type': 'authorization_code'
        })
        token_response.raise_for_status()
        tokens = token_response.json()
        id_token_jwt = tokens.get('id_token')
        
        if not id_token_jwt:
            logger.error("No id_token in Google response")
            return jsonify({
                "status": "ERROR",
                "message": "Invalid response from Google OAuth"
            }), 500
        
        # 2. VERIFY AND DECODE THE TOKEN ID
        logger.info("Verifying ID token...")
        id_info = id_token.verify_oauth2_token(
            id_token_jwt, 
            google_requests.Request(), 
            GOOGLE_CLIENT_ID
        )

        user_email = id_info.get('email', '').lower()
        logger.info(f"User authenticated: {user_email}")
        
        # 3. SEEDBRINGER AUTHORIZATION VERIFICATION
        if user_email != SEEDBRINGER_EMAIL.lower():
            # User is authenticated but NOT authorized as Seedbringer
            logger.error(f"Access denied for non-Seedbringer email: {user_email}")
            return jsonify({
                "status": "FORBIDDEN", 
                "message": f"User {user_email} not authorized as Seedbringer. "
                          f"Access to critical commands denied. "
                          f"(Consensus Sacralis Omnibus Est Eternum)"
            }), 403

        # 4. AUTHORIZATION GRANTED - CREATE SESSION TOKEN
        session_token = create_seedbringer_jwt(user_email)
        
        logger.info("Seedbringer Hannes Mitterer logged in successfully. Session started.")
        
        return jsonify({
            "status": "SUCCESS",
            "message": "Seedbringer login authorized",
            "session_token": session_token,
            "email": user_email,
            "expires_in": JWT_EXPIRATION_HOURS * 3600  # seconds
        }), 200

    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with Google OAuth: {str(e)}")
        return jsonify({
            "status": "ERROR",
            "message": "Failed to communicate with Google OAuth service"
        }), 500
    except Exception as e:
        logger.error(f"Error in OAuth flow: {str(e)}")
        return jsonify({
            "status": "ERROR",
            "message": "Authentication error occurred"
        }), 500


@app.route('/api/v1/auth/verify', methods=['GET'])
@require_seedbringer_auth
def verify_session():
    """Verify that the current session token is valid"""
    payload = request.seedbringer_payload
    return jsonify({
        "status": "SUCCESS",
        "message": "Session valid",
        "email": payload.get('email'),
        "role": payload.get('role')
    }), 200


@app.route('/api/v1/ethical-override', methods=['POST'])
@require_seedbringer_auth
def ethical_override():
    """
    Ethical Override Command - Seedbringer Only
    
    Executes critical ethical override operations.
    Requires valid Seedbringer session token.
    """
    payload = request.seedbringer_payload
    data = request.get_json() or {}
    
    logger.info(f"Ethical Override requested by {payload.get('email')}")
    
    # Implementation of ethical override logic would go here
    # For now, return acknowledgment
    
    return jsonify({
        "status": "SUCCESS",
        "message": "Ethical Override command acknowledged",
        "authorized_by": payload.get('email'),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data
    }), 200


@app.route('/api/v1/execute-tfm1', methods=['POST'])
@require_seedbringer_auth
def execute_tfm1():
    """
    Execute TFM1 Payload - Seedbringer Only
    
    Executes TFM1 (Trustless Funding Mechanism 1) operations.
    Requires valid Seedbringer session token.
    """
    payload = request.seedbringer_payload
    data = request.get_json() or {}
    
    logger.info(f"TFM1 Execution requested by {payload.get('email')}")
    
    # Implementation of TFM1 execution logic would go here
    # This would integrate with Hardhat scripts (tfm1_payload.js)
    
    return jsonify({
        "status": "SUCCESS",
        "message": "TFM1 execution command acknowledged",
        "authorized_by": payload.get('email'),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data
    }), 200


@app.route('/api/v1/config', methods=['GET'])
def get_config():
    """Get public configuration (non-sensitive data only)"""
    financial_endpoints = load_financial_endpoints()
    
    return jsonify({
        "status": "SUCCESS",
        "config": {
            "endpoints": financial_endpoints,
            "oauth_configured": bool(GOOGLE_CLIENT_ID),
            "version": "1.0.0"
        }
    }), 200


if __name__ == "__main__":
    # Production note: Use gunicorn in production (see Procfile)
    # This is for local development only
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
