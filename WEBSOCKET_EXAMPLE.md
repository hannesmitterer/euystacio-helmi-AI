# WebSocket Example - Bidirectional Messaging

Complete guide and examples for implementing real-time bidirectional messaging using WebSockets in the Nexus platform.

## Overview

This guide provides:
- Node.js WebSocket server implementation
- WebSocket client examples
- Message format specifications
- Connection lifecycle management
- Error handling and reconnection logic
- Load balancing considerations

---

## Table of Contents

1. [Server Implementation](#server-implementation)
2. [Client Implementation](#client-implementation)
3. [Message Protocol](#message-protocol)
4. [Connection Management](#connection-management)
5. [Security](#security)
6. [Load Balancing](#load-balancing)
7. [Testing](#testing)

---

## Server Implementation

### Basic WebSocket Server (Node.js)

```javascript
// server.js
const WebSocket = require('ws');
const http = require('http');
const url = require('url');
const jwt = require('jsonwebtoken');

// Create HTTP server
const server = http.createServer();

// Create WebSocket server
const wss = new WebSocket.Server({
  server,
  path: '/v1/ws'
});

// Store active connections
const clients = new Map();

// Authentication middleware
function authenticate(request) {
  const params = url.parse(request.url, true).query;
  const token = params.token || request.headers['authorization']?.replace('Bearer ', '');
  
  if (!token) {
    throw new Error('Missing authentication token');
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    return decoded;
  } catch (error) {
    throw new Error('Invalid token');
  }
}

// WebSocket connection handler
wss.on('connection', (ws, request) => {
  let user = null;
  let clientId = null;
  
  try {
    // Authenticate connection
    user = authenticate(request);
    clientId = generateClientId();
    
    // Store connection
    clients.set(clientId, {
      ws,
      user,
      subscriptions: new Set(),
      connected_at: Date.now(),
      last_ping: Date.now()
    });
    
    console.log(`Client connected: ${clientId} (${user.email})`);
    
    // Send welcome message
    send(ws, {
      type: 'connected',
      id: generateMessageId(),
      timestamp: new Date().toISOString(),
      payload: {
        client_id: clientId,
        server_time: new Date().toISOString()
      }
    });
    
  } catch (error) {
    console.error('Authentication failed:', error.message);
    ws.send(JSON.stringify({
      type: 'error',
      error: {
        code: 'AUTH_FAILED',
        message: error.message
      }
    }));
    ws.close(4000, 'Authentication failed');
    return;
  }
  
  // Message handler
  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data);
      handleMessage(clientId, message);
    } catch (error) {
      console.error('Invalid message:', error.message);
      send(ws, {
        type: 'error',
        id: generateMessageId(),
        error: {
          code: 'INVALID_MESSAGE',
          message: 'Invalid JSON format'
        }
      });
    }
  });
  
  // Ping/pong for connection health
  ws.on('pong', () => {
    const client = clients.get(clientId);
    if (client) {
      client.last_ping = Date.now();
    }
  });
  
  // Close handler
  ws.on('close', (code, reason) => {
    console.log(`Client disconnected: ${clientId}, code: ${code}, reason: ${reason}`);
    clients.delete(clientId);
  });
  
  // Error handler
  ws.on('error', (error) => {
    console.error(`WebSocket error for ${clientId}:`, error);
    clients.delete(clientId);
  });
});

// Message handler
function handleMessage(clientId, message) {
  const client = clients.get(clientId);
  if (!client) return;
  
  const { type, id, payload } = message;
  
  switch (type) {
    case 'ping':
      send(client.ws, {
        type: 'pong',
        id,
        timestamp: new Date().toISOString()
      });
      break;
      
    case 'subscribe':
      handleSubscribe(clientId, payload);
      send(client.ws, {
        type: 'subscribed',
        id,
        timestamp: new Date().toISOString(),
        payload: {
          channel: payload.channel,
          filters: payload.filters
        }
      });
      break;
      
    case 'unsubscribe':
      handleUnsubscribe(clientId, payload);
      send(client.ws, {
        type: 'unsubscribed',
        id,
        timestamp: new Date().toISOString(),
        payload: {
          channel: payload.channel
        }
      });
      break;
      
    case 'command':
      handleCommand(clientId, payload)
        .then(result => {
          send(client.ws, {
            type: 'command.result',
            id,
            timestamp: new Date().toISOString(),
            payload: result
          });
        })
        .catch(error => {
          send(client.ws, {
            type: 'error',
            id,
            error: {
              code: 'COMMAND_FAILED',
              message: error.message
            }
          });
        });
      break;
      
    case 'telemetry':
      handleTelemetry(clientId, payload);
      send(client.ws, {
        type: 'ack',
        id,
        timestamp: new Date().toISOString()
      });
      break;
      
    default:
      send(client.ws, {
        type: 'error',
        id,
        error: {
          code: 'UNKNOWN_MESSAGE_TYPE',
          message: `Unknown message type: ${type}`
        }
      });
  }
}

// Subscribe handler
function handleSubscribe(clientId, payload) {
  const client = clients.get(clientId);
  if (!client) return;
  
  const { channel, filters } = payload;
  
  // Validate channel
  const validChannels = ['telemetry', 'commands', 'tasks', 'ai', 'events'];
  if (!validChannels.includes(channel)) {
    throw new Error(`Invalid channel: ${channel}`);
  }
  
  // Add subscription
  client.subscriptions.add(JSON.stringify({ channel, filters }));
  
  console.log(`Client ${clientId} subscribed to ${channel}`);
}

// Unsubscribe handler
function handleUnsubscribe(clientId, payload) {
  const client = clients.get(clientId);
  if (!client) return;
  
  const { channel } = payload;
  
  // Remove subscriptions matching channel
  for (const sub of client.subscriptions) {
    const parsed = JSON.parse(sub);
    if (parsed.channel === channel) {
      client.subscriptions.delete(sub);
    }
  }
  
  console.log(`Client ${clientId} unsubscribed from ${channel}`);
}

// Broadcast message to subscribed clients
function broadcast(channel, message, filters = {}) {
  clients.forEach((client, clientId) => {
    // Check if client is subscribed to channel
    for (const sub of client.subscriptions) {
      const parsed = JSON.parse(sub);
      if (parsed.channel === channel) {
        // Apply filters
        if (matchesFilters(message, parsed.filters)) {
          send(client.ws, {
            type: `${channel}.update`,
            id: generateMessageId(),
            timestamp: new Date().toISOString(),
            payload: message
          });
        }
      }
    }
  });
}

// Helper functions
function send(ws, message) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(message));
  }
}

function generateClientId() {
  return `client-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

function generateMessageId() {
  return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

function matchesFilters(message, filters) {
  if (!filters) return true;
  
  for (const [key, value] of Object.entries(filters)) {
    if (message[key] !== value) {
      return false;
    }
  }
  
  return true;
}

// Heartbeat to detect broken connections
const heartbeatInterval = setInterval(() => {
  const now = Date.now();
  
  clients.forEach((client, clientId) => {
    // Close connections that haven't responded to ping in 60 seconds
    if (now - client.last_ping > 60000) {
      console.log(`Client ${clientId} timeout, closing connection`);
      client.ws.terminate();
      clients.delete(clientId);
      return;
    }
    
    // Send ping
    if (client.ws.readyState === WebSocket.OPEN) {
      client.ws.ping();
    }
  });
}, 30000); // Every 30 seconds

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, closing server...');
  clearInterval(heartbeatInterval);
  
  clients.forEach((client, clientId) => {
    client.ws.close(1000, 'Server shutting down');
  });
  
  wss.close(() => {
    console.log('WebSocket server closed');
    server.close(() => {
      console.log('HTTP server closed');
      process.exit(0);
    });
  });
});

// Start server
const PORT = process.env.WS_PORT || 3001;
server.listen(PORT, () => {
  console.log(`WebSocket server listening on port ${PORT}`);
});

module.exports = { wss, broadcast };
```

---

## Client Implementation

### Node.js Client

```javascript
// client.js
const WebSocket = require('ws');
const EventEmitter = require('events');

class NexusWSClient extends EventEmitter {
  constructor(url, token, options = {}) {
    super();
    this.url = url;
    this.token = token;
    this.options = {
      reconnect: true,
      reconnectInterval: 5000,
      maxReconnectAttempts: 10,
      ...options
    };
    
    this.ws = null;
    this.clientId = null;
    this.reconnectAttempts = 0;
    this.messageQueue = [];
    this.subscriptions = new Map();
    this.connected = false;
  }
  
  connect() {
    const url = `${this.url}?token=${this.token}`;
    this.ws = new WebSocket(url);
    
    this.ws.on('open', () => {
      console.log('WebSocket connected');
      this.connected = true;
      this.reconnectAttempts = 0;
      
      // Process queued messages
      while (this.messageQueue.length > 0) {
        const message = this.messageQueue.shift();
        this.send(message);
      }
      
      // Resubscribe to channels
      this.subscriptions.forEach((filters, channel) => {
        this.subscribe(channel, filters);
      });
      
      this.emit('connected');
    });
    
    this.ws.on('message', (data) => {
      try {
        const message = JSON.parse(data);
        this.handleMessage(message);
      } catch (error) {
        console.error('Failed to parse message:', error);
      }
    });
    
    this.ws.on('close', (code, reason) => {
      console.log(`WebSocket closed: ${code} - ${reason}`);
      this.connected = false;
      this.emit('disconnected', { code, reason });
      
      if (this.options.reconnect) {
        this.reconnect();
      }
    });
    
    this.ws.on('error', (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', error);
    });
    
    // Send periodic pings
    this.pingInterval = setInterval(() => {
      if (this.connected) {
        this.send({
          type: 'ping',
          id: this.generateId(),
          timestamp: new Date().toISOString()
        });
      }
    }, 30000);
  }
  
  reconnect() {
    if (this.reconnectAttempts >= this.options.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      this.emit('reconnect_failed');
      return;
    }
    
    this.reconnectAttempts++;
    console.log(`Reconnecting... (attempt ${this.reconnectAttempts})`);
    
    setTimeout(() => {
      this.connect();
    }, this.options.reconnectInterval);
  }
  
  handleMessage(message) {
    const { type, id, payload, error } = message;
    
    switch (type) {
      case 'connected':
        this.clientId = payload.client_id;
        console.log(`Client ID: ${this.clientId}`);
        break;
        
      case 'pong':
        // Heartbeat response
        break;
        
      case 'subscribed':
        console.log(`Subscribed to ${payload.channel}`);
        break;
        
      case 'unsubscribed':
        console.log(`Unsubscribed from ${payload.channel}`);
        break;
        
      case 'telemetry.update':
      case 'commands.update':
      case 'tasks.update':
      case 'ai.update':
      case 'events.update':
        this.emit(type, payload);
        break;
        
      case 'command.result':
        this.emit('command_result', payload);
        break;
        
      case 'ack':
        this.emit('ack', { id });
        break;
        
      case 'error':
        console.error('Server error:', error);
        this.emit('server_error', error);
        break;
        
      default:
        console.warn('Unknown message type:', type);
    }
  }
  
  send(message) {
    if (!this.connected) {
      this.messageQueue.push(message);
      return;
    }
    
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }
  
  subscribe(channel, filters = {}) {
    this.subscriptions.set(channel, filters);
    
    this.send({
      type: 'subscribe',
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      payload: { channel, filters }
    });
  }
  
  unsubscribe(channel) {
    this.subscriptions.delete(channel);
    
    this.send({
      type: 'unsubscribe',
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      payload: { channel }
    });
  }
  
  sendTelemetry(data) {
    this.send({
      type: 'telemetry',
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      payload: data
    });
  }
  
  executeCommand(command) {
    this.send({
      type: 'command',
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      payload: command
    });
  }
  
  disconnect() {
    clearInterval(this.pingInterval);
    this.options.reconnect = false;
    
    if (this.ws) {
      this.ws.close(1000, 'Client disconnecting');
    }
  }
  
  generateId() {
    return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Usage example
const client = new NexusWSClient(
  'wss://ws.nexus.example.com/v1',
  process.env.NEXUS_API_KEY
);

client.on('connected', () => {
  console.log('Connected to Nexus WebSocket server');
  
  // Subscribe to telemetry updates
  client.subscribe('telemetry', {
    device_id: 'device-001'
  });
  
  // Subscribe to command updates
  client.subscribe('commands');
});

client.on('telemetry.update', (data) => {
  console.log('Telemetry update:', data);
});

client.on('command_result', (result) => {
  console.log('Command result:', result);
});

client.on('error', (error) => {
  console.error('Client error:', error);
});

client.connect();

// Send telemetry
setInterval(() => {
  client.sendTelemetry({
    device_id: 'device-001',
    metrics: {
      cpu_usage: Math.random() * 100,
      memory_usage: Math.random() * 100
    }
  });
}, 5000);

module.exports = NexusWSClient;
```

### Browser Client

```javascript
// browser-client.js
class NexusWSClient {
  constructor(url, token, options = {}) {
    this.url = url;
    this.token = token;
    this.options = {
      reconnect: true,
      reconnectInterval: 5000,
      maxReconnectAttempts: 10,
      ...options
    };
    
    this.ws = null;
    this.clientId = null;
    this.reconnectAttempts = 0;
    this.messageQueue = [];
    this.subscriptions = new Map();
    this.connected = false;
    this.eventHandlers = new Map();
  }
  
  connect() {
    const url = `${this.url}?token=${this.token}`;
    this.ws = new WebSocket(url);
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.connected = true;
      this.reconnectAttempts = 0;
      
      // Process queued messages
      while (this.messageQueue.length > 0) {
        const message = this.messageQueue.shift();
        this.send(message);
      }
      
      // Resubscribe
      this.subscriptions.forEach((filters, channel) => {
        this.subscribe(channel, filters);
      });
      
      this.trigger('connected');
    };
    
    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (error) {
        console.error('Failed to parse message:', error);
      }
    };
    
    this.ws.onclose = (event) => {
      console.log(`WebSocket closed: ${event.code} - ${event.reason}`);
      this.connected = false;
      this.trigger('disconnected', { code: event.code, reason: event.reason });
      
      if (this.options.reconnect) {
        this.reconnect();
      }
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.trigger('error', error);
    };
    
    // Ping interval
    this.pingInterval = setInterval(() => {
      if (this.connected) {
        this.send({
          type: 'ping',
          id: this.generateId(),
          timestamp: new Date().toISOString()
        });
      }
    }, 30000);
  }
  
  reconnect() {
    if (this.reconnectAttempts >= this.options.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      this.trigger('reconnect_failed');
      return;
    }
    
    this.reconnectAttempts++;
    console.log(`Reconnecting... (attempt ${this.reconnectAttempts})`);
    
    setTimeout(() => {
      this.connect();
    }, this.options.reconnectInterval);
  }
  
  handleMessage(message) {
    const { type, payload } = message;
    
    switch (type) {
      case 'connected':
        this.clientId = payload.client_id;
        break;
        
      case 'telemetry.update':
      case 'commands.update':
      case 'tasks.update':
        this.trigger(type, payload);
        break;
    }
  }
  
  send(message) {
    if (!this.connected) {
      this.messageQueue.push(message);
      return;
    }
    
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }
  
  subscribe(channel, filters = {}) {
    this.subscriptions.set(channel, filters);
    this.send({
      type: 'subscribe',
      id: this.generateId(),
      payload: { channel, filters }
    });
  }
  
  on(event, handler) {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, []);
    }
    this.eventHandlers.get(event).push(handler);
  }
  
  trigger(event, data) {
    const handlers = this.eventHandlers.get(event) || [];
    handlers.forEach(handler => handler(data));
  }
  
  disconnect() {
    clearInterval(this.pingInterval);
    this.options.reconnect = false;
    if (this.ws) {
      this.ws.close(1000, 'Client disconnecting');
    }
  }
  
  generateId() {
    return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Usage in browser
const client = new NexusWSClient(
  'wss://ws.nexus.example.com/v1',
  'YOUR_API_KEY'
);

client.on('connected', () => {
  console.log('Connected!');
  client.subscribe('telemetry', { device_id: 'device-001' });
});

client.on('telemetry.update', (data) => {
  console.log('Telemetry:', data);
  // Update UI
});

client.connect();
```

---

## Message Protocol

### Message Format

All messages use JSON format:

```json
{
  "type": "message_type",
  "id": "unique-message-id",
  "timestamp": "2025-11-03T01:53:54.518Z",
  "payload": {
    // Message-specific data
  }
}
```

### Message Types

| Type | Direction | Description |
|------|-----------|-------------|
| `ping` | Client → Server | Heartbeat |
| `pong` | Server → Client | Heartbeat response |
| `subscribe` | Client → Server | Subscribe to channel |
| `subscribed` | Server → Client | Subscription confirmed |
| `unsubscribe` | Client → Server | Unsubscribe from channel |
| `unsubscribed` | Server → Client | Unsubscription confirmed |
| `telemetry` | Client → Server | Send telemetry |
| `telemetry.update` | Server → Client | Telemetry broadcast |
| `command` | Client → Server | Execute command |
| `command.result` | Server → Client | Command result |
| `error` | Server → Client | Error message |
| `ack` | Server → Client | Acknowledgment |

---

## Connection Management

### Reconnection Strategy

```javascript
class ReconnectionHandler {
  constructor(client, options = {}) {
    this.client = client;
    this.attempts = 0;
    this.maxAttempts = options.maxAttempts || 10;
    this.baseDelay = options.baseDelay || 1000;
    this.maxDelay = options.maxDelay || 30000;
  }
  
  reconnect() {
    if (this.attempts >= this.maxAttempts) {
      console.error('Max reconnection attempts reached');
      return false;
    }
    
    // Exponential backoff with jitter
    const delay = Math.min(
      this.baseDelay * Math.pow(2, this.attempts) + Math.random() * 1000,
      this.maxDelay
    );
    
    console.log(`Reconnecting in ${delay}ms (attempt ${this.attempts + 1})`);
    
    setTimeout(() => {
      this.attempts++;
      this.client.connect();
    }, delay);
    
    return true;
  }
  
  reset() {
    this.attempts = 0;
  }
}
```

---

## Security

### Authentication

```javascript
// Server-side token validation
const jwt = require('jsonwebtoken');

function authenticateWS(request) {
  const token = extractToken(request);
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],
      maxAge: '1h'
    });
    
    return decoded;
  } catch (error) {
    throw new Error('Authentication failed');
  }
}
```

### Rate Limiting

```javascript
const rateLimit = new Map();

function checkRateLimit(clientId) {
  const now = Date.now();
  const window = 60000; // 1 minute
  const maxMessages = 100;
  
  if (!rateLimit.has(clientId)) {
    rateLimit.set(clientId, []);
  }
  
  const timestamps = rateLimit.get(clientId);
  const recent = timestamps.filter(t => now - t < window);
  
  if (recent.length >= maxMessages) {
    throw new Error('Rate limit exceeded');
  }
  
  recent.push(now);
  rateLimit.set(clientId, recent);
}
```

---

## Load Balancing

### Nginx Configuration

```nginx
upstream websocket_backend {
    ip_hash;
    server backend1.example.com:3001;
    server backend2.example.com:3001;
    server backend3.example.com:3001;
}

server {
    listen 443 ssl;
    server_name ws.nexus.example.com;
    
    location /v1/ws {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_read_timeout 86400;
        proxy_connect_timeout 60;
        proxy_send_timeout 60;
    }
}
```

---

## Testing

### Unit Tests

```javascript
const assert = require('assert');
const WebSocket = require('ws');

describe('WebSocket Server', () => {
  it('should accept authenticated connections', (done) => {
    const ws = new WebSocket(`ws://localhost:3001/v1/ws?token=${validToken}`);
    
    ws.on('open', () => {
      ws.close();
      done();
    });
    
    ws.on('error', done);
  });
  
  it('should reject unauthenticated connections', (done) => {
    const ws = new WebSocket('ws://localhost:3001/v1/ws');
    
    ws.on('close', (code) => {
      assert.strictEqual(code, 4000);
      done();
    });
  });
});
```

---

**Last Updated**: 2025-11-03
