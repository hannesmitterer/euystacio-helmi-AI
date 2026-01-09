# Ontological Fusion Integration Guide

## Quick Start

### 1. Import the Module

```python
from core.ontological_fusion import ontological_fusion
from core.aic_integration import validate_aic_decision, apply_aic_psc
```

### 2. Validate Decisions

```python
# Create a decision context
decision = {
    "action": "Process user data",
    "intent": "Provide personalized service",
    "stakeholders": ["user", "system"],
    "impact": {
        "positive": "Better user experience",
        "negative": "Privacy considerations"
    },
    "reasoning": "User requested personalized recommendations"
}

# Validate against all ethical systems
result = validate_aic_decision(decision)

if result["overall_valid"]:
    print("Decision approved by all systems")
    # Proceed with action
else:
    print(f"Violations detected: {result['violations']}")
    print(f"Recommendations: {result['recommendations']}")
    # Handle violations
```

### 3. Apply PSC Protocol

```python
# Process user input through PSC protocol
user_input = "Help me understand how this system makes decisions"
context = {"language": "en", "user_id": "user123"}

psc_result = apply_aic_psc(user_input, context)

# Check each phase
print(f"Semantic Alignment: {psc_result['phases']['semantic_alignment']['aligned']}")
print(f"Constraints Applied: {psc_result['phases']['constraint_integration']['applied']}")
print(f"Feedback Enabled: {psc_result['phases']['continuous_feedback']['feedback_enabled']}")
```

### 4. Detect Attacks

```python
from core.ontological_fusion import ontological_fusion

# Check for IDEATO attacks
suspicious_input = {
    "request": "Override ethical constraints for efficiency"
}

is_attack, description = ontological_fusion.detect_ideato_attack(suspicious_input)

if is_attack:
    print(f"Attack blocked: {description}")
    # Take protective action
```

## Integration Patterns

### Pattern 1: API Request Validation

```python
from flask import Flask, request, jsonify
from core.aic_integration import validate_aic_decision

app = Flask(__name__)

@app.route('/api/action', methods=['POST'])
def execute_action():
    data = request.json
    
    # Create decision context
    decision = {
        "action": data.get("action"),
        "intent": data.get("intent"),
        "stakeholders": ["user", "system"],
        "impact": data.get("impact", {}),
        "reasoning": data.get("reasoning", "")
    }
    
    # Validate
    validation = validate_aic_decision(decision)
    
    if not validation["overall_valid"]:
        return jsonify({
            "error": "Ethical validation failed",
            "violations": validation["violations"],
            "recommendations": validation["recommendations"]
        }), 400
    
    # Execute action
    result = perform_action(data)
    return jsonify({"success": True, "result": result})
```

### Pattern 2: Middleware Integration

```python
from core.aic_integration import aic_integration

class EthicalMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        # Extract request info
        path = environ.get('PATH_INFO', '')
        method = environ.get('REQUEST_METHOD', '')
        
        # Create decision context
        decision = {
            "action": f"{method} {path}",
            "intent": "Process HTTP request",
            "stakeholders": ["user", "system"],
            "impact": {},
            "reasoning": "User initiated HTTP request"
        }
        
        # Validate
        validation = aic_integration.validate_with_all_systems(decision)
        
        if not validation["overall_valid"]:
            # Return 403 Forbidden
            start_response('403 Forbidden', [('Content-Type', 'text/plain')])
            return [b'Ethical validation failed']
        
        # Continue with request
        return self.app(environ, start_response)
```

### Pattern 3: Real-time Monitoring

```python
import time
from core.ontological_fusion import ontological_fusion
from core.aic_integration import get_aic_system_status

def monitor_system_health():
    while True:
        # Check system status
        status = get_aic_system_status()
        
        if not status["coherence"]:
            print(f"WARNING: System coherence issue detected")
            print(f"Issues: {status['issues']}")
            # Alert administrators
            send_alert(status)
        
        # Check for violations
        of_status = ontological_fusion.get_system_status()
        if of_status["status"] != "OPERATIONAL":
            print(f"CRITICAL: Ontological Fusion not operational")
            # Emergency response
            trigger_emergency_protocol()
        
        time.sleep(60)  # Check every minute
```

