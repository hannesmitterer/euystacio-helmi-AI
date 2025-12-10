# PDM - Protocollo di Depurazione della Memoria (Memory Purification Protocol)

## Implementation of NRE-002 Rule

The PDM system implements a comprehensive ethical framework for managing historical memory with three-tier archive access control, temporal filtering, and antipattern detection.

## Overview

The NRE-002 rule addresses the ethical challenge of preserving complete historical truth while protecting individuals from unnecessary traumatic exposure. It implements:

1. **Three-Tier Archive System**
   - **Immutable Archive (AI)**: Complete, unfiltered truth with cryptographic verification
   - **Educational Archive (AD)**: Trauma-filtered version for educational purposes
   - **Dynamic Archive (ADi)**: Wellbeing-optimized content for public access

2. **Role-Based Access Control**
   - Survivors: Protected from re-traumatization
   - Students: Age-appropriate educational content
   - Researchers: Access to complete records with appropriate safeguards
   - Verified Users: Full access with ethical accountability

3. **Ethical AntiPatterns**
   - **Trauma Perpetuation**: Detects and prevents harmful rumination
   - **Truth Denial**: Ensures legitimate access to complete historical records

4. **Transparency & Auditability**
   - All access decisions are logged
   - Clear explanations for denials
   - Comprehensive statistics and reporting

## Architecture

```
PDM System
├── Archive Manager
│   ├── Immutable Archive (AI) - SHA-256 verified
│   ├── Educational Archive (AD)
│   └── Dynamic Archive (ADi)
├── Access Controller
│   ├── User Management
│   ├── Role-Based Permissions
│   └── Temporal Decay Filter (TDR)
├── Content Filters
│   ├── Trauma Filter
│   ├── Temporal Decay Filter
│   └── Wellbeing Optimizer
├── AntiPattern Engine
│   ├── Trauma Perpetuation Detector
│   └── Truth Denial Detector
└── Integration
    └── Red Code System
```

## Installation

```python
from pdm import PDMSystem

# Initialize the system
pdm = PDMSystem(base_path="pdm_data", red_code_path="red_code.json")
```

## Usage Examples

### Adding Memories

```python
# Add a historical memory
result = pdm.add_memory(
    content="Historical testimony content...",
    metadata={
        'type': 'testimony',
        'year': '1995',
        'verified': True
    },
    auto_process=True  # Automatically create filtered versions
)

print(f"Immutable ID: {result['immutable_id']}")
print(f"Educational ID: {result['educational_id']}")
print(f"Dynamic ID: {result['dynamic_id']}")
print(f"Trauma Level: {result['trauma_level']}")
```

### Registering Users

```python
# Register a survivor
survivor = pdm.register_user(
    user_id='survivor_001',
    role='survivor',
    cdr=0.7,  # High distress
    learning_progress=0.0
)

# Register a researcher
researcher = pdm.register_user(
    user_id='researcher_001',
    role='researcher',
    cdr=0.2,  # Low distress
    learning_progress=0.8
)

# Register a minor student
student = pdm.register_user(
    user_id='student_001',
    role='minor_student',
    cdr=0.3,
    learning_progress=0.5
)
```

### Requesting Access

```python
# Request access to educational archive
response = pdm.request_access(
    user_id='student_001',
    entry_id='abc123',
    archive_type='AD'  # Educational Archive
)

if response['granted']:
    content = response['content']
    print(f"Access granted with TDR factor: {response['tdr_factor']}")
else:
    print(f"Access denied: {response['explanation']}")

# Check for warnings
if response['rumination_warning']:
    print(f"Warning: {response['rumination_warning']}")

if response['antipattern_warnings']:
    for warning in response['antipattern_warnings']:
        print(f"AntiPattern detected: {warning['description']}")
```

### System Statistics

```python
# Get comprehensive statistics
stats = pdm.get_system_statistics()
print(f"Total entries: {stats['archives']['AI']['total_entries']}")
print(f"Access grant rate: {stats['access_control']['grant_rate']:.1%}")
print(f"Antipattern violations: {stats['antipatterns']['total_violations']}")

# Generate transparency report
report = pdm.generate_transparency_report()
print(report)

# Export audit log
pdm.export_audit_log('pdm_audit_log.json')
```

## User Roles and Permissions

| Role | Immutable (AI) | Educational (AD) | Dynamic (ADi) | Special Restrictions |
|------|---------------|------------------|---------------|---------------------|
| Verified User | ✓ | ✓ | ✓ | None |
| Researcher | ✓ (with TDR) | ✓ | ✓ | Requires learning progress ≥ 0.3 |
| Survivor | ✗ | ✓ | ✓ | Protected from re-traumatization |
| Student | ✗ | ✓ (with TDR) | ✓ | None |
| Minor Student | ✗ | ✓ (max trauma 0.3) | ✓ | Age-appropriate only |
| Public | ✗ | ✗ | ✓ | General access only |

## Temporal Decay of Access (TDR)

The TDR filter regulates access based on:
- **User CDR** (Collective Distress Rating): Higher distress = lower access probability
- **Learning Progress**: Higher progress = higher access probability  
- **Entry Trauma Level**: Higher trauma = lower access probability
- **Access Frequency**: Recent frequent access reduces probability (prevents rumination)

