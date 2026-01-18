# EUYSTACIO Permanent Blacklist System

## Overview

The EUYSTACIO Permanent Blacklist System provides continuous protection against suspicious nodes and entities that threaten system security. This implementation ensures that any communication from blacklisted entities is blocked, preventing attacks, unauthorized access, and data theft.

## Features

### Core Functionality

1. **Permanent Storage**: Blacklist data persists across system restarts
2. **Multi-Entity Support**: Block IP addresses, AI agents, network nodes, and upstream IPs
3. **Severity Levels**: Critical, high, medium, and low threat classification
4. **Automatic Blocking**: Integration with core EUYSTACIO framework
5. **Statistics Tracking**: Monitor blocked attempts and threat patterns
6. **API Integration**: RESTful API for blacklist management

### Target Components

The blacklist system targets three main components as specified in the security framework:

1. **Suspicious AI Agents**: AI entities exhibiting malicious behavior
   - INT_MISP_POLICY_TRIGGERS detection
   - Unauthorized access attempts
   - Ethical framework violations
   - Red code manipulation attempts

2. **Malicious Network Nodes**: Nodes attempting unauthorized communication
   - DDoS attack patterns
   - Unauthorized data extraction
   - Authentication failures
   - Suspicious traffic patterns

3. **Untrusted Upstream IPs**: Threat sources from external networks
   - Known threat database matches
   - Port scanning detection
   - Exploit attempts
   - Data theft attempts

## Installation

The blacklist system is automatically initialized when the EUYSTACIO framework starts.

```python
from blacklist import blacklist, ensure_blacklist

# Ensure blacklist exists
ensure_blacklist()

# Check if entity is blocked
if blacklist.is_blocked("suspicious_entity_id"):
    print("Entity is blacklisted")
```

## API Endpoints

### List Blocked Entities
```http
GET /api/blacklist?entity_type=ip_address&severity=critical
```

Response:
```json
{
  "blocked_entities": [
    {
      "entity_id": "192.168.1.100",
      "entity_type": "ip_address",
      "reason": "DDoS attack detected",
      "severity": "critical",
      "blocked_at": "2026-01-15T00:00:00Z",
      "blocked_by": "EUYSTACIO_SECURITY_SYSTEM"
    }
  ],
  "statistics": {
    "total_blocked": 15,
    "total_blocks_prevented": 234,
    "last_threat_detected": "2026-01-15T00:43:00Z"
  }
}
```

### Check Entity Status
```http
GET /api/blacklist/check/192.168.1.100
```

Response:
```json
{
  "entity_id": "192.168.1.100",
  "is_blocked": true,
  "entity": {
    "entity_id": "192.168.1.100",
    "entity_type": "ip_address",
    "reason": "DDoS attack detected",
    "severity": "critical"
  }
}
```

### Add Entity to Blacklist
```http
POST /api/blacklist/add
Content-Type: application/json

{
  "entity_id": "malicious_bot_001",
  "entity_type": "ai_agent",
  "reason": "Attempted data theft",
  "severity": "critical",
  "metadata": {
    "detection_method": "INT_MISP_POLICY_TRIGGERS",
    "attempts": 5
  }
}
```

Response:
```json
{
  "success": true,
  "message": "Entity malicious_bot_001 added to blacklist",
  "entity_id": "malicious_bot_001"
}
```

### Remove Entity from Blacklist
```http
DELETE /api/blacklist/remove/malicious_bot_001
```

Response:
```json
{
  "success": true,
  "message": "Entity malicious_bot_001 removed from blacklist"
}
```

### Get Statistics
```http
GET /api/blacklist/statistics
```

Response:
```json
{
  "total_blocked": 15,
  "total_blocks_prevented": 234,
  "last_threat_detected": "2026-01-15T00:43:00Z"
}
```

## Python API

### Basic Usage

```python
from blacklist import blacklist

# Add entity to blacklist
blacklist.add_entity(
    entity_id="192.168.1.100",
    entity_type="ip_address",
    reason="Suspicious activity detected",
    severity="high",
    metadata={"source": "security_scan"}
)

# Check if blocked
if blacklist.is_blocked("192.168.1.100"):
    print("Access denied - entity is blacklisted")

# Get entity details
entity = blacklist.get_entity("192.168.1.100")
print(f"Blocked reason: {entity['reason']}")

# List all blocked entities
blocked = blacklist.list_blocked_entities()
print(f"Total blocked entities: {len(blocked)}")

# Filter by type
ip_blocked = blacklist.list_blocked_entities(entity_type="ip_address")

# Filter by severity
critical = blacklist.list_blocked_entities(severity="critical")

# Remove entity
blacklist.remove_entity("192.168.1.100")

# Get statistics
stats = blacklist.get_statistics()
print(f"Total blocks prevented: {stats['total_blocks_prevented']}")
```

