# OV/OI Modules API Documentation

## Overview

The OV (Open Visual) and OI (Open Interface) modules provide a complete authentication and augmented reality collaboration system.

## OV: Open Visual - Authentication Module

### Core Components

#### `FacialRecognition` Class

Handles facial detection and recognition using TensorFlow.js.

**Methods:**

- `initialize()` - Initialize the face detection model
  - Returns: `Promise<void>`

- `detectFaces(media)` - Detect faces in a video element or image
  - Parameters:
    - `media` (HTMLVideoElement|HTMLImageElement) - Media element to analyze
  - Returns: `Promise<Array>` - Array of detected faces

- `extractFeatures(faces)` - Extract facial features for recognition
  - Parameters:
    - `faces` (Array) - Detected faces from detectFaces
  - Returns: `Object` - Facial feature descriptor

- `compareFaces(features1, features2)` - Compare two facial feature descriptors
  - Parameters:
    - `features1` (Object) - First feature descriptor
    - `features2` (Object) - Second feature descriptor
  - Returns: `number` - Similarity score (0-1)

- `verifyFace(media, storedFeatures, threshold)` - Verify if a face matches stored features
  - Parameters:
    - `media` (HTMLVideoElement|HTMLImageElement) - Media element
    - `storedFeatures` (Object) - Previously stored facial features
    - `threshold` (number) - Similarity threshold (default 0.7)
  - Returns: `Promise<boolean>` - Whether the face matches

- `dispose()` - Cleanup resources

#### `Authentication` Class

Manages user authentication with facial recognition and password fallback.

**Methods:**

- `storeCredentials(username, password, facialFeatures)` - Store user credentials securely
  - Parameters:
    - `username` (string) - Username
    - `password` (string) - Password (will be hashed)
    - `facialFeatures` (Object) - Optional facial recognition features
  - Returns: `void`

- `authenticateWithFace(username, videoElement)` - Authenticate user with facial recognition
  - Parameters:
    - `username` (string) - Username
    - `videoElement` (HTMLVideoElement) - Video element with camera feed
  - Returns: `Promise<Object>` - Authentication result

- `authenticateWithPassword(username, password)` - Authenticate user with manual credentials
  - Parameters:
    - `username` (string) - Username
    - `password` (string) - Password
  - Returns: `Object` - Authentication result

- `userExists(username)` - Check if user exists
  - Parameters:
    - `username` (string) - Username to check
  - Returns: `boolean`

- `getUserProfile(username)` - Get user profile (without sensitive data)
  - Parameters:
    - `username` (string) - Username
  - Returns: `Object|null` - User profile

- `deleteUser(username)` - Delete user credentials
  - Parameters:
    - `username` (string) - Username to delete
  - Returns: `boolean` - Success status

#### `Registration` Class

Handles user registration with optional facial scan validation.

**Methods:**

- `captureFacialFeatures(videoElement)` - Capture facial features from video
  - Parameters:
    - `videoElement` (HTMLVideoElement) - Video element with camera feed
  - Returns: `Promise<Object>` - Capture result with features or error

- `registerUser(userDetails, videoElement, documentFile)` - Register new user
  - Parameters:
    - `userDetails` (Object) - User details (username, password, email, etc.)
    - `videoElement` (HTMLVideoElement) - Optional video element for facial scan
    - `documentFile` (File) - Optional document upload for validation
  - Returns: `Promise<Object>` - Registration result

- `addSecurityScan(username, videoElement)` - Add additional facial scans for security
  - Parameters:
    - `username` (string) - Username
    - `videoElement` (HTMLVideoElement) - Video element
  - Returns: `Promise<Object>` - Result of additional verification

#### `LoginInterface` Class

Main interface for login with facial recognition and fallback.

**Methods:**

- `initializeCamera(videoElement)` - Initialize camera for facial recognition
  - Parameters:
    - `videoElement` (HTMLVideoElement) - Video element to display camera feed
  - Returns: `Promise<boolean>` - Success status

- `stopCamera()` - Stop camera stream
  - Returns: `void`

- `attemptFacialLogin(username)` - Attempt facial recognition login
  - Parameters:
    - `username` (string) - Username to authenticate
  - Returns: `Promise<Object>` - Login result

- `fallbackLogin(username, password)` - Fallback to manual password login
  - Parameters:
    - `username` (string) - Username
    - `password` (string) - Password
  - Returns: `Object` - Login result

- `login(username, password)` - Combined login (tries facial, falls back to password)
  - Parameters:
    - `username` (string) - Username
    - `password` (string) - Password for fallback
  - Returns: `Promise<Object>` - Login result

- `getCurrentSession()` - Get current user session
  - Returns: `Object|null` - Current session or null

- `createSession(loginResult)` - Create user session after successful login
  - Parameters:
    - `loginResult` (Object) - Result from successful login
  - Returns: `void`

