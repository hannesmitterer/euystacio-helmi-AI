# Backend Integration Configuration

## Backend Server

The OV/OI modules now integrate with a backend server for enhanced functionality:

**Backend URL**: `https://oi-x3xa.onrender.com`

## Features

### Backend-Enabled Features

- **User Authentication**: Registration and login are handled by the backend API
- **Workspace Management**: Workspaces are synchronized with the backend
- **File Storage**: File metadata is stored on the backend
- **Analytics Tracking**: User activity and metrics are sent to the backend
- **Session Management**: JWT tokens are used for authenticated requests

### Local Fallback

All modules include a local fallback mode that uses:
- LocalStorage for credentials (with AES-256 encryption)
- Client-side workspace management
- Local analytics tracking

To disable backend integration and use only local storage, set `useBackend = false` in:
- `ov/auth/authentication.js`
- `ov/auth/registration.js`
- `oi/open-interface.js`

## API Endpoints

The backend API client (`ov/backend-api.js`) communicates with the following endpoints:

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with password
- `POST /api/auth/login/facial` - Login with facial recognition
- `GET /api/auth/verify` - Verify current session
- `POST /api/auth/logout` - Logout

### Workspaces
- `POST /api/workspaces` - Create workspace
- `GET /api/workspaces` - Get all workspaces
- `GET /api/workspaces/:id` - Get specific workspace
- `PUT /api/workspaces/:id` - Update workspace
- `DELETE /api/workspaces/:id` - Delete workspace
- `POST /api/workspaces/:id/files` - Add file to workspace
- `POST /api/workspaces/:id/collaborators` - Add collaborator

### Analytics
- `POST /api/analytics/events` - Track event
- `GET /api/analytics` - Get analytics data

### File Upload
- `POST /api/upload` - Upload files (documents, avatars, etc.)

### User Profile
- `PUT /api/users/profile` - Update user profile

## Authentication Flow

### Registration
1. User fills registration form with optional facial scan
2. Frontend captures facial features using TensorFlow.js
3. Data is sent to `POST /api/auth/register`
4. Backend stores user data and returns success
5. User can now login

### Login with Facial Recognition
1. User enters username and starts camera
2. Frontend captures facial features
3. Features sent to `POST /api/auth/login/facial`
4. Backend verifies features and returns JWT token
5. Token stored in localStorage for subsequent requests

### Login with Password
1. User enters username and password
2. Credentials sent to `POST /api/auth/login`
3. Backend verifies credentials and returns JWT token
4. Token stored in localStorage

## Security

### Token Storage
- JWT tokens are stored in localStorage under key `ov_auth_token`
- Tokens are automatically included in all API requests via Authorization header
- Tokens expire after session timeout (configured on backend)

### Password Security
- Passwords are hashed using PBKDF2 before being sent to backend
- Backend performs additional hashing for storage
- Facial features are stored as numeric keypoints (no images)

### Encryption
- All API communication uses HTTPS
- Sensitive data is encrypted before transmission
- AES-256 encryption is used for local credential storage

## Error Handling

The backend API client includes comprehensive error handling:
- Network errors trigger local fallback mode
- Failed requests are logged to console
- User-friendly error messages are displayed in UI
- Automatic retry logic for transient failures

## Development vs Production

### Development Mode
- Backend URL: `https://oi-x3xa.onrender.com`
- Local fallback enabled for offline development
- Debug logging enabled

### Production Deployment
For production, update the following:
1. Configure backend URL in `ov/backend-api.js`
2. Enable CORS for your domain on backend
3. Configure proper SSL certificates
4. Set up monitoring and logging
5. Implement rate limiting
6. Add CDN for static assets

## Monitoring

The backend integration includes:
- Request/response logging
- Performance metrics tracking
- Error rate monitoring
- User activity analytics

Check browser console for detailed logs during development.

## Troubleshooting

### Backend Unavailable
If backend is unavailable, modules automatically fall back to local mode.

### Authentication Failures
- Check browser console for detailed error messages
- Verify backend URL is accessible
- Ensure CORS is configured correctly
- Check token expiration

### Workspace Sync Issues
- Workspaces are created locally first
- Backend sync happens asynchronously
- Check network tab for failed requests
- Verify authentication token is valid

## Future Enhancements

Planned backend integrations:
- Real-time collaboration via WebSockets
- Cloud storage for 3D assets
- Multi-device sync
- Advanced analytics dashboard
- Notification system
- User presence tracking
