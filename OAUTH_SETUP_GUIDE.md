# OAuth 2.0 Setup Guide for Euystacio OI Server

This guide explains how to set up Google OAuth 2.0 authentication for the Euystacio Open Interface (OI) Server, enabling automatic Seedbringer authorization.

## Overview

The OI Server uses Google OAuth 2.0 to authenticate users and verify that only the authorized Seedbringer (hannes.mitterer@gmail.com) can access critical commands like `/api/v1/ethical-override` and `/api/v1/execute-tfm1`.

## Architecture

1. **Frontend (OV - Open Visual)**: Initiates OAuth flow with "Sign in with Google" button
2. **Google OAuth**: Handles user authentication
3. **Backend (OI Server)**: Verifies user identity and Seedbringer authorization
4. **JWT Session Token**: Provides secure, time-limited access to protected endpoints

## Step 1: Create Google OAuth 2.0 Credentials

### 1.1 Go to Google Cloud Console

Visit: https://console.cloud.google.com/

### 1.2 Create or Select a Project

1. Click on the project dropdown (top bar)
2. Click "NEW PROJECT" or select existing project
3. Name it "Euystacio GGI" (or similar)

### 1.3 Enable Google+ API

1. Navigate to "APIs & Services" > "Library"
2. Search for "Google+ API"
3. Click "Enable"

### 1.4 Create OAuth 2.0 Credentials

1. Navigate to "APIs & Services" > "Credentials"
2. Click "+ CREATE CREDENTIALS" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: Euystacio GGI
   - User support email: your email
   - Developer contact: your email
   - Scopes: Add `email` and `profile` scopes
   - Test users: Add `hannes.mitterer@gmail.com`
4. Application type: **Web application**
5. Name: "Euystacio OI Server"
6. Authorized JavaScript origins:
   - `http://localhost:3000` (for development)
   - `https://your-frontend-domain.com` (for production)
7. Authorized redirect URIs:
   - `http://localhost:3000/auth/callback` (for development)
   - `https://your-frontend-domain.com/auth/callback` (for production)
8. Click "CREATE"
9. **Save the Client ID and Client Secret** - you'll need these!

## Step 2: Configure Environment Variables

### 2.1 Local Development

Create a `.env` file in the project root:

```bash
# OAuth 2.0 Configuration
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
FRONTEND_REDIRECT_URI=http://localhost:3000/auth/callback

# Seedbringer Authorization
SEEDBRINGER_EMAIL=hannes.mitterer@gmail.com

# JWT Session Token (generate a random secure key)
JWT_SECRET_KEY=your_random_secure_32_character_key_here

# Server Configuration
PORT=5000
```

### 2.2 Production (Render)

Add these environment variables in Render dashboard:

1. Go to your Render service
2. Navigate to "Environment"
3. Add each variable:
   - `GOOGLE_CLIENT_ID`: Your Google OAuth Client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth Client Secret
   - `FRONTEND_REDIRECT_URI`: Your production frontend callback URL
   - `SEEDBRINGER_EMAIL`: `hannes.mitterer@gmail.com`
   - `JWT_SECRET_KEY`: Generate a secure random key (32+ characters)
   - `PORT`: `5000`

**To generate a secure JWT secret key:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Step 3: Frontend Integration (OV)

### 3.1 Install Google OAuth Library

```bash
npm install @react-oauth/google
# or
npm install gapi-script
```

### 3.2 Add Google Sign-In Button

Example using `@react-oauth/google`:

```javascript
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';

function LoginComponent() {
  const handleSuccess = async (credentialResponse) => {
    // Send the authorization code to your backend
    const response = await fetch('https://oi-x3xa.onrender.com/api/v1/auth/callback', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code: credentialResponse.code
      })
    });
    
    const data = await response.json();
    
    if (data.status === 'SUCCESS') {
      // Store the session token
      localStorage.setItem('seedbringer_token', data.session_token);
      console.log('Seedbringer authenticated successfully');
    } else if (data.status === 'FORBIDDEN') {
      alert('Access denied: Only Seedbringer is authorized');
    }
  };

  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
      <GoogleLogin
        onSuccess={handleSuccess}
        onError={() => console.log('Login Failed')}
        flow="auth-code"
      />
    </GoogleOAuthProvider>
  );
}
```