- `logout()` - Logout and clear session
  - Returns: `void`

- `isAuthenticated()` - Check if user is authenticated
  - Returns: `boolean`

- `redirectToOI(oiUrl)` - Redirect to OI after successful authentication
  - Parameters:
    - `oiUrl` (string) - URL of the OI interface (default: '/oi/interface.html')
  - Returns: `void`

## OI: Open Interface - AR Environment Module

### Core Components

#### `AREnvironment` Class

Manages augmented reality workspace allocation and rendering using Three.js.

**Methods:**

- `initialize()` - Initialize Three.js AR environment
  - Returns: `void`

- `allocateWorkspace(workspaceId, config)` - Allocate a new AR workspace
  - Parameters:
    - `workspaceId` (string) - Unique workspace identifier
    - `config` (Object) - Workspace configuration
  - Returns: `Object` - Workspace object

- `setActiveWorkspace(workspaceId)` - Set active workspace
  - Parameters:
    - `workspaceId` (string) - Workspace ID to activate
  - Returns: `boolean` - Success status

- `addObjectToWorkspace(workspaceId, object, metadata)` - Add 3D object to workspace
  - Parameters:
    - `workspaceId` (string) - Target workspace
    - `object` (THREE.Object3D) - 3D object to add
    - `metadata` (Object) - Object metadata
  - Returns: `Object|boolean` - Object data or false

- `createFileObject(fileInfo)` - Create a file representation in AR space
  - Parameters:
    - `fileInfo` (Object) - File information
  - Returns: `THREE.Object3D` - 3D file representation

- `addCollaborator(workspaceId, userId, userData)` - Add collaborator to workspace
  - Parameters:
    - `workspaceId` (string) - Workspace ID
    - `userId` (string) - User ID
    - `userData` (Object) - User data
  - Returns: `Object|boolean` - Collaborator object or false

- `removeWorkspace(workspaceId)` - Remove workspace
  - Parameters:
    - `workspaceId` (string) - Workspace to remove
  - Returns: `boolean` - Success status

- `getWorkspaceInfo(workspaceId)` - Get workspace information
  - Parameters:
    - `workspaceId` (string) - Workspace ID
  - Returns: `Object|null` - Workspace info

- `dispose()` - Cleanup and dispose resources
  - Returns: `void`

#### `AnalyticsEngine` Class

Provides telemetry feeds and analytics for the AR environment.

**Methods:**

- `enableTelemetry()` - Enable telemetry collection
  - Returns: `void`

- `disableTelemetry()` - Disable telemetry collection
  - Returns: `void`

- `toggleTelemetry()` - Toggle telemetry on/off
  - Returns: `boolean` - New telemetry state

- `trackUserActivity(userId, action, data)` - Track user activity
  - Parameters:
    - `userId` (string) - User ID
    - `action` (string) - Action type
    - `data` (Object) - Additional data
  - Returns: `void`

- `updateActiveUsers(count)` - Update active users count
  - Parameters:
    - `count` (number) - Number of active users
  - Returns: `void`

- `updateWorkspaceCount(count)` - Update workspace count
  - Parameters:
    - `count` (number) - Number of workspaces
  - Returns: `void`

- `trackPerformance(perfData)` - Track performance metrics
  - Parameters:
    - `perfData` (Object) - Performance data (fps, latency, renderTime)
  - Returns: `void`

- `calculateFPS()` - Calculate FPS (frames per second)
  - Returns: `number` - Current FPS

- `getCurrentMetrics()` - Get current metrics
  - Returns: `Object` - Current metrics snapshot

- `getMetricsHistory(limit)` - Get metrics history
  - Parameters:
    - `limit` (number) - Maximum number of records (default 100)
  - Returns: `Array` - Metrics history

- `getAggregatedStats(timeWindow)` - Get aggregated statistics
  - Parameters:
    - `timeWindow` (number) - Time window in milliseconds (default 60000)
  - Returns: `Object` - Aggregated statistics

- `subscribe(eventType, callback)` - Subscribe to analytics events
  - Parameters:
    - `eventType` (string) - Event type (metrics, activity, performance)
    - `callback` (Function) - Callback function
  - Returns: `string` - Subscription ID

- `unsubscribe(subscriptionId)` - Unsubscribe from analytics events
  - Parameters:
    - `subscriptionId` (string) - Subscription ID
  - Returns: `void`

- `exportData(format)` - Export analytics data
  - Parameters:
    - `format` (string) - Export format ('json' or 'csv', default 'json')
  - Returns: `string` - Exported data

- `clearData()` - Clear all analytics data
  - Returns: `void`

#### `OpenInterface` Class

Main interface controller for the OI AR environment.

**Methods:**

- `initialize(userSession)` - Initialize the Open Interface
  - Parameters:
    - `userSession` (Object) - User session from OV authentication
  - Returns: `void`

