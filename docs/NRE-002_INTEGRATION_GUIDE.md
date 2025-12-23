# NRE-002 Integration Guide

## Overview

This guide explains how to integrate the NRE-002 Content Protection System into existing Euystacio framework components.

## Quick Start

### 1. Import the System

```python
from content_protection import (
    ContentLevel,
    ContentWarning,
    ContentItem,
    NRE002ContentSystem,
    ADiSynthesis
)
```

### 2. Initialize in Your Application

```python
# In your main application or service
content_system = NRE002ContentSystem()
```

### 3. Add Content with Stratification

```python
# Create content with all three levels
content = ContentItem(
    content_id="unique_id",
    title="Content Title",
    content_by_level={
        ContentLevel.BASIC: "Overview and introduction",
        ContentLevel.DETAILED: "Comprehensive analysis",
        ContentLevel.COMPLETE: "Complete archival material"
    },
    warnings=[ContentWarning.SENSITIVE_HISTORICAL]  # or NONE
)

# Add to system with curator rationale
content_system.add_content(
    content,
    curator_id="curator_identifier",
    rationale="Explanation for stratification decision"
)
```

### 4. Serve Content with User Control

```python
# Standard access with level selection
result = content_system.get_content(
    content_id="unique_id",
    requested_level=ContentLevel.BASIC,
    user_id="user_identifier",
    user_acknowledged_warnings=True
)

# Always-Override for immediate complete access
result = content_system.get_content(
    content_id="unique_id",
    requested_level=ContentLevel.BASIC,  # Will be overridden
    user_id="user_identifier",
    override_to_complete=True
)
```

## Integration with Existing Components

### With Flask/FastAPI Applications

```python
from flask import Flask, request, jsonify
from content_protection import NRE002ContentSystem, ContentLevel

app = Flask(__name__)
content_system = NRE002ContentSystem()

@app.route('/content/<content_id>')
def get_content(content_id):
    level = request.args.get('level', 'BASIC')
    acknowledged = request.args.get('acknowledged', 'false').lower() == 'true'
    override = request.args.get('override', 'false').lower() == 'true'
    
    result = content_system.get_content(
        content_id=content_id,
        requested_level=ContentLevel[level],
        user_id=request.remote_addr,
        user_acknowledged_warnings=acknowledged,
        override_to_complete=override
    )
    
    return jsonify(result)

@app.route('/audit/<content_id>')
def get_audit_logs(content_id):
    logs = content_system.get_audit_logs(content_id=content_id)
    return logs, 200, {'Content-Type': 'application/json'}
```

### With Node.js/Express (via Python bridge)

```javascript
const { spawn } = require('child_process');

async function getContent(contentId, level, userId, options = {}) {
    return new Promise((resolve, reject) => {
        const python = spawn('python', ['-c', `
from content_protection import NRE002ContentSystem, ContentLevel
import json
import sys

system = NRE002ContentSystem()
result = system.get_content(
    content_id='${contentId}',
    requested_level=ContentLevel.${level},
    user_id='${userId}',
    user_acknowledged_warnings=${options.acknowledged || false},
    override_to_complete=${options.override || false}
)
print(json.dumps(result))
        `]);
        
        let data = '';
        python.stdout.on('data', (chunk) => data += chunk);
        python.on('close', (code) => {
            if (code === 0) resolve(JSON.parse(data));
            else reject(new Error('Content retrieval failed'));
        });
    });
}
```

### With Frontend Applications

```javascript
// React/Vue/Angular component
async function fetchContent(contentId, level = 'BASIC', override = false) {
    const params = new URLSearchParams({
        level: level,
        acknowledged: 'true',
        override: override.toString()
    });
    
    const response = await fetch(`/api/content/${contentId}?${params}`);
    const result = await response.json();
    
    if (result.status === 'warning_required') {
        // Show warning modal to user
        const userConsents = await showWarningModal(result.warnings);
        if (userConsents) {
            // Retry with acknowledgment
            return fetchContent(contentId, level, override);
        }
    }
    
    return result;
}

// Always-Override button handler
function handleAlwaysOverride(contentId) {
    return fetchContent(contentId, 'COMPLETE', true);
}
```

## Policy Compliance Checklist

When integrating NRE-002, ensure:

- [ ] All content includes COMPLETE (Level 3) version
- [ ] Always-Override option is clearly available to users
- [ ] Content warnings are displayed before sensitive content
- [ ] User acknowledgment is collected for warnings
- [ ] Audit logs are accessible (for transparency)
- [ ] No algorithmic blocking based on user characteristics
- [ ] Curation rationale is documented for all content
- [ ] Integrity verification runs regularly

