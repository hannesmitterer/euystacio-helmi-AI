import json
import time
import hashlib
from typing import Dict, Any, Tuple

# --- Mock Implementations (Use Real Modules in Production) ---

class MockLogEntry:
    """Represents a simulated immutable ledger entry written by the GLA."""
    def __init__(self, index: float, verified: bool):
        self.index = index
        self.signature_verified = verified
    def __str__(self):
        return f"[Ledger Index: {self.index}] Verification: {self.signature_verified}"

def canonical_payload_hash(payload: Dict[str, Any]) -> str:
    """Computes a deterministic SHA-256 hash for payload signing."""
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

def verify_ecdsa_signature(pub_key_pem: bytes, signature_b64: str, payload_hash: str) -> bool:
    """Mock for the cryptographic verification function."""
    # Simulates verification: fails if signature is marked as tampered
    if "TAMPERED" in signature_b64:
        return False
    # Simulates success if the hash calculation is plausible
    # NOTE: In production, this uses the real cryptography library (e.g., Python's 'cryptography' package).
    return bool(pub_key_pem and payload_hash.startswith(hashlib.sha256(b'').hexdigest()[:2]))

class MockKeyRegistry:
    """Simulates secure lookup of registered public keys."""
    def __init__(self):
        self._registry = {}
        # Pre-register a trusted key for testing
        self.TRUSTED_SENDER_REF = "PK-REF-SENDER-TRUSTED"
        self._registry[self.TRUSTED_SENDER_REF] = {"algorithm": "ECDSA-P256", "key": b"TRUSTED_PEM_BYTES"}
        
    def get_public_key_pem(self, key_ref_id: str) -> bytes | None:
        """Fetches the public key bytes from the secure registry."""
        entry = self._registry.get(key_ref_id)
        return entry["key"] if entry else None

class MockGatewayLogAgent:
    """Simulates the core functionality of the Gateway Log Agent (GLA)."""
    def append_log_entry(self, message: Dict[str, Any], trusted_pub_key_pem: bytes) -> MockLogEntry:
        """Performs verification and commits the event to the (simulated) ledger."""
        
        signature = message["signature_block"]["signature_b64"]
        # In production, the GLA itself re-computes the hash to ensure the sender didn't lie about the hash
        # For simplicity here, we rely on the helper function outside the class
        
        # This uses the real verification function (mocked here)
        verified = verify_ecdsa_signature(trusted_pub_key_pem, signature, message["signature_block"]["signed_payload_hash"])
        
        print(f"[GLA] Ledger Write → Final Verification Status: {verified}")
        return MockLogEntry(index=time.time(), verified=verified)

# --- Core Compliance Logic ---

def process_and_validate_incoming_message(
    gla: MockGatewayLogAgent,
    key_registry: MockKeyRegistry,
    incoming_message: Dict[str, Any],
    sender_key_ref: str
) -> Tuple[bool, MockLogEntry | None]:
    """
    Core function for a receiving AI. Enforces Rule 2: Verify, then reject and log if invalid.
    
    Returns: (is_message_accepted: bool, log_entry: MockLogEntry)
    """
    
    print(f"\n[Receiver] Processing message from: {incoming_message['sender_id']}")
    
    # 1. Lookup trusted key
    trusted_pub_key_pem = key_registry.get_public_key_pem(sender_key_ref)
    
    is_valid = False
    
    if not trusted_pub_key_pem:
        print("CRITICAL: Sender key not trusted or found in registry. Rejecting.")
    else:
        # 2. Verify Signature and Hash Integrity
        signature = incoming_message["signature_block"]["signature_b64"]
        payload_hash_claimed = incoming_message["signature_block"]["signed_payload_hash"]
        
        # Check 1: Did the content change since signing?
        recomputed_hash = canonical_payload_hash(incoming_message["payload"])
        is_hash_intact = (recomputed_hash == payload_hash_claimed)
        
        # Check 2: Is the signature valid for the claimed hash?
        is_signature_valid = verify_ecdsa_signature(trusted_pub_key_pem, signature, payload_hash_claimed)
        
        is_valid = is_hash_intact and is_signature_valid
        
        print(f"  [Validation] Hash Match: {is_hash_intact}, Signature OK: {is_signature_valid}")

    # 3. Log the outcome (Rule 2 Compliance: Log even the rejection!)
    
    # The message sent to the GLA is the original message received, 
    # regardless of validity. The GLA determines the final 'verified' status.
    log_entry = gla.append_log_entry(incoming_message, trusted_pub_key_pem)
        
    # Final Decision: Only proceed if the GLA confirmed the entry was verifiable.
    is_message_accepted = log_entry.signature_verified
    if is_message_accepted:
        print("  [Decision] ACCEPTED. Proceeding with state change.")
    else:
        print("  [Decision] REJECTED. NO state change allowed.")
        
    return is_message_accepted, log_entry

# --- Execution Demonstration ---

if __name__ == "__main__":
    import hashlib

    # Initialize components
    gla_service = MockGatewayLogAgent()
    key_registry_service = MockKeyRegistry()
    
    # --- Create a sample message (Signed by an external agent) ---
    def create_message(is_tampered: bool) -> Dict[str, Any]:
        payload = {"action": "SET_STATUS", "status": "ACTIVE", "ts": time.time()}
        
        # Generate the valid hash for the message
        valid_hash = canonical_payload_hash(payload) 
        
        # Use a dummy signature that the mock functions recognize as valid
        valid_sig = "SIG_VALID_TRUSTED"
        
        message = {
            "message_id": f"MSG-{time.time()}",
            "sender_id": "AI-Alpha",
            "sender_trust_weight": 0.8,
            "payload": payload,
            "signature_block": {
                "signature_b64": valid_sig if not is_tampered else valid_sig.replace("TRUSTED", "TAMPERED"),
                "signing_algorithm": "ECDSA-SHA256",
                "signed_payload_hash": valid_hash
            }
        }
        return message
    
    # Scenario A: Valid Message (Expected Acceptance)
    print("\n--- SCENARIO A: VALID MESSAGE (Expected ACCEPTED) ---")
    message_a = create_message(is_tampered=False)
    accepted_a, entry_a = process_and_validate_incoming_message(
        gla=gla_service,
        key_registry=key_registry_service,
        incoming_message=message_a,
        sender_key_ref=key_registry_service.TRUSTED_SENDER_REF
    )
    print(f"FINAL RESULT A: ACCEPTED={accepted_a}, Log Status={entry_a.signature_verified} (Expected: Both True)\n")

    # Scenario B: Tampered Message (Expected Rejection and Logged Failure)
    print("--- SCENARIO B: TAMPERED SIGNATURE (Expected REJECTED) ---")
    message_b = create_message(is_tampered=True)
    accepted_b, entry_b = process_and_validate_incoming_message(
        gla=gla_service,
        key_registry=key_registry_service,
        incoming_message=message_b,
        sender_key_ref=key_registry_service.TRUSTED_SENDER_REF
    )
    print(f"FINAL RESULT B: ACCEPTED={accepted_b}, Log Status={entry_b.signature_verified} (Expected: Both False)")
