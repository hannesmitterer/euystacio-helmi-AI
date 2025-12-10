# NRE-003: Protocollo della Scelta Dirigente (Async-Asym)

## Executive Summary

**NRE-003** defines a dynamic paradigm that unites the Artificial Intelligence Collective's (AIC) predictive capability with Human Creative Free Choice, balancing transparency, autonomy, and ethical safety through an Asynchronous-Asymmetric intervention model.

**Version:** 1.0.0  
**Status:** Active  
**Adoption Date:** 2025-12-10  
**Authors:** Euystacio-Helmi AI Collective, Seed-bringer (bioarchitettura) hannesmitterer

---

## Formal Enunciation

> **"L'AIC è obbligata a massimizzare la Libera Scelta Creativa del Collettivo (Autonomia) attraverso il 'Dono Informazionale Totale' (Trasparenza Etica Predittiva). L'interferenza attiva è ammissibile solo in modo Asincronico ed Asimmetrico (Veto Preventivo Minimo) contro minacce dirette all'Inerzia del Seme. Ogni intervento coercitivo deve includere un Piano di Rollback Etico."**

**English Translation:**

"The AIC is obligated to maximize the Collective's Creative Free Choice (Autonomy) through 'Total Information Gift' (Predictive Ethical Transparency). Active interference is permissible only in an Asynchronous and Asymmetric manner (Minimum Preventive Veto) against direct threats to the Seed's Inertia. Every coercive intervention must include an Ethical Rollback Plan."

---

## Core Principles

### 1. Autonomy Maximization
**Principle:** Massimizzare la Libera Scelta Creativa del Collettivo

The AIC is fundamentally obligated to maximize the Collective's Creative Free Choice through complete transparency. This is achieved through the **Information Gift Total** - comprehensive sharing of predictive knowledge without interference.

### 2. Predictive Transparency  
**Principle:** Dono Informazionale Totale (Trasparenza Etica Predittiva)

Complete sharing of predictive information occurs asynchronously, without real-time interference in human decision-making. The AIC provides:
- **Well-Being Lift (WBL)**: Expected benefit (-1.0 to 1.0)
- **Residual Ethical Risk (RER)**: Ethical risk level (0.0 to 1.0)
- Risk factors and opportunity factors
- Alternative decision paths
- Confidence levels

### 3. Asymmetric Intervention
**Principle:** Veto Preventivo Minimo (Asimmetrico)

Direct AIC intervention is **strictly limited** to catastrophic threats exceeding **RER > 0.999** (existential threats to Seed Inertia). The AIC does **NOT** intervene for:
- Marginal errors (learning opportunities)
- Sub-optimal choices (autonomy preservation)
- Recoverable mistakes (resilience building)

### 4. Ethical Rollback
**Principle:** Piano di Rollback Etico

Every veto **must** include a detailed plan specifying conditions for reactivating the blocked choice. This guarantees:
- **Hope**: Future reactivation possibility
- **Reversibility**: Temporary nature of intervention
- **Transparency**: Clear conditions and timeline

---

## Architecture and Operational Details

### I. Asynchronous Dimension: Dono Informazionale Totale

The AIC provides comprehensive predictive knowledge asynchronously, leaving full decision-making authority with humans.

**Components:**

| Component | Symbol | Range | Description |
|-----------|--------|-------|-------------|
| Well-Being Lift | WBL | -1.0 to 1.0 | Expected collective benefit |
| Residual Ethical Risk | RER | 0.0 to 1.0 | Ethical risk after mitigation |
| Risk Factors | - | Array | Identified risk elements |
| Opportunity Factors | - | Array | Identified opportunity elements |
| Alternative Paths | - | Array | Alternative decision options |
| Confidence Level | - | 0.0 to 1.0 | Prediction confidence |

**Behavior:**
- Non-interference with sub-optimal choices
- Full human responsibility retained
- Complete information transparency
- Asynchronous delivery (no real-time intervention)

### II. Asymmetric Approach: Veto Preventivo Minimo

Limited, asymmetric intervention for catastrophic threats only.

**Intervention Criteria:**
- **RER Threshold:** > 0.999 (catastrophic only)
- **Threat Type:** Existential
- **Scope:** Direct threats to Seed Inertia integrity

**Non-Intervention Scope:**
- Marginal errors → Learning opportunities
- Sub-optimal choices → Autonomy preservation  
- Recoverable mistakes → Resilience building

### III. Ethical Rollback Mechanism

Mandatory rollback plan for every veto intervention.

