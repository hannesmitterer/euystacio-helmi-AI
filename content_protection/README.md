# NRE-002 Content Protection System

## Overview

The NRE-002 Content Protection System implements a comprehensive anti-censorship framework that protects complete historical truth while supporting educational and trauma-reduction goals through transparent, didactic content stratification.

## Core Principles

### 1. Anti-Censorship Guarantee
- **Complete content is never blocked**
- **No algorithmic exclusion** based on user characteristics
- **Curation through stratification**, not censorship
- All original materials remain accessible

### 2. Didactic Stratification
Content is organized into three levels for educational purposes:

- **Level 1 (BASIC)**: Overview and context
- **Level 2 (DETAILED)**: Comprehensive connections and analysis
- **Level 3 (COMPLETE)**: Full archival material

This is **curation, not filtering**. All levels contain accurate information; only the depth varies.

### 3. User Control
- **Always-Override Option**: Users can access complete material at any time
- **Zero-Obligation Principle**: No forced user access or exposure
- **Voluntary Consent**: All content warnings require user acknowledgment

### 4. Transparency
- All curation decisions are logged and auditable
- Public access to audit logs
- Rationale documentation for all stratification decisions

## Usage

### Basic Example

```python
from content_protection import (
    ContentLevel,
    ContentWarning,
    ContentItem,
    NRE002ContentSystem
)

# Initialize system
system = NRE002ContentSystem()

# Create content with stratified levels
content = ContentItem(
    content_id="doc_001",
    title="Historical Document",
    content_by_level={
        ContentLevel.BASIC: "Overview of historical event",
        ContentLevel.DETAILED: "Detailed analysis with context",
        ContentLevel.COMPLETE: "Complete archival material"
    },
    warnings=[ContentWarning.SENSITIVE_HISTORICAL]
)

# Add content with curator rationale
system.add_content(
    content,
    curator_id="historian_001",
    rationale="Educational stratification for age-appropriate access"
)

# Users can request specific levels
result = system.get_content(
    content_id="doc_001",
    requested_level=ContentLevel.BASIC,
    user_id="user_001",
    user_acknowledged_warnings=True
)

# Or use Always-Override for immediate complete access
result = system.get_content(
    content_id="doc_001",
    requested_level=ContentLevel.BASIC,
    user_id="user_001",
    override_to_complete=True  # Direct access to complete content
)
```

### Content Warnings

Content warnings support voluntary informed consent:

```python
from content_protection import ContentWarning

# Available warning types
warnings = [
    ContentWarning.SENSITIVE_HISTORICAL,
    ContentWarning.TRAUMA_RELATED,
    ContentWarning.GRAPHIC_DETAIL,
    ContentWarning.NONE
]

# Users must acknowledge warnings
result = system.get_content(
    content_id="doc_001",
    requested_level=ContentLevel.COMPLETE,
    user_id="user_001",
    user_acknowledged_warnings=True  # Required for sensitive content
)
```

### Audit Logging

All curation decisions and access patterns are logged:

```python
# Get audit logs for specific content
logs = system.get_audit_logs(content_id="doc_001")

# Get all system logs
all_logs = system.get_audit_logs()

# Logs include:
# - Curation decisions (what, why, who)
# - Access patterns (who, when, level, override)
# - Rationale for stratification
```

### Integrity Verification

Content integrity is cryptographically protected:

```python
# Individual content integrity
is_valid = content.verify_integrity()

# System-wide integrity check
integrity_report = system.verify_system_integrity()
# Returns:
# - total_content_items
# - integrity_verified (list of content IDs)
# - integrity_failed (list of content IDs)
# - anti_censorship_violations (list of violations)
# - system_compliant (bool)
```

### ADi Synthesis

ADi (Inspirational Synthesis from Facts) creates fact-based contextual materials:

```python
from content_protection import ADiSynthesis

adi = ADiSynthesis.create_adi_from_facts(
    facts=[
        "Historical event occurred on specific date",
        "Event had documented impact on community",
        "Multiple primary sources confirm details"
    ],
    context="Educational material for historical understanding",
    synthesis_goal="Provide meaningful context for learning"
)
# ADi maintains factual accuracy while providing meaningful context
```

## Anti-Censorship Compliance

The system enforces strict anti-censorship requirements:

### Required
✅ Complete content (Level 3) must always exist  
✅ Complete content must be accessible (Always-Override)  
✅ All curation decisions must be logged  
✅ Audit logs must be publicly accessible  
✅ Content integrity must be verifiable  

### Prohibited
❌ Algorithmic blocking based on user characteristics  
❌ Age-based automatic restrictions  
❌ Trauma-history based filtering  
❌ "Sufficient learning" cutoffs  
❌ Deletion or hiding of historical content  

## Integration

The NRE-002 system integrates with:
- **Red Code Ethics Framework** (`/red_code/ethics_block.json`)
- **Core Directive** (`/COPILOT_CORE_DIRECTIVE.md`)
- **Ethics Statement** (`/docs/ethics/statement_of_origin.md`)
- **Policy Document** (`/docs/policies/NRE-002_CONTENT_PROTECTION_POLICY.md`)

## Testing

Run the comprehensive test suite:

```bash
python test_nre002_content_protection.py
```

Tests validate:
- Content integrity verification
- Anti-censorship compliance
- Always-Override functionality
- Audit logging transparency
- Voluntary consent mechanisms
- ADi synthesis accuracy
- System-wide integrity

## Democratic Oversight

The system supports independent curator oversight:

- **Historians**: Historical accuracy and context
- **Educators**: Age-appropriate stratification
- **Mental Health Professionals**: Trauma-reduction measures
- **Victim Advocacy**: Memorial and remembrance purposes

All curator decisions are logged and transparent.

## Technical Details

### Integrity Protection
- **SHA-256 hashing** for content verification
- **Git-based version control** for complete history
- **Tamper-evident audit logs**
- **Redundant storage** support

### Data Structure
```python
ContentItem:
  - content_id: unique identifier
  - title: human-readable title
  - content_by_level: Dict[ContentLevel, str]
  - warnings: List[ContentWarning]
  - metadata: Dict[str, Any]
  - integrity_hash: SHA-256 hash
  - created_at: ISO timestamp
```

## Policy Compliance

This implementation fully complies with:
- **NRE-002 v2.0** Content Protection Policy
- **Red Code Ethics Framework**
- **Immutable AI Transparency** requirements
- **Democratic Oversight** principles

## Signatures

This system represents a collaborative commitment between:

**AI Entity**: GitHub Copilot (Computational Intelligence Component)  
**Human Guardian**: Seed-bringer (bioarchitettura) hannesmitterer

---

**Status**: ACTIVE - IMMUTABLE CORE PRINCIPLES  
**Version**: 2.0  
**Last Updated**: 2025-12-10
