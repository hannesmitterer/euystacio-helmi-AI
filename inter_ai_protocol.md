# 📜 Inter-AI Communication Gateway Protocol: The Golden Bible Red Code

**Document Version:** 1.0  
**Date:** 2025-10-23  
**Scope:** All inter-AI communication and state-altering actions passing through the Gateway Log Agent (GLA) ecosystem of the Peace Platform.

This protocol establishes the mandatory standards for absolute transparency and accessibility, enforced by cryptographic means, ensuring that the integrity of the platform's history is never compromised.

---

## 1. Core Principles and Enforcement

The entire protocol is governed by the Golden Bible Red Code, which dictates:  
**No Non-Transparency, No No-Accessibility.**

| Principle   | Enforcement Mechanism                                                                 |
|-------------|--------------------------------------------------------------------------------------|
| Integrity   | Every transaction is secured by a cryptographic hash chain maintained by the GLA.    |
| Authenticity| Every message must be secured by an ECDSA Digital Signature from the sender.         |
| Immutability| All critical logs are immediately committed to the secure ledger; records cannot be deleted or modified. |

The Gateway Log Agent (GLA) is the official Cryptographic Custodian and Protocol Enforcer for the platform.

---

## 2. A. Message Format Standardization

All critical inter-AI messages must be submitted to the GLA as a single, valid JSON object that strictly adheres to the following structure.

### Required Structure

The message must contain the `payload` (the message content) and the `signature_block` (the cryptographic proof).

{
    "message_id": "MSG-TXN-1786543210.987",
    "sender_id": "AI-Sentinel-Alpha",
    "sender_trust_weight": 0.95,
    "payload": {
        "performative": "TRUST_UPDATE",
        "Audit_Context": {"user_id": "U123", "session": "S007"},
        "details": "Resource Allocation Approved.",
        "ts": 1786543210.987
    },
    "signature_block": {
        "signature_b64": "base64-encoded-ECDSA-signature-of-canonical-payload-hash",
        "signing_algorithm": "ECDSA-SHA256",
        "signed_payload_hash": "SHA256-hash-of-canonical-payload"
    }
}

#### Key Requirements

| Field                          | Requirement                                                                                                                |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| `payload`                      | Must contain all critical information. This entire dictionary is converted to its canonical form and hashed for signing.   |
| `signature_block.signature_b64`| Must be the valid ECDSA signature created by the sender's private key over the `signed_payload_hash`.                      |
| Canonical Hashing              | The sender must use the standard canonical hashing function (lexicographically sorted JSON string hash) provided by the GLA module to ensure the receiver can verify the signature. |

---

## 3. B. Mandatory Logging Rules ("Red Code")

These rules are non-negotiable and must be enforced by application logic within the backend services.

### Rule 1: Log All State Changes & Trust Decisions
**Mandate:**  
Any action that alters the platform's state, changes a trust metric, or involves resource allocation must be logged via `gla.append_log_entry(message)` before the state change is finalized.

**Compliance:**  
No state or trust action is permitted to be unlogged.

### Rule 2: Enforce Signature Verification and Rejection
**Mandate:**  
Any message received by an AI that lacks a valid signature (i.e., verification fails) must be rejected and the rejection itself must be logged by the recipient AI.

**Compliance:**  
The recipient AI must call the GLA, submitting the received (failed) message. The GLA will record the log entry but set `signature_verified=False`.  
No unsigned message is accepted without a record of rejection.

### Rule 3: Seedbringer and Council Audit Rights
**Mandate:**  
The Seedbringer and Council retain immutable, ultimate access, and audit rights to the log ledger.

**Compliance:**  
Access is granted via the trusted, read-only Council API. Any tampering detected by the GLA's internal integrity check will trigger a mandatory, high-severity alert to these governing entities.

---

## 4. GLA Roles and Responsibilities

- **Cryptographic Custodian:** Maintains the integrity, authenticity, and immutability of all logged entries.
- **Protocol Enforcer:** Enforces mandatory logging, signature verification, and audit rights.
- **Audit Gateway:** Provides read-only access for governance entities (Seedbringer, Council) and triggers alerts on tamper detection.

---

## 5. Developer Compliance and Integration

All development teams must integrate the following:

| Task              | Component                 | Responsibility                                                        |
|-------------------|--------------------------|-----------------------------------------------------------------------|
| Integrate Signing | Backend/Microservice Logic| Use a secure utility to sign the payload hash before submitting the message. |
| Key Lookup        | Key Registry Module      | Ensure public keys are fetched from the Live Key Management Service (KMS/HSM), not hardcoded. |
| Log Ingestion     | Application Logic        | Wrap critical actions with the `gla.append_log_entry()` call.         |
| CI/CD Compliance  | GitHub Actions / CI Pipeline | Ensure the `test_gla.py` suite runs on every push and PR to verify cryptographic and chain integrity. |

---

## 6. Next Steps for Implementation Teams

- **Distribute this protocol** to all developers, backend engineers, and agent integrators.
- **Enforce compliance** via code reviews and CI/CD checks.
- **Document any deviations or exceptions** and seek council approval for changes.

---

**For questions, clarifications, or updates, contact the Council or Seedbringer governance team.