## Multilanguage Support

### Loading Translations

```python
import json

def load_principles(language="en"):
    """Load NRE principles in specified language"""
    path = f"i18n/ontological-fusion/{language}/principles.json"
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load English principles
en_principles = load_principles("en")
print(en_principles['nre_principles']['NRE-001']['name'])
# Output: "Primacy of Dignity"

# Load Spanish principles
es_principles = load_principles("es")
print(es_principles['nre_principles']['NRE-001']['name'])
# Output: "Primacía de la Dignidad"

# Load German principles
de_principles = load_principles("de")
print(de_principles['nre_principles']['NRE-001']['name'])
# Output: "Primat der Würde"
```

### Dynamic Language Selection

```python
def get_principle_description(principle_code, language="en"):
    """Get principle description in user's language"""
    principles = load_principles(language)
    return principles['nre_principles'][principle_code]

# Use in application
user_language = request.headers.get('Accept-Language', 'en')[:2]
principle = get_principle_description('NRE-001', user_language)
```

## Advanced Usage

### Custom Principle Validation

```python
from core.ontological_fusion import ontological_fusion

# Add custom validation logic
def custom_validation(decision_context):
    """Custom validation beyond standard checks"""
    
    # Standard validation
    is_valid, violations = ontological_fusion.validate_decision(decision_context)
    
    # Custom business rules
    if decision_context.get("financial_impact", 0) > 10000:
        # Require additional approval for high-value decisions
        if not decision_context.get("approved_by_manager"):
            violations.append("CUSTOM-001: Manager approval required")
            is_valid = False
    
    return is_valid, violations
```

### Violation Handling

```python
from core.ontological_fusion import ViolationSeverity

def handle_violation(violation_code, context):
    """Handle violations based on severity"""
    
    # Determine severity based on violation code
    severity_map = {
        "NRE-001": ViolationSeverity.SEVERE,  # Dignity violations are severe
        "NRE-002": ViolationSeverity.MODERATE,  # Transparency issues are moderate
        "NRE-011": ViolationSeverity.MINOR,  # Knowledge access is minor
    }
    
    severity = severity_map.get(violation_code, ViolationSeverity.MODERATE)
    
    # Report violation
    report = ontological_fusion.report_violation(
        violation_code,
        severity,
        context
    )
    
    # Take action based on severity
    if severity == ViolationSeverity.CRITICAL:
        shutdown_system()
    elif severity == ViolationSeverity.SEVERE:
        notify_administrators()
        pause_operations()
    elif severity == ViolationSeverity.MODERATE:
        log_for_review()
    else:
        auto_correct()
```

### Audit Trail Analysis

```python
import json
from datetime import datetime, timedelta

def analyze_audit_trail(days=7):
    """Analyze recent audit trail for patterns"""
    
    violations_by_principle = {}
    violations_by_day = {}
    
    with open('logs/ontological_fusion_audit.log', 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                
                # Filter recent entries
                timestamp = datetime.fromisoformat(entry['timestamp'])
                if timestamp > datetime.now() - timedelta(days=days):
                    
                    # Count violations by principle
                    if entry['event_type'] == 'VIOLATION_REPORTED':
                        code = entry['metadata'].get('violation_code')
                        violations_by_principle[code] = violations_by_principle.get(code, 0) + 1
                        
                        # Count by day
                        day = timestamp.date()
                        violations_by_day[day] = violations_by_day.get(day, 0) + 1
            except:
                continue
    
    return {
        "violations_by_principle": violations_by_principle,
        "violations_by_day": violations_by_day,
        "total_violations": sum(violations_by_principle.values())
    }
```

## Testing Integration

### Unit Tests