- `createWorkspace(name, config)` - Create a new collaborative workspace
  - Parameters:
    - `name` (string) - Workspace name
    - `config` (Object) - Workspace configuration
  - Returns: `string` - Workspace ID

- `switchWorkspace(workspaceId)` - Switch to a different workspace
  - Parameters:
    - `workspaceId` (string) - Target workspace ID
  - Returns: `boolean` - Success status

- `addFile(fileInfo)` - Add a file to the current workspace
  - Parameters:
    - `fileInfo` (Object) - File information
  - Returns: `Object` - File object data

- `inviteCollaborator(workspaceId, userId, userData)` - Invite collaborator to workspace
  - Parameters:
    - `workspaceId` (string) - Workspace ID
    - `userId` (string) - User ID to invite
    - `userData` (Object) - User data
  - Returns: `Object` - Collaborator object

- `getWorkspaceInfo(workspaceId)` - Get workspace information
  - Parameters:
    - `workspaceId` (string) - Workspace ID
  - Returns: `Object` - Workspace information

- `getAllWorkspaces()` - Get all workspaces
  - Returns: `Array` - Array of workspace information

- `toggleAnalytics()` - Toggle analytics telemetry
  - Returns: `boolean` - New telemetry state

- `getMetrics()` - Get current analytics metrics
  - Returns: `Object` - Current metrics

- `getAnalyticsDashboard()` - Get analytics dashboard data
  - Returns: `Object` - Dashboard data with current, history, and aggregated stats

- `subscribeToAnalytics(eventType, callback)` - Subscribe to analytics events
  - Parameters:
    - `eventType` (string) - Event type
    - `callback` (Function) - Callback function
  - Returns: `string` - Subscription ID

- `unsubscribeFromAnalytics(subscriptionId)` - Unsubscribe from analytics events
  - Parameters:
    - `subscriptionId` (string) - Subscription ID
  - Returns: `void`

- `exportAnalytics(format)` - Export analytics data
  - Parameters:
    - `format` (string) - Export format (default 'json')
  - Returns: `string` - Exported data

- `shutdown()` - Cleanup and shutdown
  - Returns: `void`

## Data Structures

### Authentication Result

```javascript
{
  success: boolean,
  method: 'facial' | 'password',
  username: string,
  timestamp: number,
  error?: string,
  fallbackRequired?: boolean
}
```

### Registration Result

```javascript
{
  success: boolean,
  username: string,
  hasFacialRecognition: boolean,
  documentValidated: boolean,
  timestamp: number,
  errors?: string[]
}
```

### User Session

```javascript
{
  username: string,
  method: 'facial' | 'password',
  timestamp: number,
  expiresAt: number
}
```

### Workspace Info

```javascript
{
  id: string,
  owner: string,
  createdAt: number,
  objectCount: number,
  collaborators: Array<{
    id: string,
    joinedAt: number
  }>
}
```

### Analytics Metrics

```javascript
{
  activeUsers: number,
  workspaces: number,
  interactions: number,
  performance: {
    fps: number,
    latency: number,
    renderTime: number
  },
  timestamp: number
}
```

## Security Considerations

1. **Encryption**: All credentials are encrypted using AES-256 encryption
2. **Password Hashing**: Passwords are hashed using SHA-256 before storage
3. **Session Management**: Sessions expire after 24 hours
4. **Facial Data**: Facial features are stored as numeric keypoint arrays, not images
5. **Local Storage**: All authentication data is stored in browser localStorage with encryption

## Browser Compatibility

- **OV Module**: Requires camera access and modern JavaScript features (ES6+)
- **OI Module**: Requires WebGL support for Three.js rendering
- **Recommended**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## Examples

### Basic Authentication Flow

```javascript
import LoginInterface from './ov/login-interface.js';

const loginInterface = new LoginInterface();
const videoElement = document.getElementById('video');

// Initialize camera
await loginInterface.initializeCamera(videoElement);

// Attempt login
const result = await loginInterface.login('username', 'password');

if (result.success) {
  loginInterface.createSession(result);
  loginInterface.redirectToOI();
}
```

### Creating a Workspace

```javascript
import OpenInterface from './oi/open-interface.js';

const session = JSON.parse(localStorage.getItem('ov_current_session'));
const oi = new OpenInterface(containerElement);

oi.initialize(session);

const workspaceId = oi.createWorkspace('My Workspace', {
  color: 0x0f766e
});
```

### Tracking Analytics

```javascript
// Subscribe to metrics updates
const subscriptionId = oi.subscribeToAnalytics('metrics', (metrics) => {
  console.log('FPS:', metrics.performance.fps);
  console.log('Active Users:', metrics.activeUsers);
});

// Export analytics data
const jsonData = oi.exportAnalytics('json');
console.log(jsonData);
```