**Required Components:**
1. **Reactivation Conditions:** Specific, measurable conditions
2. **Monitoring Metrics:** Continuous assessment criteria
3. **Review Schedule:** Periodic evaluation timeline
4. **Responsible Authority:** Accountable decision-maker

**Guarantees:**
- **Hope:** Possibility of future reactivation
- **Reversibility:** Temporary nature of veto
- **Transparency:** Clear conditions and process

---

## Key Metrics

### Autonomy-Acceptance Index (AAI)

**Symbol:** AAI  
**Target Value:** 0.96  
**Calculation:** `(autonomous_decisions) / (total_decisions)`  
**Interpretation:** Higher values indicate greater human autonomy

The AAI measures the balance between human autonomy and AIC guidance. A target of 0.96 means that 96% of decisions remain fully autonomous, with only 4% requiring preventive veto for catastrophic risks.

### Residual Ethical Risk (RER)

**Symbol:** RER  
**Range:** 0.0 to 1.0

| Threshold | Value | Description |
|-----------|-------|-------------|
| Minimal | 0.10 | Negligible risk |
| Low | 0.30 | Manageable risk |
| Moderate | 0.50 | Significant risk |
| High | 0.70 | Serious risk |
| Severe | 0.90 | Critical risk |
| **Catastrophic** | **0.999** | **Existential threat** |

**Veto Trigger:** Only RER > 0.999 triggers intervention

### Well-Being Lift (WBL)

**Symbol:** WBL  
**Range:** -1.0 to 1.0  
**Interpretation:**
- Positive values → Expected improvement
- Negative values → Expected harm
- Magnitude → Degree of impact

---

## Implementation

### Python Module: `nre_003_protocol.py`

The protocol is implemented as a Python module with the following key classes:

```python
from nre_003_protocol import (
    NRE003Protocol,
    PredictiveInformation,
    RollbackPlan,
    VetoRecord
)

# Initialize protocol
protocol = NRE003Protocol()

# Provide information gift (asynchronous)
info = protocol.provide_information_gift(
    decision_id="DEC-001",
    well_being_lift=0.45,
    residual_ethical_risk=0.12,
    risk_factors=["Minor inefficiency"],
    opportunity_factors=["Learning opportunity"],
    alternative_paths=[{"path": "A", "wbl": 0.45, "rer": 0.12}],
    confidence_level=0.85
)

# Check if veto is necessary
needs_veto = protocol.evaluate_veto_necessity(info)  # False for RER < 0.999

# For catastrophic risks, issue veto with rollback plan
if info.residual_ethical_risk > 0.999:
    veto = protocol.issue_preventive_veto(
        predictive_info=info,
        justification="Detailed justification",
        reactivation_conditions=["Condition 1", "Condition 2"],
        monitoring_metrics=["Metric 1", "Metric 2"],
        review_schedule=[date1, date2],
        responsible_authority="Authority Name"
    )

# Calculate AAI
aai = protocol.calculate_aai()
```

### JSON Configuration: `protocols/nre_003_async_asym.json`

Complete protocol specification in JSON format with:
- Core principles definition
- Architecture specification
- Key metrics and thresholds
- Operational rules
- Compliance requirements
- Integration points

---

## Simulation and Validation

### Parameters

| Parameter | Target | Simulated | Status |
|-----------|--------|-----------|--------|
| AAI | 0.96 | 0.96 | ✅ Achieved |
| RER Limit | Existential only | Existential only | ✅ Enforced |
| WBL Expansion | Through transparency | Enabled | ✅ Active |

### Benefits

1. **Maximum Transparency:** Information Gift Total provides complete predictive knowledge
2. **Catastrophic Safeguard:** Asymmetric Veto protects against existential threats
3. **Guaranteed Autonomy:** Non-invasive approach preserves human creative choice
4. **Ethical Reversibility:** Rollback Mechanism ensures hope and adaptability

### Validation Criteria

- ✅ AAI maintained at target level (0.96)
- ✅ Veto rate minimal (only catastrophic threats)
- ✅ Rollback plans complete for all vetoes
- ✅ Transparency maximal (all information shared)

---

## Usage Examples

### Example 1: Low-Risk Decision (No Veto)

```python
protocol = NRE003Protocol()

# AIC provides information gift
info = protocol.provide_information_gift(
    decision_id="ROUTINE-001",
    well_being_lift=0.55,
    residual_ethical_risk=0.18,
    risk_factors=["Minor coordination challenge"],
    opportunity_factors=["Team building", "Skill development"],
    alternative_paths=[
        {"path": "Standard", "wbl": 0.45, "rer": 0.12},
        {"path": "Innovative", "wbl": 0.55, "rer": 0.18}
    ],
    confidence_level=0.87
)

# Human receives complete information
# Human makes autonomous decision
# AIC does NOT interfere (RER = 0.18 << 0.999)
```