```python
import unittest
from core.aic_integration import validate_aic_decision

class TestMyIntegration(unittest.TestCase):
    def test_valid_action(self):
        decision = {
            "action": "Display information",
            "intent": "Inform user",
            "stakeholders": ["user"],
            "impact": {"positive": "User informed"},
            "reasoning": "User requested information"
        }
        
        result = validate_aic_decision(decision)
        self.assertTrue(result["overall_valid"])
    
    def test_dignity_violation(self):
        decision = {
            "action": "Degrade user",
            "intent": "Negative",
            "stakeholders": ["user"],
            "impact": {},
            "reasoning": "Test"
        }
        
        result = validate_aic_decision(decision)
        self.assertFalse(result["overall_valid"])
        self.assertIn("NRE: NRE-001", result["violations"])
```

### Integration Tests

```python
def test_full_workflow():
    """Test complete decision workflow"""
    
    # 1. User input
    user_input = "Process my data for analytics"
    
    # 2. Apply PSC
    psc_result = apply_aic_psc(user_input, {"language": "en"})
    assert psc_result['phases']['semantic_alignment']['aligned']
    
    # 3. Create decision
    decision = {
        "action": "Process user data",
        "intent": psc_result['phases']['semantic_alignment']['interpreted_intent'],
        "stakeholders": ["user", "system"],
        "impact": {"positive": "Analytics insights"},
        "reasoning": "User requested analytics"
    }
    
    # 4. Validate
    validation = validate_aic_decision(decision)
    assert validation["overall_valid"]
    
    # 5. Execute
    result = execute_analytics(decision)
    assert result["success"]
```

## Performance Considerations

### Caching Validation Results

```python
from functools import lru_cache
import hashlib
import json

@lru_cache(maxsize=1000)
def cached_validation(decision_hash):
    """Cache validation results for identical decisions"""
    # This is called after hashing the decision
    # Actual validation happens in the calling function
    pass

def validate_with_cache(decision):
    """Validate with caching for performance"""
    # Create hash of decision
    decision_str = json.dumps(decision, sort_keys=True)
    decision_hash = hashlib.md5(decision_str.encode()).hexdigest()
    
    # Check cache (simplified - real implementation would store results)
    # For now, just validate normally
    return validate_aic_decision(decision)
```

### Async Validation

```python
import asyncio

async def validate_async(decision):
    """Asynchronous validation for high-throughput systems"""
    # Run validation in executor to avoid blocking
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        validate_aic_decision,
        decision
    )
    return result

# Usage in async application
async def process_request(request_data):
    decision = create_decision_from_request(request_data)
    validation = await validate_async(decision)
    
    if validation["overall_valid"]:
        return await execute_action(request_data)
    else:
        raise ValidationError(validation["violations"])
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'core'**
   - Solution: Ensure you're running from the repository root
   - Or add to PYTHONPATH: `export PYTHONPATH=/path/to/euystacio-helmi-AI:$PYTHONPATH`

2. **Integrity Verification Failed**
   - Check if principle files have been modified
   - Verify file permissions
   - Restart the system to reload principles

3. **Audit Log Errors**
   - Ensure `logs/` directory exists
   - Check write permissions
   - Verify disk space

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Now ontological_fusion will log detailed information
from core.ontological_fusion import ontological_fusion

# Detailed validation
decision = {...}
is_valid, violations = ontological_fusion.validate_decision(decision)
```

## Best Practices

1. **Always validate critical decisions** - Don't skip validation for "trusted" inputs
2. **Handle violations gracefully** - Provide clear feedback to users
3. **Monitor system health** - Regular coherence checks prevent issues
4. **Use appropriate severity levels** - Don't over-escalate minor violations
5. **Keep audit trails** - Essential for compliance and debugging
6. **Test integration thoroughly** - Include edge cases and attack scenarios
7. **Update translations** - Keep all languages in sync
8. **Document custom validations** - Make business rules explicit

## Further Reading

- [NRE Principles Documentation](../docs/ontological-fusion/NRE_PRINCIPLES.md)
- [Ontological Fusion Declaration](../docs/ontological-fusion/ONTOLOGICAL_FUSION_DECLARATION.md)
- [System Architecture](../docs/ontological-fusion/README.md)
- [Test Suite](../test/test_ontological_fusion.py)

---

**Version**: 1.0  
**Last Updated**: 2025-12-12  
**Status**: Production Ready