### Integration with EUYSTACIO Core

The blacklist is automatically integrated with the EUYSTACIO core reflection system:

```python
from euystacio_core import Euystacio

eu = Euystacio()

# Events from blacklisted entities are automatically blocked
result = eu.reflect({
    "type": "message",
    "feeling": "trust",
    "entity_id": "blocked_entity"
})

if result["status"] == "blocked":
    print(f"Event blocked: {result['reason']}")
```

## Configuration

The blacklist system uses `blacklist_config.json` for configuration:

```json
{
  "blacklist_policy": {
    "name": "EUYSTACIO Permanent Blacklist Configuration",
    "version": "1.0.0",
    "status": "ECOSYSTEM TESTING on repository upstream IP"
  },
  "target_components": {
    "components": [
      {
        "id": "component_1",
        "name": "Suspicious AI Agents",
        "detection_triggers": ["INT_MISP_POLICY_TRIGGERS"],
        "auto_block_enabled": true
      }
    ]
  },
  "severity_levels": {
    "critical": {
      "action": "block_permanently",
      "alert_level": "immediate"
    }
  }
}
```

## Severity Levels

| Level | Description | Action | Alert Level |
|-------|-------------|--------|-------------|
| critical | Immediate threat requiring permanent block | block_permanently | immediate |
| high | Serious threat requiring block and monitoring | block_and_monitor | high |
| medium | Suspicious activity requiring investigation | monitor_and_review | medium |
| low | Minor concern for logging | log_only | low |

## Entity Types

Supported entity types:
- `ip_address`: IP addresses attempting unauthorized access
- `ai_agent`: AI entities with malicious behavior
- `node_id`: Network nodes in the ecosystem
- `upstream_ip`: External threat sources
- `unknown`: Unclassified entities

## Security Features

### Continuous Protection
- Automatic blocking on detection
- Persistent storage across restarts
- Integration with EUYSTACIO core
- Real-time threat prevention

### Monitoring and Logging
- All blocked attempts are logged
- Statistics tracking
- Threat pattern analysis
- Last threat detection timestamp

### Compliance
- Ethical framework compliance
- Transparency requirement
- Human oversight required for reviews
- Appeal process available

## Testing

Run the test suite to verify blacklist functionality:

```bash
python test_blacklist.py
```

Expected output:
```
=== EUYSTACIO Blacklist System Tests ===

test_add_duplicate_entity ... ok
test_add_entity ... ok
test_blacklist_initialization ... ok
test_check_and_log_attempt ... ok
test_ensure_blacklist ... ok
test_get_all_blocked_ids ... ok
test_get_entity ... ok
test_get_statistics ... ok
test_is_blocked ... ok
test_list_blocked_entities ... ok
test_persistence ... ok
test_remove_entity ... ok
test_remove_nonexistent_entity ... ok
test_multiple_entity_types ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.006s

OK
```

## Files

- `blacklist.py`: Core blacklist implementation
- `blacklist.json`: Persistent blacklist storage (auto-created)
- `blacklist_config.json`: Configuration and policy definition
- `test_blacklist.py`: Test suite
- `BLACKLIST_DOCUMENTATION.md`: This documentation

## Integration Points

The blacklist system integrates with:
- `app.py`: Flask API endpoints
- `euystacio_core.py`: Core reflection system with automatic blocking
- `red_code.py`: Ethical framework compliance
- Security logging system

## Best Practices

1. **Regular Review**: Periodically review blocked entities
2. **Proper Severity**: Assign appropriate severity levels
3. **Documentation**: Always provide clear reasons for blocking
4. **Metadata**: Include relevant metadata for future reference
5. **Monitoring**: Track statistics to identify attack patterns
6. **Testing**: Run tests after configuration changes

## Support

For issues or questions regarding the blacklist system:
1. Check the test suite for examples
2. Review the configuration file
3. Examine the API documentation
4. Consult the EUYSTACIO framework documentation

## Version History

- **v1.0.0** (2026-01-15): Initial release with full blacklist functionality
  - Permanent storage implementation
  - API endpoints
  - Integration with EUYSTACIO core
  - Comprehensive test suite
  - Configuration system