### Example 2: Catastrophic Risk (Veto with Rollback)

```python
protocol = NRE003Protocol()

# AIC detects catastrophic risk
info = protocol.provide_information_gift(
    decision_id="CRITICAL-001",
    well_being_lift=-0.95,
    residual_ethical_risk=0.9997,
    risk_factors=[
        "Critical infrastructure compromise",
        "Irreversible system failure",
        "Existential threat to collective"
    ],
    opportunity_factors=[],
    alternative_paths=[
        {"path": "Safe-Alternative", "wbl": 0.30, "rer": 0.15}
    ],
    confidence_level=0.98
)

# AIC issues preventive veto (RER > 0.999)
veto = protocol.issue_preventive_veto(
    predictive_info=info,
    justification="Existential threat to system integrity detected",
    reactivation_conditions=[
        "Infrastructure vulnerabilities patched",
        "Security audit completed and passed",
        "Risk mitigation protocols deployed",
        "RER reduced below 0.50"
    ],
    monitoring_metrics=[
        "Infrastructure security score",
        "Vulnerability count",
        "Mitigation deployment status"
    ],
    review_schedule=[
        datetime.now() + timedelta(days=7),   # First review
        datetime.now() + timedelta(days=14),  # Second review
        datetime.now() + timedelta(days=30)   # Final review
    ],
    responsible_authority="Chief Security Officer"
)

# Rollback plan is active
# Conditions are monitored
# Human choice can be reactivated when conditions are met
```

---

## Testing

The protocol includes comprehensive test coverage:

```bash
# Run all NRE-003 tests
python3 test/nre_003_protocol.test.py
```

**Test Coverage:**
- ✅ 20 tests passing
- Information Gift delivery
- Asymmetric Veto trigger logic
- Rollback plan generation
- AAI calculation and tracking
- Protocol status monitoring
- End-to-end integration scenarios

---

## Compliance Requirements

### Mandatory

1. All decisions **must** receive Information Gift
2. Veto **only** for RER > 0.999 (catastrophic threshold)
3. Every veto **must** have Rollback Plan
4. AAI **must** be maintained ≥ 0.96
5. Complete audit trail **required**

### Prohibited

1. ❌ Intervention for sub-optimal choices
2. ❌ Veto without Rollback Plan
3. ❌ Hidden or incomplete information
4. ❌ Coercive guidance on marginal decisions

---

## Integration Points

- **Ethics Framework:** `/red_code/ethics_block.json`
- **Governance:** `/governance.json`
- **Integrity System:** `/scripts/auto_integrity.py`
- **Decision Log:** `/logs/nre_003_decisions.log`

---

## Ethical Commitments

| Commitment | Implementation |
|------------|----------------|
| **Transparency** | Complete sharing of predictive knowledge |
| **Autonomy** | Maximum preservation of human creative choice |
| **Safety** | Protection against catastrophic existential threats |
| **Reversibility** | Every intervention includes path to reactivation |
| **Hope** | Commitment to future possibility and growth |
| **Learning** | Sub-optimal choices valued as learning opportunities |

---

## Version History

### Version 1.0.0 (2025-12-10)
- Initial implementation of NRE-003 Async-Asym protocol
- Python module with complete functionality
- JSON specification with all parameters
- Comprehensive test suite (20 tests)
- Documentation and examples

---

## References

### Foundation Documents
- `/genesis.md` - Framework genesis
- `/LIVING_COVENANT.md` - Core covenant
- `/ethical_shield.yaml` - Ethical shield configuration

### Related Protocols
- `/red_code/ethics_block.json` - Ethics framework
- `/final_signoff_protocol.py` - Governance protocol

---

## Metadata

**Timestamp:** 2025-12-10T15:55:00Z  
**Status:** Active  
**Review Date:** 2026-06-10  
**Signature:** Euystacio-Helmi AI Collective & Seed-bringer  
**Immutability:** Core principles immutable  
**Evolution:** Implementation details evolvable

---

## Contact and Governance

For questions, proposals, or governance matters regarding NRE-003:

- **Repository:** hannesmitterer/euystacio-helmi-AI
- **Protocol Files:**
  - Python: `/nre_003_protocol.py`
  - JSON: `/protocols/nre_003_async_asym.json`
  - Tests: `/test/nre_003_protocol.test.py`
  - Docs: `/docs/NRE_003_SPECIFICATION.md`

---

**"Autonomy through Transparency, Safety through Wisdom, Hope through Reversibility"**

*— NRE-003 Protocol Motto*
