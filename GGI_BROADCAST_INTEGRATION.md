# GGI Broadcast Integration Guide

Complete guide for integrating with the GGI (General Gateway Interface) Broadcast system for webhook-based event distribution and real-time notifications.

## Overview

The GGI Broadcast interface enables the Nexus platform to:
- Send broadcast messages to multiple subscribers
- Receive webhook notifications from external systems
- Integrate with third-party messaging platforms
- Distribute events to microservices
- Implement pub/sub patterns

---

## Table of Contents

1. [Architecture](#architecture)
2. [Webhook Configuration](#webhook-configuration)
3. [Sending Broadcasts](#sending-broadcasts)
4. [Receiving Webhooks](#receiving-webhooks)
5. [Event Types](#event-types)
6. [Security](#security)
7. [Examples](#examples)
8. [Testing](#testing)

---

## Architecture

```
┌─────────────────┐
│  Nexus Platform │
└────────┬────────┘
         │
    ┌────▼─────────────────┐
    │  GGI Broadcast       │
    │  Interface           │
    └────┬─────────────────┘
         │
    ┌────▼──────┬──────────┬──────────┐
    │           │          │          │
┌───▼────┐ ┌───▼────┐ ┌──▼─────┐ ┌──▼──────┐
│Webhook │ │Webhook │ │Webhook │ │Webhook  │
│Target 1│ │Target 2│ │Target 3│ │Target N │
└────────┘ └────────┘ └────────┘ └─────────┘
```

---

## Webhook Configuration

### Register Webhook Endpoint

**Endpoint:** `POST /broadcast/webhooks`

```json
{
  "name": "Analytics Service Webhook",
  "url": "https://analytics.example.com/webhooks/nexus",
  "events": [
    "telemetry.alert",
    "task.completed",
    "command.executed"
  ],
  "filters": {
    "device_id": "device-*",
    "priority": "high"
  },
  "auth": {
    "type": "bearer",
    "token": "webhook_secret_token_here"
  },
  "retry_policy": {
    "max_retries": 3,
    "backoff_multiplier": 2,
    "initial_delay_ms": 1000
  },
  "timeout_ms": 5000,
  "active": true
}
```

**Response:**

```json
{
  "webhook_id": "wh-abc123",
  "name": "Analytics Service Webhook",
  "url": "https://analytics.example.com/webhooks/nexus",
  "secret": "whsec_a1b2c3d4e5f6...",
  "created_at": "2025-11-03T01:53:54.518Z",
  "status": "active"
}
```

### List Webhooks

**Endpoint:** `GET /broadcast/webhooks`

### Update Webhook

**Endpoint:** `PATCH /broadcast/webhooks/{webhook_id}`

### Delete Webhook

**Endpoint:** `DELETE /broadcast/webhooks/{webhook_id}`

### Test Webhook

**Endpoint:** `POST /broadcast/webhooks/{webhook_id}/test`

Send a test event to verify webhook is working:

```json
{
  "event_type": "webhook.test",
  "test_data": {
    "message": "This is a test webhook delivery"
  }
}
```

---

## Sending Broadcasts

### Broadcast Event

**Endpoint:** `POST /broadcast/send`

Send an event to all subscribed webhooks:

```json
{
  "event_type": "telemetry.alert",
  "data": {
    "device_id": "device-12345",
    "alert_type": "high_cpu",
    "threshold": 80,
    "current_value": 95,
    "timestamp": "2025-11-03T01:53:54.518Z"
  },
  "metadata": {
    "priority": "high",
    "source": "telemetry-engine"
  },
  "filters": {
    "device_id": "device-12345"
  }
}
```

**Response:**

```json
{
  "broadcast_id": "bc-xyz789",
  "event_type": "telemetry.alert",
  "sent_at": "2025-11-03T01:53:54.520Z",
  "webhooks_notified": 5,
  "delivery_status": "processing"
}
```

### Broadcast Status

**Endpoint:** `GET /broadcast/{broadcast_id}/status`

**Response:**

```json
{
  "broadcast_id": "bc-xyz789",
  "event_type": "telemetry.alert",
  "sent_at": "2025-11-03T01:53:54.520Z",
  "webhooks_notified": 5,
  "deliveries": [
    {
      "webhook_id": "wh-abc123",
      "webhook_name": "Analytics Service",
      "status": "delivered",
      "attempts": 1,
      "delivered_at": "2025-11-03T01:53:54.750Z",
      "response_code": 200
    },
    {
      "webhook_id": "wh-def456",
      "webhook_name": "Monitoring Service",
      "status": "failed",
      "attempts": 3,
      "last_attempt_at": "2025-11-03T01:53:58.120Z",
      "error": "Connection timeout",
      "next_retry_at": "2025-11-03T01:54:06.120Z"
    }
  ]
}
```

---

## Receiving Webhooks

### Webhook Payload Format

All webhook deliveries use this format:

```json
{
  "webhook_id": "wh-abc123",
  "event_id": "evt-12345",
  "event_type": "telemetry.alert",
  "timestamp": "2025-11-03T01:53:54.518Z",
  "data": {
    "device_id": "device-12345",
    "alert_type": "high_cpu",
    "threshold": 80,
    "current_value": 95
  },
  "metadata": {
    "priority": "high",
    "source": "telemetry-engine"
  },
  "signature": "sha256=a1b2c3d4e5f6..."
}
```

### Webhook Signature Verification

All webhook deliveries include a signature for verification:

**Node.js Example:**

```javascript
const crypto = require('crypto');

function verifyWebhookSignature(payload, signature, secret) {
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(JSON.stringify(payload))
    .digest('hex');
  
  const signatureHash = signature.replace('sha256=', '');
  
  return crypto.timingSafeEqual(
    Buffer.from(signatureHash),
    Buffer.from(expectedSignature)
  );
}

// Express middleware
app.post('/webhooks/nexus', (req, res) => {
  const signature = req.headers['x-nexus-signature'];
  const secret = process.env.NEXUS_WEBHOOK_SECRET;
  
  if (!verifyWebhookSignature(req.body, signature, secret)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  
  // Process webhook
  const { event_type, data } = req.body;
  
  switch (event_type) {
    case 'telemetry.alert':
      handleTelemetryAlert(data);
      break;
    case 'task.completed':
      handleTaskCompleted(data);
      break;
    default:
      console.log('Unknown event type:', event_type);
  }
  
  res.status(200).json({ received: true });
});
```

**Python Example:**

```python
import hmac
import hashlib
import json

def verify_webhook_signature(payload, signature, secret):
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        json.dumps(payload).encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    signature_hash = signature.replace('sha256=', '')
    
    return hmac.compare_digest(signature_hash, expected_signature)

# Flask example
from flask import Flask, request, jsonify

@app.route('/webhooks/nexus', methods=['POST'])
def nexus_webhook():
    signature = request.headers.get('X-Nexus-Signature')
    secret = os.getenv('NEXUS_WEBHOOK_SECRET')
    
    if not verify_webhook_signature(request.json, signature, secret):
        return jsonify({'error': 'Invalid signature'}), 401
    
    event_type = request.json.get('event_type')
    data = request.json.get('data')
    
    if event_type == 'telemetry.alert':
        handle_telemetry_alert(data)
    elif event_type == 'task.completed':
        handle_task_completed(data)
    
    return jsonify({'received': True}), 200
```

### Webhook Response Requirements

Webhook endpoints must:
- Respond with HTTP 2xx status code for success
- Respond within timeout period (default: 5 seconds)
- Return JSON response body (optional)

**Success Response:**

```json
{
  "received": true,
  "processed": true,
  "message": "Event processed successfully"
}
```

**Error Response:**

```json
{
  "received": true,
  "processed": false,
  "error": "Processing failed: database connection error"
}
```

---

## Event Types

### Telemetry Events

| Event Type | Description | Data Schema |
|------------|-------------|-------------|
| `telemetry.frame` | New telemetry data received | `{ device_id, metrics, tags }` |
| `telemetry.alert` | Alert triggered by threshold | `{ device_id, alert_type, threshold, current_value }` |

### Command Events

| Event Type | Description | Data Schema |
|------------|-------------|-------------|
| `command.submitted` | Command queued for execution | `{ command_id, command, target }` |
| `command.started` | Command execution started | `{ command_id, started_at }` |
| `command.completed` | Command finished successfully | `{ command_id, result, duration_ms }` |
| `command.failed` | Command execution failed | `{ command_id, error, attempts }` |

### Task Events

| Event Type | Description | Data Schema |
|------------|-------------|-------------|
| `task.created` | New task created | `{ task_id, name, type }` |
| `task.started` | Task execution started | `{ task_id, started_at }` |
| `task.completed` | Task finished successfully | `{ task_id, result, duration_ms }` |
| `task.failed` | Task execution failed | `{ task_id, error, attempts }` |

### AI Events

| Event Type | Description | Data Schema |
|------------|-------------|-------------|
| `ai.agent.registered` | AI agent registered | `{ agent_id, capabilities }` |
| `ai.agent.offline` | AI agent went offline | `{ agent_id, last_seen }` |
| `ai.task.assigned` | AI task assigned to agent | `{ task_id, agent_id }` |
| `ai.task.completed` | AI task completed | `{ task_id, result }` |

---

## Security

### Authentication Methods

#### Bearer Token

```json
{
  "auth": {
    "type": "bearer",
    "token": "your_secret_token_here"
  }
}
```

Headers sent:
```http
Authorization: Bearer your_secret_token_here
```

#### Basic Auth

```json
{
  "auth": {
    "type": "basic",
    "username": "webhook_user",
    "password": "webhook_password"
  }
}
```

Headers sent:
```http
Authorization: Basic d2ViaG9va191c2VyOndlYmhvb2tfcGFzc3dvcmQ=
```

#### Custom Headers

```json
{
  "auth": {
    "type": "custom",
    "headers": {
      "X-API-Key": "your_api_key",
      "X-Custom-Header": "custom_value"
    }
  }
}
```

### IP Whitelist

Restrict webhook deliveries to specific IP addresses:

```json
{
  "webhook_id": "wh-abc123",
  "security": {
    "ip_whitelist": [
      "203.0.113.0/24",
      "198.51.100.42"
    ]
  }
}
```

### HTTPS Required

All webhook URLs must use HTTPS in production:

```json
{
  "url": "https://your-service.com/webhooks/nexus"
}
```

---

## Examples

### Complete Integration Example (Node.js)

```javascript
const express = require('express');
const crypto = require('crypto');
const axios = require('axios');

const app = express();
app.use(express.json());

// Webhook secret from Nexus
const WEBHOOK_SECRET = process.env.NEXUS_WEBHOOK_SECRET;

// Verify webhook signature
function verifySignature(payload, signature) {
  const expectedSignature = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(JSON.stringify(payload))
    .digest('hex');
  
  const signatureHash = signature.replace('sha256=', '');
  
  return crypto.timingSafeEqual(
    Buffer.from(signatureHash),
    Buffer.from(expectedSignature)
  );
}

// Webhook endpoint
app.post('/webhooks/nexus', async (req, res) => {
  const signature = req.headers['x-nexus-signature'];
  
  // Verify signature
  if (!signature || !verifySignature(req.body, signature)) {
    console.error('Invalid webhook signature');
    return res.status(401).json({ error: 'Invalid signature' });
  }
  
  const { event_id, event_type, data, timestamp } = req.body;
  
  console.log(`Received event: ${event_type} (${event_id})`);
  
  try {
    // Process event based on type
    switch (event_type) {
      case 'telemetry.alert':
        await handleTelemetryAlert(data);
        break;
        
      case 'task.completed':
        await handleTaskCompleted(data);
        break;
        
      case 'command.executed':
        await handleCommandExecuted(data);
        break;
        
      default:
        console.log(`Unhandled event type: ${event_type}`);
    }
    
    // Return success
    res.status(200).json({
      received: true,
      event_id,
      processed: true,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Error processing webhook:', error);
    
    res.status(500).json({
      received: true,
      event_id,
      processed: false,
      error: error.message
    });
  }
});

// Event handlers
async function handleTelemetryAlert(data) {
  const { device_id, alert_type, current_value } = data;
  
  console.log(`Alert: ${alert_type} on ${device_id}: ${current_value}`);
  
  // Send notification to Slack
  await axios.post(process.env.SLACK_WEBHOOK_URL, {
    text: `🚨 Alert: ${alert_type} on ${device_id}`,
    attachments: [{
      color: 'danger',
      fields: [
        { title: 'Device', value: device_id, short: true },
        { title: 'Alert Type', value: alert_type, short: true },
        { title: 'Current Value', value: current_value, short: true }
      ]
    }]
  });
}

async function handleTaskCompleted(data) {
  const { task_id, result, duration_ms } = data;
  
  console.log(`Task ${task_id} completed in ${duration_ms}ms`);
  
  // Update database
  await db.tasks.update({
    where: { id: task_id },
    data: {
      status: 'completed',
      result,
      completed_at: new Date()
    }
  });
}

async function handleCommandExecuted(data) {
  const { command_id, result } = data;
  
  console.log(`Command ${command_id} executed:`, result);
  
  // Log to analytics
  await analytics.track('command_executed', {
    command_id,
    success: result.success,
    duration: result.duration_ms
  });
}

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Webhook server listening on port ${PORT}`);
});
```

### Register Webhook with Nexus

```javascript
const axios = require('axios');

async function registerWebhook() {
  const response = await axios.post(
    'https://api.nexus.example.com/v1/broadcast/webhooks',
    {
      name: 'My Service Webhook',
      url: 'https://my-service.com/webhooks/nexus',
      events: [
        'telemetry.alert',
        'task.completed',
        'command.executed'
      ],
      filters: {
        priority: 'high'
      },
      auth: {
        type: 'bearer',
        token: process.env.MY_SERVICE_TOKEN
      },
      retry_policy: {
        max_retries: 3,
        backoff_multiplier: 2,
        initial_delay_ms: 1000
      },
      timeout_ms: 5000
    },
    {
      headers: {
        'Authorization': `Bearer ${process.env.NEXUS_API_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  console.log('Webhook registered:', response.data);
  
  // Save webhook secret
  process.env.NEXUS_WEBHOOK_SECRET = response.data.secret;
  
  return response.data;
}

registerWebhook().catch(console.error);
```

---

## Testing

### Test Webhook Delivery

```bash
# Send test event
curl -X POST https://api.nexus.example.com/v1/broadcast/webhooks/wh-abc123/test \
  -H "Authorization: Bearer $NEXUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "webhook.test",
    "test_data": {
      "message": "This is a test"
    }
  }'
```

### Mock Webhook Server

```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.post('/webhooks/nexus', (req, res) => {
  console.log('Received webhook:');
  console.log(JSON.stringify(req.body, null, 2));
  console.log('Headers:', req.headers);
  
  res.status(200).json({
    received: true,
    timestamp: new Date().toISOString()
  });
});

app.listen(3000, () => {
  console.log('Mock webhook server listening on port 3000');
});
```

### Integration Tests

```javascript
const assert = require('assert');
const axios = require('axios');

describe('GGI Broadcast Integration', () => {
  it('should deliver webhook successfully', async () => {
    // Send broadcast
    const broadcast = await axios.post(
      'https://api.nexus.example.com/v1/broadcast/send',
      {
        event_type: 'test.event',
        data: { message: 'test' }
      },
      {
        headers: { 'Authorization': `Bearer ${API_KEY}` }
      }
    );
    
    // Wait for delivery
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Check status
    const status = await axios.get(
      `https://api.nexus.example.com/v1/broadcast/${broadcast.data.broadcast_id}/status`,
      {
        headers: { 'Authorization': `Bearer ${API_KEY}` }
      }
    );
    
    assert.strictEqual(status.data.deliveries[0].status, 'delivered');
  });
});
```

---

## Troubleshooting

### Common Issues

**Webhook not receiving events:**
- Verify webhook is active
- Check event type filters
- Verify URL is accessible
- Check firewall/security groups

**Signature verification fails:**
- Ensure using correct secret
- Verify payload is stringified correctly
- Check for charset/encoding issues

**Deliveries timing out:**
- Reduce processing time in webhook handler
- Increase timeout_ms in webhook config
- Return 200 immediately, process asynchronously

**Too many retries:**
- Fix errors in webhook handler
- Check network connectivity
- Verify response format

---

## Best Practices

1. **Return 2xx quickly** - Process webhooks asynchronously
2. **Verify signatures** - Always validate webhook authenticity
3. **Handle duplicates** - Use event_id for idempotency
4. **Log events** - Keep audit trail of webhook deliveries
5. **Monitor failures** - Set up alerts for webhook failures
6. **Use HTTPS** - Encrypt webhook data in transit
7. **Implement retries** - Handle transient failures gracefully
8. **Filter events** - Subscribe only to needed events

---

**Last Updated**: 2025-11-03
