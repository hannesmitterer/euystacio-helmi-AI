import pytest
import json
import os
import sqlite3
import hashlib
from datetime import datetime

# --- IMPORTANT SETUP ---
# In a real project, replace the following import placeholder with the actual import:
# from your_gla_module import LogEntry, GatewayLogAgent, canonical_payload_hash, verify_ecdsa_signature, KeyRegistry
#
# For testing, we assume the core classes/functions are available via a shared context or import.
# The following imports and setup use the components defined in the prior tool code generation.
# If running this standalone, ensure the full GLA class and dependencies are in the execution path.

# Assuming the required components (LogEntry, GatewayLogAgent, etc.) are available globally
# or imported from the main module file, we define a fixture for setup/teardown.

# --- FIXTURES AND SETUP ---

@pytest.fixture(scope="function")
def setup_gla():
    """Fixture to initialize a clean GLA instance before each test."""
    DB_PATH = "test_gla_ledger.db"
    
    # 1. Teardown: Remove any existing test DB file
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # 2. Setup: Initialize a new GLA instance pointing to the test DB
    # NOTE: You may need to adjust the class name if it differs in your environment.
    gla = GatewayLogAgent(agent_id="GLA-TEST-01")
    gla.DB_PATH = DB_PATH # Ensure the GLA instance uses the test DB path
    gla._initialize_db()
    
    # Generate a key pair for testing signature features
    sender_key_agent = KeyRegistry()
    
    yield gla, sender_key_agent

    # 3. Final Teardown: Close connection and remove DB file
    gla.conn.close()
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def create_valid_message(key_agent, index, detail):
    """Helper to create a fully signed, valid message."""
    payload = {
        "performative": "TEST_ACTION",
        "Audit_Context": {"test_id": f"T{index}", "run": "R1"},
        "details": detail,
        "ts": time.time()
    }
    signing_payload_hash = canonical_payload_hash(payload)
    signature_b64 = key_agent.sign_payload_hash(signing_payload_hash.encode('utf-8'))
    
    return {
        "message_id": f"MSG-T{index}",
        "sender_id": "Agent-Test-Sender",
        "sender_trust_weight": 0.5 + (index / 10),
        "payload": payload,
        "signature_block": {
            "signature_b64": signature_b64,
            "signing_algorithm": "ECDSA-SHA256"
        }
    }

# --- TEST SUITES ---

## 1. Test Immutability and Core Data

def test_logentry_is_immutable():
    """1. Test Immutability: Verify a frozen dataclass cannot be modified."""
    entry = LogEntry(
        timestamp="2025-10-23T01:00:00Z", index=0, previous_hash="0"*64,
        message_id="MSG-0", sender_id="S1", performative="INIT", 
        audit_context={}, message_payload_hash="A"*64, 
        signature_verified=True, sender_trust_weight=1.0, 
        signature="", current_hash="B"*64
    )
    
    # Attempt to change a field (should raise an exception)
    with pytest.raises(AttributeError):
        entry.sender_id = "S2"

def test_canonical_hashing_consistency():
    """2. Test Canonical Hashing: Verify hash is deterministic across formatting changes."""
    payload_a = {"key1": 100, "key2": "value"}
    payload_b = {"key2": "value", "key1": 100} # Key order changed
    
    hash_a = canonical_payload_hash(payload_a)
    hash_b = canonical_payload_hash(payload_b)
    
    # Hashes must match due to sort_keys=True
    assert hash_a == hash_b
    
    # Check that a content change results in a different hash
    payload_c = {"key1": 101, "key2": "value"}
    hash_c = canonical_payload_hash(payload_c)
    
    assert hash_a != hash_c

# -------------------------------------------------------------

## 2. Test Cryptography

def test_signature_verification_valid(setup_gla):
    """3. Test Signature Verification (Valid): Test with a correct signature."""
    _, key_agent = setup_gla
    
    # Setup
    test_message = b"This is the canonical payload hash."
    pub_key_pem = key_agent.get_public_key_pem()
    valid_signature_b64 = key_agent.sign_payload_hash(test_message)
    
    # Verification (Should Pass)
    result = verify_ecdsa_signature(pub_key_pem, valid_signature_b64, test_message)
    assert result is True

