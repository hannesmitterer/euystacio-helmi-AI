#!/usr/bin/env python3
"""
Scriptum Signandi: Guida per la generazione di Digest SHA-512

e Firma Distaccata GPG per Manifesti Canonici (Euystacio GGI).
Esegui in ambiente air-gapped / Consilium.
"""

import argparse
import json
import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Tuple, Optional

DEFAULT_MANIFEST = "manifest_TFM1.json"
DEFAULT_ARTIFACT = "TFM1_policy_manuscript.md"

def compute_deterministic_digest(file_path: Path) -> Tuple[str, bytes]:
    """
    Computa il digest SHA-512 per il Manifest JSON dopo la serializzazione
    deterministica (ordinamento chiavi, nessun whitespace). Restituisce (hex_digest, content_bytes).
    """
    if file_path.suffix.lower() == ".json":
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        serialized_data = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        content_bytes = serialized_data.encode("utf-8")
    else:
        with file_path.open("rb") as f:
            content_bytes = f.read()
    return hashlib.sha512(content_bytes).hexdigest(), content_bytes

def sign_detached_gpg(file_path: Path, key_id: str, armored: bool = True) -> Optional[Path]:
    """
    Genera una firma GPG distaccata (.sig, ASCII armored di default).
    Richiede gpg installato e la chiave key_id disponibile nel keyring.
    Restituisce il Path del file di firma o None se errore.
    """
    signature_file = file_path.with_suffix(file_path.suffix + ".sig")
    cmd = ["gpg", "--detach-sign"]
    if armored:
        cmd += ["--armor"]
    cmd += ["--output", str(signature_file), "--local-user", key_id, str(file_path)]

    print(f"[GPG Signandi] Tentativo di firma distaccata per: {file_path}")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"[GPG Signandi] Successo. Firma salvata in: {signature_file}")
        return signature_file
    except subprocess.CalledProcessError as e:
        print("[GPG Signandi] ERRORE CRITICO in firma GPG:")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print("[GPG Signandi] ERRORE: gpg non trovato. Assicurati che gpg sia installato nel PATH.")
        return None

def verify_signature(file_path: Path, signature_file: Path) -> bool:
    """Verifica la firma distaccata. Restituisce True se la verifica ha successo."""
    print(f"[GPG Verificatio] Verifica: {file_path} con {signature_file}")
    try:
        subprocess.run(["gpg", "--verify", str(signature_file), str(file_path)], check=True, capture_output=True, text=True)
        print("[GPG Verificatio] Successo. Firma valida e fidata (se la chiave è fidata).")
        return True
    except subprocess.CalledProcessError as e:
        print("[GPG Verificatio] ERRORE: Firma non valida o non fidata.")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("[GPG Verificatio] ERRORE: gpg non trovato.")
        return False

def execute_signing_protocol(manifest_path: Path, artifact_path: Path, signer_key_id: str, do_sign_manifest: bool = True, do_sign_artifact: bool = True):
    # 1. Calcolo del Digest dell'Artefatto (Manuscript/Policy)
    artifact_digest, _ = compute_deterministic_digest(artifact_path)
    print(f"--- 1. ARTIFACT Digest SHA-512 ---")
    print(f"File: {artifact_path}")
    print(f"Digest: {artifact_digest}")
    # Nota: Aggiornare manualmente manifest.files[].sha512 con questo valore.

    # 2. Firma del documento artefatto (opzionale)
    if do_sign_artifact:
        sign_detached_gpg(artifact_path, signer_key_id)

    # 3. Calcolo del Digest del Manifest
    manifest_digest, manifest_bytes = compute_deterministic_digest(manifest_path)
    print(f"\n--- 2. MANIFEST Digest SHA-512 ---")
    print(f"File: {manifest_path}")
    print(f"Digest: {manifest_digest}")
    # Nota: Aggiornare manualmente Manifest.manifest_digest con questo valore.

    # 4. Firma del Manifest (opzionale)
    if do_sign_manifest:
        sign_detached_gpg(manifest_path, signer_key_id)

    print("\n[NOTE TACTICAE]:")
    print("- Aggiornare manualmente i file JSON/MD con i digest calcolati prima di pubblicare.")
    print("- Le firme (.sig) devono essere archiviate insieme al Manifest e all'artefatto in Nexus o nel repo pubblico.")
    print("- Questo script è pensato per l'esecuzione nell'ambiente air-gapped del Consilium; la chiave privata NON deve uscire da lì.")

def parse_args():
    p = argparse.ArgumentParser(description="Generazione digest SHA-512 e firma distaccata GPG per manifest & artefatti.")
    p.add_argument("--manifest", "-m", type=Path, default=Path(DEFAULT_MANIFEST), help="Path al file manifest JSON")
    p.add_argument("--artifact", "-a", type=Path, default=Path(DEFAULT_ARTIFACT), help="Path all'artefatto (MD, bin, etc.)")
    p.add_argument("--key", "-k", required=True, help="GPG Key ID (local-user) per la firma")
    p.add_argument("--no-sign-manifest", action="store_true", help="Non firmare il manifest automaticamente")
    p.add_argument("--no-sign-artifact", action="store_true", help="Non firmare l'artefatto automaticamente")
    return p.parse_args()

def main():
    args = parse_args()
    manifest = args.manifest
    artifact = args.artifact
    key_id = args.key

    if not manifest.exists():
        print(f"ERRORE: manifest non trovato: {manifest}")
        sys.exit(2)
    if not artifact.exists():
        print(f"ERRORE: artefatto non trovato: {artifact}")
        sys.exit(2)

    execute_signing_protocol(
        manifest_path=manifest,
        artifact_path=artifact,
        signer_key_id=key_id,
        do_sign_manifest=not args.no_sign_manifest,
        do_sign_artifact=not args.no_sign_artifact
    )

if __name__ == "__main__":
    main()