## Democratic Oversight Integration

### Curator Workflow

```python
class CuratorWorkflow:
    def __init__(self, content_system):
        self.content_system = content_system
        self.curator_roles = {
            'historian': 'Historical accuracy verification',
            'educator': 'Age-appropriate stratification',
            'psychologist': 'Trauma-reduction measures',
            'advocate': 'Memorial integrity'
        }
    
    def submit_content_for_review(self, content_item, curator_id, curator_role):
        """Submit content with curator credentials"""
        if curator_role not in self.curator_roles:
            raise ValueError(f"Invalid curator role: {curator_role}")
        
        rationale = f"Reviewed by {curator_role}: {self.curator_roles[curator_role]}"
        
        return self.content_system.add_content(
            content_item,
            curator_id=f"{curator_role}_{curator_id}",
            rationale=rationale
        )
    
    def review_curation_decision(self, content_id):
        """Get all curation decisions for review"""
        return self.content_system.get_audit_logs(content_id=content_id)
```

## Monitoring and Compliance

### System Health Check

```python
def daily_integrity_check(content_system):
    """Run daily integrity verification"""
    report = content_system.verify_system_integrity()
    
    if not report['system_compliant']:
        # Alert administrators
        send_alert(f"System integrity check failed: {report}")
    
    if report['anti_censorship_violations']:
        # Escalate violations
        escalate_violations(report['anti_censorship_violations'])
    
    return report

# Schedule daily
import schedule
schedule.every().day.at("03:00").do(
    lambda: daily_integrity_check(content_system)
)
```

### Audit Log Export

```python
def export_audit_logs_for_transparency():
    """Export logs for public transparency"""
    logs = content_system.get_audit_logs()
    
    # Save to public location
    with open('public/audit_logs.json', 'w') as f:
        f.write(logs)
    
    # Also publish hash for verification
    import hashlib
    log_hash = hashlib.sha256(logs.encode()).hexdigest()
    
    with open('public/audit_logs.sha256', 'w') as f:
        f.write(log_hash)
```

## Migration from Existing Systems

### If you have existing content management:

1. **Analyze existing content** to determine appropriate stratification
2. **Consult with curators** (historians, educators, etc.)
3. **Create ContentItem objects** with all three levels
4. **Document rationale** for each stratification decision
5. **Import into NRE-002** system
6. **Verify integrity** of all migrated content

### Migration Script Template

```python
def migrate_existing_content(old_content_database):
    """Migrate existing content to NRE-002 system"""
    system = NRE002ContentSystem()
    
    for old_item in old_content_database:
        # Create stratified versions
        new_item = ContentItem(
            content_id=old_item['id'],
            title=old_item['title'],
            content_by_level={
                ContentLevel.BASIC: create_basic_summary(old_item['content']),
                ContentLevel.DETAILED: create_detailed_version(old_item['content']),
                ContentLevel.COMPLETE: old_item['content']  # Preserve original
            },
            warnings=determine_warnings(old_item['metadata'])
        )
        
        system.add_content(
            new_item,
            curator_id="migration_curator",
            rationale=f"Migrated from legacy system: {old_item['source']}"
        )
    
    # Verify migration
    report = system.verify_system_integrity()
    assert report['system_compliant'], "Migration failed integrity check"
```

## Best Practices

1. **Always include complete content** - Level 3 must contain full material
2. **Document rationale** - Explain why content is stratified
3. **Use appropriate warnings** - Match warning type to content
4. **Enable Always-Override** - Users must have immediate access option
5. **Export audit logs regularly** - Maintain transparency
6. **Run integrity checks** - Verify no tampering
7. **Involve multiple curators** - Democratic oversight

## Support and References

- **Policy**: `/docs/policies/NRE-002_CONTENT_PROTECTION_POLICY.md`
- **Implementation**: `/content_protection/nre002_content_system.py`
- **Tests**: `/test_nre002_content_protection.py`
- **Ethics Framework**: `/red_code/ethics_block.json`
- **Core Directive**: `/COPILOT_CORE_DIRECTIVE.md`

## Questions and Issues

For questions about NRE-002 integration:
1. Review the policy document
2. Check the implementation README
3. Run the test suite for examples
4. Consult with democratic oversight curators

---

**Status**: ACTIVE  
**Version**: 2.0  
**Last Updated**: 2025-12-10