def test_signature_verification_invalid_payload(setup_gla):
    """3. Test Signature Verification (Invalid): Test when the payload is altered."""
    _, key_agent = setup_gla
    
    # Setup
    original_message = b"Original canonical payload hash."
    tampered_message = b"Tampered canonical payload hash!"
    pub_key_pem = key_agent.get_public_key_pem()
    
    # Sign the original, but attempt to verify against the tampered message
    valid_signature_b64 = key_agent.sign_payload_hash(original_message)
    
    # Verification (Should Fail)
    result = verify_ecdsa_signature(pub_key_pem, valid_signature_b64, tampered_message)
    assert result is False

def test_signature_verification_invalid_signature(setup_gla):
    """3. Test Signature Verification (Invalid): Test when the signature itself is altered."""
    _, key_agent = setup_gla
    
    # Setup
    test_message = b"The payload hash."
    pub_key_pem = key_agent.get_public_key_pem()
    
    # Get a valid signature, then break it
    valid_signature_b64 = key_agent.sign_payload_hash(test_message)
    tampered_signature_b64 = valid_signature_b64.replace('A', 'B', 1)
    
    # Verification (Should Fail)
    result = verify_ecdsa_signature(pub_key_pem, tampered_signature_b64, test_message)
    assert result is False

# -------------------------------------------------------------

## 3. Test Chain Integrity

def test_chain_integrity_valid_multi_entry(setup_gla):
    """4. Test Chain Integrity (Pass): Verify a correctly chained ledger passes audit."""
    gla, key_agent = setup_gla
    pub_key_pem = key_agent.get_public_key_pem()
    
    # Append 3 valid entries
    gla.append_log_entry(create_valid_message(key_agent, 0, "Genesis event"), pub_key_pem)
    gla.append_log_entry(create_valid_message(key_agent, 1, "First follow-up"), pub_key_pem)
    gla.append_log_entry(create_valid_message(key_agent, 2, "Second follow-up"), pub_key_pem)

    # Verification (Should Pass)
    assert gla.verify_chain_integrity() is True

def test_chain_integrity_broken_link(setup_gla):
    """4. Test Chain Integrity (Fail on Link): Verify tamper detection if previous_hash is broken."""
    gla, key_agent = setup_gla
    pub_key_pem = key_agent.get_public_key_pem()
    
    # Append two entries
    gla.append_log_entry(create_valid_message(key_agent, 0, "A"), pub_key_pem)
    entry2 = gla.append_log_entry(create_valid_message(key_agent, 1, "B"), pub_key_pem)
    
    # Manually tamper with entry 2's previous_hash in the DB
    broken_hash = "1234567890" * 6 + "AA" # Invalid length, but distinct value
    gla.conn.execute(
        "UPDATE log_ledger SET previous_hash = ? WHERE entry_index = ?", 
        (broken_hash, entry2.index)
    )
    gla.conn.commit()

    # Verification (Should Fail)
    assert gla.verify_chain_integrity() is False

def test_chain_integrity_content_tampered(setup_gla):
    """4. Test Chain Integrity (Fail on Content): Verify tamper detection if log_data is altered."""
    gla, key_agent = setup_gla
    pub_key_pem = key_agent.get_public_key_pem()
    
    # Append one entry
    entry1 = gla.append_log_entry(create_valid_message(key_agent, 0, "Untampered original"), pub_key_pem)
    
    # Retrieve and tamper with the raw JSON data in the DB
    cursor = gla.conn.execute("SELECT log_data FROM log_ledger WHERE entry_index = 0")
    log_data_json = cursor.fetchone()[0]
    log_data = json.loads(log_data_json)
    
    # Tamper the content (but leave the stored current_hash unchanged)
    log_data["performative"] = "TAMPERED_ACTION"
    
    # Update the DB with the tampered content
    gla.conn.execute(
        "UPDATE log_ledger SET log_data = ? WHERE entry_index = 0", 
        (json.dumps(log_data),)
    )
    gla.conn.commit()

    # Verification (Should Fail)
    # The stored hash will not match the recomputed hash of the tampered log_data
    assert gla.verify_chain_integrity() is False