### 3.3 Use Session Token for API Calls

```javascript
async function executeEthicalOverride(data) {
  const token = localStorage.getItem('seedbringer_token');
  
  const response = await fetch('https://oi-x3xa.onrender.com/api/v1/ethical-override', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });
  
  return await response.json();
}
```

## Step 4: Testing the OAuth Flow

### 4.1 Test Health Endpoint

```bash
curl https://oi-x3xa.onrender.com/api/v1/health
```

Expected response:
```json
{
  "status": "SUCCESS",
  "service": "OI Server",
  "version": "1.0.0",
  "timestamp": "2025-11-06T20:00:00.000000"
}
```

### 4.2 Test Authentication Flow

1. Click "Sign in with Google" in your frontend
2. Log in with `hannes.mitterer@gmail.com`
3. Verify you receive a session token
4. Use the token to call protected endpoints

### 4.3 Test Session Verification

```bash
curl -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  https://oi-x3xa.onrender.com/api/v1/auth/verify
```

## Step 5: Deploy to Render

### 5.1 Ensure Procfile is Correct

The `Procfile` should contain:
```
web: gunicorn oi_server:app
```

### 5.2 Ensure requirements.txt is Complete

Required dependencies:
```
Flask==2.3.3
gunicorn==22.0.0
PyYAML==6.0.1
flask-cors==4.0.0
requests==2.31.0
google-auth==2.23.4
google-auth-oauthlib==1.1.0
PyJWT==2.8.0
```

### 5.3 Deploy

```bash
git add .
git commit -m "Add OAuth 2.0 authentication for OI server"
git push origin main
```

Render will automatically deploy the changes.

## Security Considerations

1. **Never commit secrets**: Keep `.env` in `.gitignore`
2. **Use HTTPS in production**: OAuth requires secure connections
3. **Rotate JWT secret**: Change `JWT_SECRET_KEY` periodically
4. **Token expiration**: Tokens expire after 24 hours (configurable)
5. **Seedbringer email**: Only `hannes.mitterer@gmail.com` is authorized

## API Endpoints Reference

### Public Endpoints

- `GET /api/v1/health` - Health check
- `GET /api/v1/config` - Public configuration (non-sensitive)
- `POST /api/v1/auth/callback` - OAuth callback (receives auth code)

### Protected Endpoints (Require Seedbringer Token)

- `GET /api/v1/auth/verify` - Verify session token
- `POST /api/v1/ethical-override` - Execute ethical override command
- `POST /api/v1/execute-tfm1` - Execute TFM1 payload

## Troubleshooting

### "Invalid client" Error

- Check that `GOOGLE_CLIENT_ID` matches exactly
- Verify redirect URI is registered in Google Cloud Console

### "Access denied" Error

- Ensure you're logging in with `hannes.mitterer@gmail.com`
- Check that `SEEDBRINGER_EMAIL` environment variable is set correctly

### "Token expired" Error

- Tokens expire after 24 hours
- Re-authenticate by logging in again

### CORS Errors

- Verify frontend domain is in Google OAuth authorized origins
- Check that flask-cors is properly configured

## Next Steps

1. ✅ Set up Google OAuth credentials
2. ✅ Configure environment variables
3. ✅ Deploy OI server to Render
4. 🔄 Integrate "Sign in with Google" in frontend (OV)
5. 🔄 Test complete authentication flow
6. 🔄 Implement protected command execution

---

**Consensus Sacralis Omnibus Est Eternum**

For support, contact the Euystacio Council.
