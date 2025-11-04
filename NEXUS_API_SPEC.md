# Nexus API Specification

**Version:** 1.0.0  
**Status:** Draft  
**Last Updated:** 2025-11-03

## Overview

The Nexus API provides a unified interface for telemetry collection, command execution, task management, AI coordination, and event streaming. It supports both REST and WebSocket protocols to enable real-time bidirectional communication between clients and the Nexus coordination platform.

## Table of Contents

1. [Architecture](#architecture)
2. [Authentication & Authorization](#authentication--authorization)
3. [Telemetry API](#telemetry-api)
4. [Command API](#command-api)
5. [Task Management API](#task-management-api)
6. [AI Coordination API](#ai-coordination-api)
7. [Security & Rate Limiting](#security--rate-limiting)
8. [Event Streaming](#event-streaming)
9. [WebSocket Protocol](#websocket-protocol)
10. [Error Handling](#error-handling)
11. [Example Workflows](#example-workflows)

---

## Architecture

### Protocol Support

- **REST API**: HTTP/HTTPS for synchronous request-response operations
- **WebSocket**: WSS for real-time bidirectional messaging
- **gRPC** (optional): For high-performance internal service communication

### Core Components

```
┌─────────────────┐
│   API Gateway   │
│  (REST/WS/gRPC) │
└────────┬────────┘
         │
    ┌────┴────┐
    │  Nexus  │
    │  Core   │
    └────┬────┘
         │
    ┌────┴────────────────────┐
    │                         │
┌───▼───┐  ┌────▼────┐  ┌────▼────┐
│Telemetry│ │Command │ │  Task   │
│Engine  │ │Executor│ │Manager  │
└────────┘ └─────────┘ └─────────┘
```

### Base URLs

- **Production**: `https://api.nexus.example.com/v1`
- **Staging**: `https://api-staging.nexus.example.com/v1`
- **WebSocket**: `wss://ws.nexus.example.com/v1`

---

## Authentication & Authorization

### API Key Authentication

All API requests require an API key in the header:

```http
Authorization: Bearer YOUR_API_KEY
```

### OAuth 2.0 (Optional)

For user-scoped operations, OAuth 2.0 with JWT tokens is supported:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Scopes

- `telemetry:read` - Read telemetry data
- `telemetry:write` - Send telemetry data
- `command:execute` - Execute commands
- `task:read` - Read task information
- `task:write` - Create and update tasks
- `ai:coordinate` - AI coordination operations
- `admin` - Full administrative access

---

## Telemetry API

### Send Telemetry Frame

**Endpoint:** `POST /telemetry/frames`

Send telemetry data frames to the Nexus platform.

**Request Headers:**
```http
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

**Request Body:**
```json
{
  "device_id": "device-12345",
  "timestamp": "2025-11-03T01:53:54.518Z",
  "metrics": {
    "cpu_usage": 45.2,
    "memory_usage": 62.8,
    "disk_usage": 78.5,
    "network_latency_ms": 12.3
  },
  "tags": {
    "environment": "production",
    "region": "us-west-2",
    "service": "api-gateway"
  },
  "metadata": {
    "version": "1.2.3",
    "build": "abc123"
  }
}
```

**Response:**
```json
{
  "success": true,
  "frame_id": "frame-67890",
  "received_at": "2025-11-03T01:53:54.520Z"
}
```

**Status Codes:**
- `201 Created` - Telemetry frame successfully received
- `400 Bad Request` - Invalid frame format
- `401 Unauthorized` - Missing or invalid API key
- `429 Too Many Requests` - Rate limit exceeded

### Query Telemetry Data

**Endpoint:** `GET /telemetry/query`

Query historical telemetry data with filtering and aggregation.

**Query Parameters:**
- `device_id` (optional) - Filter by device ID
- `start_time` (required) - Start time (ISO 8601)
- `end_time` (required) - End time (ISO 8601)
- `metrics` (optional) - Comma-separated list of metrics
- `tags` (optional) - Tag filters in format `key:value`
- `aggregation` (optional) - `avg`, `min`, `max`, `sum`, `count`
- `interval` (optional) - Aggregation interval (e.g., `1m`, `5m`, `1h`)

**Example Request:**
```http
GET /telemetry/query?device_id=device-12345&start_time=2025-11-03T00:00:00Z&end_time=2025-11-03T02:00:00Z&metrics=cpu_usage,memory_usage&aggregation=avg&interval=5m
```

**Response:**
```json
{
  "query": {
    "device_id": "device-12345",
    "start_time": "2025-11-03T00:00:00Z",
    "end_time": "2025-11-03T02:00:00Z",
    "metrics": ["cpu_usage", "memory_usage"],
    "aggregation": "avg",
    "interval": "5m"
  },
  "data": [
    {
      "timestamp": "2025-11-03T00:00:00Z",
      "cpu_usage": 42.5,
      "memory_usage": 60.2
    },
    {
      "timestamp": "2025-11-03T00:05:00Z",
      "cpu_usage": 45.8,
      "memory_usage": 62.1
    }
  ],
  "total_points": 24
}
```

---

## Command API

### Execute Command

**Endpoint:** `POST /commands/execute`

Execute a command on a target device or service.

**Request Body:**
```json
{
  "command": "restart_service",
  "target": {
    "device_id": "device-12345",
    "service": "api-gateway"
  },
  "parameters": {
    "graceful": true,
    "timeout_seconds": 30
  },
  "async": true,
  "callback_url": "https://your-app.com/webhooks/command-result"
}
```

**Response (Async):**
```json
{
  "command_id": "cmd-abc123",
  "status": "pending",
  "submitted_at": "2025-11-03T01:53:54.530Z",
  "estimated_completion": "2025-11-03T01:54:24.530Z"
}
```

**Response (Sync):**
```json
{
  "command_id": "cmd-abc123",
  "status": "completed",
  "result": {
    "success": true,
    "message": "Service restarted successfully",
    "duration_ms": 2847
  },
  "completed_at": "2025-11-03T01:53:57.377Z"
}
```

### Get Command Status

**Endpoint:** `GET /commands/{command_id}`

**Response:**
```json
{
  "command_id": "cmd-abc123",
  "status": "completed",
  "command": "restart_service",
  "target": {
    "device_id": "device-12345",
    "service": "api-gateway"
  },
  "result": {
    "success": true,
    "message": "Service restarted successfully",
    "duration_ms": 2847
  },
  "submitted_at": "2025-11-03T01:53:54.530Z",
  "completed_at": "2025-11-03T01:53:57.377Z"
}
```

**Status Values:**
- `pending` - Command queued but not yet started
- `running` - Command currently executing
- `completed` - Command finished successfully
- `failed` - Command failed with error
- `timeout` - Command exceeded timeout limit
- `cancelled` - Command was cancelled

---

## Task Management API

### Create Task

**Endpoint:** `POST /tasks`

Create a new task with optional scheduling and dependencies.

**Request Body:**
```json
{
  "name": "Process daily analytics",
  "description": "Aggregate and process analytics data for the previous day",
  "type": "scheduled",
  "schedule": {
    "cron": "0 2 * * *",
    "timezone": "UTC"
  },
  "parameters": {
    "date": "yesterday",
    "output_format": "parquet"
  },
  "dependencies": ["task-xyz789"],
  "retry_policy": {
    "max_retries": 3,
    "backoff_multiplier": 2,
    "initial_delay_seconds": 60
  },
  "timeout_seconds": 3600,
  "tags": {
    "team": "analytics",
    "priority": "high"
  }
}
```

**Response:**
```json
{
  "task_id": "task-def456",
  "name": "Process daily analytics",
  "status": "scheduled",
  "created_at": "2025-11-03T01:53:54.540Z",
  "next_run": "2025-11-04T02:00:00.000Z"
}
```

### Get Task

**Endpoint:** `GET /tasks/{task_id}`

### List Tasks

**Endpoint:** `GET /tasks`

**Query Parameters:**
- `status` - Filter by status (`scheduled`, `running`, `completed`, `failed`)
- `type` - Filter by type
- `tags` - Filter by tags
- `limit` - Number of results (default: 50, max: 100)
- `offset` - Pagination offset

### Update Task

**Endpoint:** `PATCH /tasks/{task_id}`

### Delete Task

**Endpoint:** `DELETE /tasks/{task_id}`

### Execute Task Manually

**Endpoint:** `POST /tasks/{task_id}/execute`

Trigger a task execution outside of its schedule.

**Request Body:**
```json
{
  "parameters": {
    "date": "2025-11-02",
    "force": true
  }
}
```

---

## AI Coordination API

### Register AI Agent

**Endpoint:** `POST /ai/agents/register`

Register an AI agent with the Nexus coordination platform.

**Request Body:**
```json
{
  "agent_id": "agent-alpha-001",
  "name": "Analytics Agent",
  "type": "analytics",
  "capabilities": [
    "data_analysis",
    "anomaly_detection",
    "forecasting"
  ],
  "model": {
    "name": "gpt-4",
    "version": "2025-01-01",
    "provider": "openai"
  },
  "resources": {
    "max_concurrent_tasks": 5,
    "memory_limit_mb": 4096
  },
  "metadata": {
    "owner": "analytics-team",
    "region": "us-west-2"
  }
}
```

**Response:**
```json
{
  "agent_id": "agent-alpha-001",
  "status": "registered",
  "registered_at": "2025-11-03T01:53:54.550Z",
  "heartbeat_interval_seconds": 30
}
```

### Agent Heartbeat

**Endpoint:** `POST /ai/agents/{agent_id}/heartbeat`

Send periodic heartbeat to maintain agent registration.

**Request Body:**
```json
{
  "status": "idle",
  "current_tasks": 0,
  "resource_usage": {
    "cpu_percent": 12.5,
    "memory_mb": 1024
  }
}
```

### Request AI Task

**Endpoint:** `POST /ai/tasks`

Request an AI agent to perform a task.

**Request Body:**
```json
{
  "task_type": "analysis",
  "agent_preferences": {
    "capabilities": ["data_analysis"],
    "preferred_agents": ["agent-alpha-001"]
  },
  "input": {
    "dataset_id": "ds-12345",
    "analysis_type": "trend_detection",
    "parameters": {
      "lookback_days": 30,
      "confidence_threshold": 0.85
    }
  },
  "priority": "high",
  "timeout_seconds": 300
}
```

**Response:**
```json
{
  "task_id": "ai-task-ghi789",
  "assigned_agent": "agent-alpha-001",
  "status": "assigned",
  "created_at": "2025-11-03T01:53:54.560Z",
  "estimated_completion": "2025-11-03T01:58:54.560Z"
}
```

### Get AI Task Result

**Endpoint:** `GET /ai/tasks/{task_id}`

**Response:**
```json
{
  "task_id": "ai-task-ghi789",
  "status": "completed",
  "assigned_agent": "agent-alpha-001",
  "input": {
    "dataset_id": "ds-12345",
    "analysis_type": "trend_detection"
  },
  "result": {
    "trends": [
      {
        "metric": "user_signups",
        "direction": "increasing",
        "confidence": 0.92,
        "rate_per_day": 125.5
      }
    ],
    "anomalies": [],
    "summary": "Strong upward trend in user signups detected"
  },
  "created_at": "2025-11-03T01:53:54.560Z",
  "completed_at": "2025-11-03T01:56:12.340Z",
  "duration_ms": 137780
}
```

### AI Collaboration

**Endpoint:** `POST /ai/collaborate`

Enable multiple AI agents to collaborate on a complex task.

**Request Body:**
```json
{
  "collaboration_id": "collab-001",
  "task_description": "Analyze user behavior and generate recommendations",
  "agents": [
    {
      "agent_id": "agent-alpha-001",
      "role": "analyst"
    },
    {
      "agent_id": "agent-beta-002",
      "role": "recommender"
    }
  ],
  "workflow": {
    "steps": [
      {
        "step": 1,
        "agent": "agent-alpha-001",
        "action": "analyze_data",
        "output_to": "shared_context"
      },
      {
        "step": 2,
        "agent": "agent-beta-002",
        "action": "generate_recommendations",
        "input_from": "shared_context"
      }
    ]
  },
  "shared_context": {
    "dataset_id": "ds-12345",
    "user_segment": "premium_users"
  }
}
```

---

## Security & Rate Limiting

### Rate Limits

- **Telemetry API**: 1000 requests/minute per API key
- **Command API**: 100 requests/minute per API key
- **Task API**: 200 requests/minute per API key
- **AI Coordination API**: 500 requests/minute per API key

Rate limit headers are included in all responses:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1699000000
```

### Security Headers

All API responses include security headers:

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

### Data Encryption

- All data in transit uses TLS 1.3
- Sensitive fields are encrypted at rest using AES-256
- API keys are hashed using bcrypt

### Session Management

- JWT tokens expire after 1 hour
- Refresh tokens valid for 7 days
- Session cleanup runs every 15 minutes

---

## Event Streaming

### Subscribe to Events

**Endpoint:** `GET /events/stream` (Server-Sent Events)

Subscribe to real-time event streams.

**Query Parameters:**
- `event_types` - Comma-separated list of event types
- `filters` - JSON-encoded filter object

**Example:**
```http
GET /events/stream?event_types=telemetry.alert,command.completed
```

**Event Format:**
```
event: telemetry.alert
id: evt-12345
data: {"device_id":"device-12345","alert_type":"high_cpu","threshold":80,"current_value":95}

event: command.completed
id: evt-12346
data: {"command_id":"cmd-abc123","status":"completed","result":{"success":true}}
```

### Event Types

- `telemetry.frame` - New telemetry frame received
- `telemetry.alert` - Alert triggered by telemetry threshold
- `command.submitted` - Command submitted
- `command.started` - Command execution started
- `command.completed` - Command execution completed
- `command.failed` - Command execution failed
- `task.created` - New task created
- `task.started` - Task execution started
- `task.completed` - Task execution completed
- `task.failed` - Task execution failed
- `ai.agent.registered` - AI agent registered
- `ai.agent.offline` - AI agent went offline
- `ai.task.assigned` - AI task assigned to agent
- `ai.task.completed` - AI task completed

---

## WebSocket Protocol

### Connection

Connect to the WebSocket endpoint with authentication:

```javascript
const ws = new WebSocket('wss://ws.nexus.example.com/v1?token=YOUR_API_KEY');
```

### Message Format

All WebSocket messages use JSON format:

```json
{
  "type": "message_type",
  "id": "unique-message-id",
  "timestamp": "2025-11-03T01:53:54.570Z",
  "payload": {
    // Message-specific data
  }
}
```

### Client → Server Messages

#### Subscribe to Telemetry

```json
{
  "type": "subscribe",
  "id": "msg-001",
  "payload": {
    "channel": "telemetry",
    "filters": {
      "device_id": "device-12345"
    }
  }
}
```

#### Send Command

```json
{
  "type": "command",
  "id": "msg-002",
  "payload": {
    "command": "restart_service",
    "target": {
      "device_id": "device-12345"
    }
  }
}
```

### Server → Client Messages

#### Telemetry Update

```json
{
  "type": "telemetry.frame",
  "id": "msg-003",
  "timestamp": "2025-11-03T01:53:54.580Z",
  "payload": {
    "device_id": "device-12345",
    "metrics": {
      "cpu_usage": 45.2
    }
  }
}
```

#### Command Result

```json
{
  "type": "command.result",
  "id": "msg-004",
  "timestamp": "2025-11-03T01:53:57.580Z",
  "payload": {
    "command_id": "cmd-abc123",
    "status": "completed",
    "result": {
      "success": true
    }
  }
}
```

### Heartbeat/Ping-Pong

Client sends ping every 30 seconds:

```json
{
  "type": "ping",
  "id": "ping-001",
  "timestamp": "2025-11-03T01:53:54.590Z"
}
```

Server responds with pong:

```json
{
  "type": "pong",
  "id": "ping-001",
  "timestamp": "2025-11-03T01:53:54.591Z"
}
```

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid telemetry frame format",
    "details": {
      "field": "timestamp",
      "issue": "Invalid ISO 8601 format"
    },
    "request_id": "req-xyz789",
    "timestamp": "2025-11-03T01:53:54.600Z"
  }
}
```

### Error Codes

- `INVALID_REQUEST` - Malformed request
- `UNAUTHORIZED` - Missing or invalid authentication
- `FORBIDDEN` - Insufficient permissions
- `NOT_FOUND` - Resource not found
- `CONFLICT` - Resource conflict
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `INTERNAL_ERROR` - Server error
- `SERVICE_UNAVAILABLE` - Service temporarily unavailable
- `TIMEOUT` - Request timeout
- `VALIDATION_ERROR` - Request validation failed

### Retry Strategy

For transient errors (5xx, timeout):
1. Retry with exponential backoff
2. Initial delay: 1 second
3. Backoff multiplier: 2
4. Max retries: 3
5. Max delay: 30 seconds

---

## Example Workflows

### Workflow 1: Device Monitoring with Alerts

```mermaid
sequenceDiagram
    participant Device
    participant Nexus
    participant AlertService
    participant User

    Device->>Nexus: POST /telemetry/frames
    Nexus->>Nexus: Check thresholds
    Nexus->>AlertService: Trigger alert
    AlertService->>User: Send notification
    User->>Nexus: POST /commands/execute (restart)
    Nexus->>Device: Execute restart
    Device->>Nexus: POST /telemetry/frames (recovered)
```

### Workflow 2: AI-Powered Data Analysis

```mermaid
sequenceDiagram
    participant Client
    participant Nexus
    participant AIAgent

    Client->>Nexus: POST /ai/tasks (analysis request)
    Nexus->>AIAgent: Assign task
    AIAgent->>Nexus: POST /ai/agents/{id}/heartbeat
    AIAgent->>Nexus: Process and analyze
    AIAgent->>Nexus: Submit result
    Nexus->>Client: Return analysis result
```

### Workflow 3: Multi-Agent Collaboration

```mermaid
sequenceDiagram
    participant Client
    participant Nexus
    participant Agent1
    participant Agent2

    Client->>Nexus: POST /ai/collaborate
    Nexus->>Agent1: Assign step 1
    Agent1->>Nexus: Complete step 1, update context
    Nexus->>Agent2: Assign step 2 with context
    Agent2->>Nexus: Complete step 2
    Nexus->>Client: Return final result
```

### Example: Complete Task Execution Flow

```javascript
// 1. Create a scheduled task
const task = await fetch('https://api.nexus.example.com/v1/tasks', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Daily backup',
    type: 'scheduled',
    schedule: { cron: '0 1 * * *' },
    parameters: { target: 'database-prod' }
  })
});

// 2. Monitor task via WebSocket
const ws = new WebSocket('wss://ws.nexus.example.com/v1?token=YOUR_API_KEY');

ws.send(JSON.stringify({
  type: 'subscribe',
  id: 'sub-001',
  payload: {
    channel: 'tasks',
    filters: { task_id: task.task_id }
  }
}));

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'task.completed') {
    console.log('Task completed:', message.payload);
  }
};

// 3. Manually trigger execution if needed
await fetch(`https://api.nexus.example.com/v1/tasks/${task.task_id}/execute`, {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
});
```

---

## Appendix

### Supported Telemetry Metric Types

- **Numeric**: CPU usage, memory usage, disk usage, latency
- **Boolean**: Service status, feature flags
- **String**: Status messages, version info
- **Array**: Lists of events, errors
- **Object**: Complex nested metrics

### Task Types

- `scheduled` - Recurring tasks with cron schedule
- `one_time` - Single execution tasks
- `event_driven` - Tasks triggered by events
- `dependent` - Tasks with dependencies on other tasks

### Command Categories

- `system` - System-level commands (restart, shutdown)
- `service` - Service management (start, stop, reload)
- `data` - Data operations (backup, restore, sync)
- `diagnostic` - Diagnostic commands (health check, logs)
- `custom` - User-defined commands

### WebSocket Close Codes

- `1000` - Normal closure
- `1001` - Going away
- `1002` - Protocol error
- `1003` - Unsupported data
- `1008` - Policy violation
- `1011` - Internal server error
- `4000` - Authentication failed
- `4001` - Rate limit exceeded
- `4002` - Invalid subscription

---

## Support & Feedback

For API support, documentation updates, or feedback:

- **Email**: api-support@nexus.example.com
- **Documentation**: https://docs.nexus.example.com
- **Status Page**: https://status.nexus.example.com
- **GitHub Issues**: https://github.com/nexus/api/issues

---

**Document Revision History:**

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-03 | Initial draft specification |
