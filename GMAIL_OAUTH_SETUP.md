# Gmail OAuth 2.0 Setup Guide

Complete guide for setting up Gmail API integration with OAuth 2.0 authentication for the Nexus platform.

## Overview

This guide covers:
- Creating a Google Cloud project
- Enabling Gmail API
- Configuring OAuth 2.0 consent screen
- Creating OAuth 2.0 credentials
- Required scopes
- Environment variable configuration
- Testing the integration

---

## Prerequisites

- Google account (Gmail or Google Workspace)
- Access to [Google Cloud Console](https://console.cloud.google.com)
- Admin privileges if using Google Workspace

---

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click on the project dropdown (top navigation bar)
3. Click **"New Project"**
4. Enter project details:
   - **Project name**: `Nexus Gmail Integration`
   - **Organization**: Select your organization (if applicable)
5. Click **"Create"**
6. Wait for project creation to complete
7. Select the newly created project from the dropdown

---

## Step 2: Enable Gmail API

1. In Google Cloud Console, navigate to **"APIs & Services"** → **"Library"**
2. Search for **"Gmail API"**
3. Click on **"Gmail API"**
4. Click **"Enable"**
5. Wait for API to be enabled

---

## Step 3: Configure OAuth Consent Screen

### Choose User Type

1. Navigate to **"APIs & Services"** → **"OAuth consent screen"**
2. Select user type:
   - **Internal**: For Google Workspace users only (recommended for internal apps)
   - **External**: For any Google account users
3. Click **"Create"**

### App Information

Fill in the following fields:

**Required fields:**
- **App name**: `Nexus Platform`
- **User support email**: Your email address
- **App logo** (optional): Upload a logo image (120x120px)
- **Application home page**: `https://your-nexus-domain.com`
- **Application privacy policy link**: `https://your-nexus-domain.com/privacy`
- **Application terms of service link**: `https://your-nexus-domain.com/terms`

**Developer contact information:**
- **Email addresses**: Your email address(es)

Click **"Save and Continue"**

### Scopes

1. Click **"Add or Remove Scopes"**
2. Add the following scopes:

**Basic scopes:**
```
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
openid
```

**Gmail scopes (choose based on your needs):**

#### Read-only access:
```
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.metadata
https://www.googleapis.com/auth/gmail.labels
```

#### Send emails:
```
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.compose
```

#### Modify emails:
```
https://www.googleapis.com/auth/gmail.modify
```

#### Full access (use with caution):
```
https://mail.google.com/
```

**Recommended scope combination for Nexus:**
```
openid
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.labels
```

3. Click **"Update"**
4. Click **"Save and Continue"**

### Test Users (External Apps Only)

If you selected "External" user type and haven't published:

1. Click **"Add Users"**
2. Add email addresses of test users
3. Click **"Add"**
4. Click **"Save and Continue"**

### Summary

Review your configuration and click **"Back to Dashboard"**

---

## Step 4: Create OAuth 2.0 Credentials

1. Navigate to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Select **"Application type"**:
   - **Web application** (most common for Nexus)
   - **Desktop app** (if using desktop client)
   - **Other** (for server-to-server)

### Web Application Configuration

**Name**: `Nexus Web Client`

**Authorized JavaScript origins** (optional):
```
https://your-nexus-domain.com
http://localhost:3000  (for development)
```

**Authorized redirect URIs**:
```
https://your-nexus-domain.com/oauth/callback
https://your-nexus-domain.com/auth/google/callback
http://localhost:3000/oauth/callback  (for development)
```

4. Click **"Create"**
5. **Important**: Copy and save:
   - **Client ID**: `123456789-abcdefghijklmnop.apps.googleusercontent.com`
   - **Client Secret**: `GOCSPX-abcdefghijklmnopqrstuvwxyz`

---

## Step 5: Download Credentials JSON

1. On the **"Credentials"** page, find your OAuth 2.0 Client ID
2. Click the **download icon** (⬇) on the right
3. Save as `credentials.json` or `google-oauth-credentials.json`
4. **Keep this file secure** - do not commit to version control

---

## Step 6: Environment Variable Configuration

### Method 1: Using Credentials JSON

Store the entire credentials JSON in an environment variable:

```bash
# .env file
GOOGLE_OAUTH_CREDENTIALS='{"web":{"client_id":"123456789-abcd.apps.googleusercontent.com","project_id":"nexus-gmail","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"GOCSPX-abcdefghijklmnop","redirect_uris":["https://your-domain.com/oauth/callback"]}}'
```

### Method 2: Individual Variables (Recommended)

```bash
# .env file

# Google OAuth 2.0 Configuration
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
GOOGLE_REDIRECT_URI=https://your-nexus-domain.com/oauth/callback

# OAuth Scopes (space-separated)
GOOGLE_OAUTH_SCOPES=openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.readonly

# Gmail API Configuration
GMAIL_API_ENABLED=true
GMAIL_QUOTA_USER=nexus-platform
GMAIL_USER_AGENT=Nexus/1.0

# Token Storage
OAUTH_TOKEN_ENCRYPTION=true
OAUTH_TOKEN_DB_TABLE=oauth_tokens
```

### Method 3: Service Account (Server-to-Server)

For service accounts (domain-wide delegation):

```bash
# .env file
GOOGLE_SERVICE_ACCOUNT_EMAIL=nexus-service@project-id.iam.gserviceaccount.com
GOOGLE_SERVICE_ACCOUNT_KEY='{"type":"service_account","project_id":"nexus-gmail",...}'
GOOGLE_SERVICE_ACCOUNT_IMPERSONATE=admin@yourdomain.com
GOOGLE_ADMIN_SCOPES=https://www.googleapis.com/auth/gmail.send
```

---

## Step 7: Implementation Examples

### Node.js Example

```javascript
const { google } = require('googleapis');
const OAuth2 = google.auth.OAuth2;

// Initialize OAuth2 client
const oauth2Client = new OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URI
);

// Generate authentication URL
const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/gmail.send'
  ],
  prompt: 'consent'
});

console.log('Authorize this app by visiting:', authUrl);

// Exchange authorization code for tokens
async function getTokens(code) {
  const { tokens } = await oauth2Client.getToken(code);
  oauth2Client.setCredentials(tokens);
  
  // Save tokens to database
  await saveTokens(tokens);
  
  return tokens;
}

// Send email using Gmail API
async function sendEmail(to, subject, body) {
  const gmail = google.gmail({ version: 'v1', auth: oauth2Client });
  
  const email = [
    `To: ${to}`,
    'Content-Type: text/html; charset=utf-8',
    'MIME-Version: 1.0',
    `Subject: ${subject}`,
    '',
    body
  ].join('\n');
  
  const encodedEmail = Buffer.from(email)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
  
  const response = await gmail.users.messages.send({
    userId: 'me',
    requestBody: {
      raw: encodedEmail
    }
  });
  
  return response.data;
}

// Refresh access token
async function refreshAccessToken(refreshToken) {
  oauth2Client.setCredentials({
    refresh_token: refreshToken
  });
  
  const { credentials } = await oauth2Client.refreshAccessToken();
  await saveTokens(credentials);
  
  return credentials;
}
```

### Python Example

```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import base64
from email.mime.text import MIMEText

# OAuth 2.0 scopes
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/gmail.send'
]

# Initialize OAuth flow
flow = Flow.from_client_config(
    {
        "web": {
            "client_id": os.getenv('GOOGLE_CLIENT_ID'),
            "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
            "redirect_uris": [os.getenv('GOOGLE_REDIRECT_URI')],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    },
    scopes=SCOPES
)

flow.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')

# Generate authorization URL
auth_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'
)

print(f'Please visit: {auth_url}')

# Exchange authorization code for tokens
def get_tokens(code):
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Save tokens
    save_tokens(credentials)
    
    return credentials

# Send email
def send_email(to, subject, body):
    credentials = load_credentials()
    
    service = build('gmail', 'v1', credentials=credentials)
    
    message = MIMEText(body, 'html')
    message['to'] = to
    message['subject'] = subject
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    result = service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()
    
    return result

# Refresh token
def refresh_token(credentials):
    credentials.refresh(Request())
    save_tokens(credentials)
    return credentials
```

---

## Step 8: Testing the Integration

### Test OAuth Flow

1. Navigate to your authorization URL
2. Sign in with Google account
3. Review requested permissions
4. Click **"Allow"**
5. Verify redirect to callback URL with authorization code
6. Exchange code for tokens
7. Test API calls

### Test Email Sending

```bash
# Using curl to test API endpoint
curl -X POST https://your-nexus-domain.com/v1/email/send \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Test Email from Nexus",
    "body": "<h1>Hello!</h1><p>This is a test email.</p>"
  }'
```

### Verify Scopes

```javascript
// Check granted scopes
const tokenInfo = await oauth2Client.getTokenInfo(accessToken);
console.log('Granted scopes:', tokenInfo.scopes);
```

---

## Scope Reference

### Complete Scope List

| Scope | Description | Use Case |
|-------|-------------|----------|
| `openid` | OpenID Connect | User authentication |
| `email` | User's email address | User identification |
| `profile` | User's basic profile | User information |
| `gmail.readonly` | Read all emails | Email monitoring |
| `gmail.send` | Send emails | Notifications, alerts |
| `gmail.compose` | Manage drafts | Draft management |
| `gmail.modify` | Modify emails | Labels, archiving |
| `gmail.labels` | Manage labels | Organization |
| `gmail.settings.basic` | Basic settings | Configuration |
| `gmail.settings.sharing` | Sharing settings | Delegation |
| `gmail.metadata` | Email metadata only | Lightweight access |

### Minimal Scopes for Nexus

For basic email notifications:
```
openid
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/gmail.send
```

For full email integration:
```
openid
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.labels
```

---

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Encrypt tokens** at rest in database
4. **Implement token refresh** logic
5. **Set token expiration** and cleanup
6. **Use HTTPS** for all OAuth callbacks
7. **Validate redirect URIs** against whitelist
8. **Implement CSRF protection** with state parameter
9. **Log OAuth events** for audit trail
10. **Rotate client secrets** periodically

---

## Troubleshooting

### Common Issues

**Error: redirect_uri_mismatch**
- Ensure redirect URI exactly matches authorized URI in Google Console
- Check for trailing slashes
- Verify protocol (http vs https)

**Error: invalid_grant**
- Refresh token expired or revoked
- Re-authorize user to obtain new tokens
- Check token storage/retrieval

**Error: insufficient_permissions**
- Requested scope not granted
- User needs to re-authorize with additional scopes

**Error: quota_exceeded**
- Gmail API quota exceeded
- Implement rate limiting
- Request quota increase in Google Console

**Tokens not refreshing**
- Ensure `access_type: 'offline'` in auth URL
- Use `prompt: 'consent'` to force consent
- Check refresh token is saved

---

## Rate Limits & Quotas

### Gmail API Quotas (Free Tier)

- **Daily sending limit**: 100 emails/day (Gmail), 2000/day (Workspace)
- **Quota units per day**: 1,000,000,000
- **Per-user rate limit**: 250 quota units/second

### Quota Costs

| Operation | Quota Cost |
|-----------|------------|
| Send email | 100 units |
| Read email | 5 units |
| List messages | 5 units |
| Modify labels | 5 units |

### Requesting Quota Increase

1. Go to Google Cloud Console
2. Navigate to **"APIs & Services"** → **"Quotas"**
3. Select **"Gmail API"**
4. Click **"Edit Quotas"**
5. Fill out request form
6. Explain use case and expected volume

---

## Sample Environment File

```bash
# .env.example

# Google OAuth 2.0
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_client_secret_here
GOOGLE_REDIRECT_URI=https://your-domain.com/oauth/callback

# Gmail API
GMAIL_API_VERSION=v1
GMAIL_SCOPES=openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/gmail.send
GMAIL_FROM_EMAIL=noreply@your-domain.com
GMAIL_FROM_NAME=Nexus Platform

# Token Storage
OAUTH_TOKEN_EXPIRY_BUFFER_MINUTES=5
OAUTH_TOKEN_REFRESH_ENABLED=true
OAUTH_TOKEN_ENCRYPTION_KEY=generate_random_32_byte_key
```

---

## Support

For Gmail OAuth setup assistance:

- **Google OAuth Documentation**: https://developers.google.com/identity/protocols/oauth2
- **Gmail API Documentation**: https://developers.google.com/gmail/api
- **Nexus Support**: support@nexus.example.com

---

**Last Updated**: 2025-11-03
