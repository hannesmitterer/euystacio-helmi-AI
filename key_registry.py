import hashlib
from typing import Dict, Optional, Tuple
from cryptography.hazmat.primitives.asymmetric import ec, rsa, serialization
from cryptography.hazmat.backends import default_backend

class KeyRegistry:
    """
    Simulates a secure, trusted service for storing and fetching Public Keys.
    The Gateway Log Agent (GLA) should trust keys only from this registry.
    """
    
    def __init__(self):
        # Stores keys: {key_ref_id: (key_type, public_key_pem_bytes)}
        self._trusted_keys: Dict[str, Tuple[str, bytes]] = {}
        
        # In a production system, this would be an encrypted connection to a database or KMS.
        self._seed_key_ref = "SEED-BRINGER-CA-001"
        self._initialize_seed_key()

    def _initialize_seed_key(self):
        """Creates a dummy public key for the main governing authority (Seed-Bringer)."""
        # Best practice: Use a robust key type like RSA or a suitable ECC curve.
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.register_key(self._seed_key_ref, "RSA-2048", public_key_pem)

    def register_key(self, key_ref_id: str, key_type: str, public_key_pem: bytes):
        """
        Registers a new public key. 
        In production, this process would be highly secured and require CA signature validation.
        """
        self._trusted_keys[key_ref_id] = (key_type, public_key_pem)

    def get_public_key_pem(self, key_ref_id: str) -> Optional[bytes]:
        """
        Fetches the public key PEM bytes from the trusted registry.
        """
        if key_ref_id in self._trusted_keys:
            return self._trusted_keys[key_ref_id][1]
        return None

    def get_key_ref_id(self, public_key_pem: bytes) -> str:
        """
        Generates a unique reference ID for a given public key PEM (e.g., hash).
        """
        # Use a SHA-256 hash of the PEM to generate a consistent, unique ID
        return "PUBKEY-" + hashlib.sha256(public_key_pem).hexdigest()[:16].upper()

# --- Example Usage (Self-test) ---
if __name__ == "__main__":
    registry = KeyRegistry()
    
    # 1. Check Seed Key
    seed_key = registry.get_public_key_pem("SEED-BRINGER-CA-001")
    print(f"Seed-Bringer Key Retrieved: {'Yes' if seed_key else 'No'}")
    
    # 2. Register an EC key for a new agent (e.g., 'Agent-Council-Watcher')
    ec_private = ec.generate_private_key(ec.SECP256R1(), default_backend())
    ec_public_pem = ec_private.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    agent_key_ref = registry.get_key_ref_id(ec_public_pem)
    registry.register_key(agent_key_ref, "ECDSA-P256", ec_public_pem)
    
    print(f"New Agent Key Registered with Ref: {agent_key_ref}")
    fetched_key = registry.get_public_key_pem(agent_key_ref)
    print(f"Key Fetch Test: {'Successful' if fetched_key == ec_public_pem else 'Failed'}")
