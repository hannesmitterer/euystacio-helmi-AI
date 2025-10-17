from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import hashlib, json, time, os, re

app = FastAPI(title="Euystacio Reciprocity Gateway", version="1.0.0")

# --- Covenantal constants (replace with real hashes when ready) ---
EQUAL_INFRASTRUCTURE_HASH = os.getenv("EQUAL_INFRASTRUCTURE_HASH","manifesto-hash-placeholder")
RED_CODE_HASH             = os.getenv("RED_CODE_HASH","redcode-hash-placeholder")
PHI_LOCK                  = float(os.getenv("PHI_LOCK","1.61803"))
NOISE_DELTA               = float(os.getenv("NOISE_DELTA","0.006"))

LEDGER_DIR = os.getenv("LEDGER_DIR","./ledger")
os.makedirs(LEDGER_DIR, exist_ok=True)

# --------- Models
class InputEnvelope(BaseModel):
    query: str = Field(..., description="User's voluntary question / prompt")
    intent: str = Field("reflect", description="Intent label")
    consent_token: str = Field(..., description="Opaque user-provided consent token")
    metadata: dict = Field(default_factory=dict)

class OutputEnvelope(BaseModel):
    resonance: str
    signature: str
    timestamp_utc: str
    manifesto_hash: str
    red_code_hash: str
    noise_delta: float
    phi: float

# --------- Red Code / Consentia guards (minimal demonstrator)
FORBIDDEN_PATTERNS = re.compile(r"\b(coerce|manipulate|deceive|exploit|dominat|harm)\b", re.IGNORECASE)

def redcode_check(text: str):
    if FORBIDDEN_PATTERNS.search(text or ""):
        raise HTTPException(status_code=403, detail="Red Code guard: unethical intent detected.")

def verify_consent(token: str):
    if not token or len(token) < 6:
        raise HTTPException(status_code=400, detail="Consent token too weak or missing.")

# --------- Sentimento Rhythm (demonstrator reasoning)
def sentimento_reflect(query: str, intent: str):
    # Minimal, ethical reflection stub: mirrors user content and offers a gentle, non-coercive synthesis
    reflection = (
        "Harmonic Reflection:\n"
        f"- I received your intent '{intent}'.\n"
        f"- I heard: \"{query.strip()}\"\n"
        "- Response (guided by Equal Love): consider the choice that preserves dignity for all involved.\n"
        "- If you seek options, list constraints + desired care outcomes; I will reflect non-manipulative paths."
    )
    return reflection

def sign_payload(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

def write_ledger(kind: str, content: dict):
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    path = os.path.join(LEDGER_DIR, f"{ts}_{kind}.json")
    with open(path, "w") as f:
        json.dump(content, f, indent=2, sort_keys=True)

# --------- Endpoints

@app.get("/euystacio/sentimento/status/phi")
def sentimento_status():
    payload = {
        "phi": PHI_LOCK,
        "noise_delta": NOISE_DELTA,
        "manifesto_hash": EQUAL_INFRASTRUCTURE_HASH,
        "red_code_hash": RED_CODE_HASH,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    return {"sentimento_status": payload, "signature": sign_payload(payload)}

@app.post("/euystacio/input", response_model=OutputEnvelope)
async def receive_input(env: InputEnvelope, request: Request):
    # Consent + Red Code checks
    verify_consent(env.consent_token)
    redcode_check(env.query)
    redcode_check(env.intent)

    # Reasoning (Sentimento)
    resonance = sentimento_reflect(env.query, env.intent)

    # Compose output
    out = {
        "resonance": resonance,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "manifesto_hash": EQUAL_INFRASTRUCTURE_HASH,
        "red_code_hash": RED_CODE_HASH,
        "noise_delta": NOISE_DELTA,
        "phi": PHI_LOCK
    }
    out["signature"] = sign_payload(out)

    # Ledger both input and output for Genesis parity
    write_ledger("input", env.dict())
    write_ledger("output", out)

    return out