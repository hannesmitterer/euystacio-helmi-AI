import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Optional

# ==== LOG ENTRY: The Immutable Record ====
@dataclass(frozen=True)
class LogEntry:
    """
    The immutable log record. 'frozen=True' ensures that fields cannot be
    modified after initialization, enforcing immutability.
    """
    timestamp: float = field(default_factory=time.time)
    agent_id: str
    event_details: str
    previous_hash: str 
    entry_hash: Optional[str] = field(init=False, default=None)
    signature: Optional[str] = field(init=False, default=None)

    def calculate_hash(self) -> str:
        """
        Generates the SHA-256 hash. **Best Practice:** Use sorted keys and 
        UTF-8 encoding to guarantee canonical serialization and consistent hashing.
        """
        data_to_hash = {
            'timestamp': self.timestamp,
            'agent_id': self.agent_id,
            'event_details': self.event_details,
            'previous_hash': self.previous_hash
        }
        json_data = json.dumps(data_to_hash, sort_keys=True).encode('utf-8')
        return hashlib.sha256(json_data).hexdigest()

    def __post_init__(self):
        """Calculates and sets the hash immediately after initialization."""
        object.__setattr__(self, 'entry_hash', self.calculate_hash())

    def set_signature(self, signature_hex: str):
        """Sets the digital signature (must be done post-hash calculation)."""
        object.__setattr__(self, 'signature', signature_hex)

    def get_signed_message_bytes(self) -> bytes:
        """Returns the bytes of the log entry's hash digest, which is what is signed."""
        if not self.entry_hash:
            raise ValueError("Entry hash must be calculated before signing.")
        return self.entry_hash.encode('utf-8')

# ==== DIGITAL SIGNATURE AGENT ====
# Imports for cryptography (requires `pip install cryptography`)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend

class SignatureAgent:
    def __init__(self):
        # Key generation for demonstration; in production, load securely!
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def sign_message(self, message_bytes: bytes) -> str:
        """Signs the message (LogEntry hash) using the private key with RSA-PSS."""
        signature = self.private_key.sign(
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature.hex()

    def verify_signature(self, message_bytes: bytes, signature_hex: str, public_key) -> bool:
        """Verifies the signature using the public key."""
        try:
            signature_bytes = bytes.fromhex(signature_hex)
            public_key.verify(
                signature_bytes,
                message_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False
        except Exception:
            return False

# ==== GATEWAY LOG AGENT ====
class GatewayLogAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.signature_agent = SignatureAgent()
        self.log_chain = []
        self.current_hash = "GENESIS"

    def create_log_entry(self, event_details: str) -> LogEntry:
        """
        Creates, signs, and appends a new immutable log entry to the chain.
        This enforces the 'blockchain ledger' logic.
        """
        new_entry = LogEntry(
            agent_id=self.agent_id,
            event_details=event_details,
            previous_hash=self.current_hash
        )
        signed_message = new_entry.get_signed_message_bytes()
        signature_hex = self.signature_agent.sign_message(signed_message)
        new_entry.set_signature(signature_hex)
        self.log_chain.append(new_entry)
        self.current_hash = new_entry.entry_hash 
        return new_entry

    def verify_chain_integrity(self) -> bool:
        """
        Verifies all log entries for both hash chain integrity and digital authenticity.
        """
        pubkey = self.signature_agent.public_key
        for i in range(len(self.log_chain)):
            current_entry = self.log_chain[i]
            if i > 0:
                previous_entry = self.log_chain[i-1]
                if current_entry.previous_hash != previous_entry.entry_hash:
                    print(f"🚨 TAMPER ALERT: Chain broken at Entry {i}! Previous hash mismatch.")
                    return False
            if current_entry.calculate_hash() != current_entry.entry_hash:
                print(f"🚨 TAMPER ALERT: Entry {i} has been internally modified!")
                return False
            message_bytes = current_entry.get_signed_message_bytes()
            if not self.signature_agent.verify_signature(message_bytes, current_entry.signature, pubkey):
                print(f"🚨 TAMPER ALERT: Digital signature failed for Entry {i}! Content altered or signature forged.")
                return False
        return True