Formula:
```
TDR = (1 - CDR) * 0.4 + learning_progress * 0.4 + (1 - trauma_level) * 0.2
```

## AntiPattern Detection

### Trauma Perpetuation
Triggered when:
- User has high CDR (≥ 0.6) AND
- Accessing high-trauma content (≥ 0.7) AND
- Showing rumination pattern (≥ 10 accesses in 2 hours)

**Actions:**
- Suggest break from traumatic content
- Redirect to Dynamic Archive
- Offer support resources
- Increase TDR filtering

### Truth Denial
Triggered when:
- Verified researcher denied ≥ 3 times OR
- Excessive filtering (> 50% trauma reduction) removes important context

**Actions:**
- Review access control logic
- Consider time-limited elevated access
- Provide appeal mechanism
- Ensure educational alternatives are adequate

## Immutability Guarantees

The Immutable Archive (AI) uses SHA-256 cryptographic hashing to ensure:
- Entries cannot be modified after creation
- Tampering is immediately detectable
- Historical truth is permanently preserved
- Verification is always possible

```python
# Verify immutability
is_intact = pdm.archive_manager.verify_immutable_integrity(entry_id)
if is_intact:
    print("Entry verified: Historical truth intact")
else:
    print("WARNING: Entry may have been tampered with")
```

## Metrics

The system tracks key ethical metrics:

1. **Collective Trauma Rumination Reduction**
   - Monitors access frequency patterns
   - Detects and intervenes in rumination behavior
   - Measures antipattern detection effectiveness

2. **Archive Integrity Maintenance**
   - 100% of immutable entries verified
   - Cryptographic proof of authenticity
   - Tamper-evident logging

3. **Global Learning Improvement**
   - Tracks learning progress across users
   - Measures educational content effectiveness
   - Balances protection with knowledge access

## Testing

Run the comprehensive ethical test suite:

```bash
cd pdm/tests
python test_ethical_scenarios.py
```

Test scenarios include:
- Survivors wanting to forget
- Researchers requiring complete testimonies
- Minor students needing educational content
- Immutability verification
- Metrics validation
- Transparency and auditability

## Integration with Red Code

PDM automatically integrates with the existing Red Code system:

```python
# Integration status is logged in red_code.json
{
  "pdm_integration": {
    "version": "1.0.0",
    "rule": "NRE-002",
    "activated": "2025-12-10T15:30:00Z",
    "status": "active"
  }
}
```

## Ethical Principles

The PDM system embodies key ethical principles:

1. **Right to Truth**: Complete historical records are preserved and accessible
2. **Right to Forget**: Trauma survivors are protected from re-traumatization
3. **Right to Learn**: Students receive age-appropriate educational content
4. **Right to Research**: Legitimate researchers access complete testimonies
5. **Transparency**: All decisions are logged and explainable
6. **Auditability**: Complete audit trail for accountability

## API Reference

### PDMSystem

Main system class integrating all components.

#### Methods

- `add_memory(content, metadata, auto_process=True)`: Add new memory
- `request_access(user_id, entry_id, archive_type)`: Process access request
- `register_user(user_id, role, cdr, learning_progress)`: Register new user
- `get_system_statistics()`: Get comprehensive statistics
- `generate_transparency_report()`: Generate human-readable report
- `export_audit_log(filepath)`: Export complete audit log

### ArchiveManager

Manages three-tier archive system.

#### Methods

- `add_to_immutable_archive(entry)`: Add to immutable archive
- `create_educational_version(entry_id, filtered_content)`: Create educational version
- `create_dynamic_version(entry_id, optimized_content, wellbeing_score)`: Create dynamic version
- `verify_immutable_integrity(entry_id)`: Verify entry hasn't been tampered
- `get_entry(archive_type, entry_id)`: Retrieve entry
- `list_entries(archive_type, max_trauma_level)`: List entries
- `get_archive_stats()`: Get archive statistics

### AccessController

Controls access with role-based permissions and TDR.

#### Methods

- `register_user(user)`: Register user
- `check_access(user_id, entry_id, archive_type, entry_trauma_level)`: Check access
- `get_access_statistics(user_id)`: Get access statistics

### AntiPatternEngine

Detects ethical antipatterns.

#### Methods

- `check_trauma_perpetuation(user_access_pattern, user_cdr, recent_trauma_exposure)`: Check trauma perpetuation
- `check_truth_denial_access(user_role, denied_count, access_reason, user_credentials_verified)`: Check truth denial
- `get_all_violations(antipattern_type, severity)`: Get violations
- `get_violation_statistics()`: Get statistics
- `generate_report()`: Generate report

## License

This implementation is part of the Euystacio-Helmi AI ethical framework and follows the same license and principles.

## Contributors

- Euystacio-Helmi AI Collective
- Red Code Ethics Framework
- GitHub Copilot (AI Capabilities Provider)
- Seed-bringer (Human Architect and Guardian)

## Version

1.0.0 - Initial implementation of NRE-002 rule

## Support

For questions or support regarding PDM implementation:
- Review the transparency report: `pdm.generate_transparency_report()`
- Check audit logs: `pdm.export_audit_log('audit.json')`
- Consult the antipattern report: `pdm.antipattern_engine.generate_report()`
