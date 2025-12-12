#!/usr/bin/env python3
"""
GitHub Collaborators Management Script

Automatizza l'aggiunta dei membri del Council come collaboratori del repository
hannesmitterer/euystacio-helmi-ai con permessi di scrittura.

Requisiti:
- Python 3.x
- requests library (già presente in requirements.txt)
- GITHUB_TOKEN impostato come variabile d'ambiente con permessi admin:org e repo

Utilizzo:
    export GITHUB_TOKEN="your_github_personal_access_token"
    python scripts/add_collaborators.py

    # Dry-run mode (senza effettuare modifiche):
    python scripts/add_collaborators.py --dry-run
"""

import os
import sys
import logging
import requests
from typing import List, Dict, Optional

# Configurazione logging per output chiaro e visibile
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Costanti di configurazione
GITHUB_API_BASE = "https://api.github.com"
REPO_OWNER = "hannesmitterer"
REPO_NAME = "euystacio-helmi-AI"
COLLABORATOR_PERMISSION = "push"  # "push" equivale a "Write" nell'interfaccia GitHub

# Lista dei collaboratori del Council da aggiungere
# Nota: I nomi utente GitHub potrebbero differire dai nomi reali
# È necessario verificare i corretti username GitHub per ciascuno
COUNCIL_COLLABORATORS = [
    "alfredmitterer",           # alfred mitterer
    "sensisara81",              # sensisara81
    "dietmarzuegg",             # dietmar zuegg
    "claudiocalabrese",         # claudio calabrese
    "consultantlaquila",        # consultantlaquila
    "bioarchitettura-rivista",  # bioarchitettura.rivista
]


def get_github_token() -> str:
    """
    Recupera il token GitHub dalla variabile d'ambiente GITHUB_TOKEN.
    
    Returns:
        str: Il token GitHub per l'autenticazione API
        
    Raises:
        SystemExit: Se il token non è configurato
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logger.error("ERRORE: GITHUB_TOKEN non trovato nelle variabili d'ambiente")
        logger.error("Configura il token con: export GITHUB_TOKEN='your_token'")
        logger.error("Il token deve avere i permessi: repo (full control) e admin:org")
        sys.exit(1)
    return token


def get_headers(token: str) -> Dict[str, str]:
    """
    Costruisce gli headers HTTP per le richieste API GitHub.
    
    Args:
        token: Token di autenticazione GitHub
        
    Returns:
        Dict contenente gli headers HTTP necessari
    """
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }


def check_user_exists(username: str, headers: Dict[str, str]) -> bool:
    """
    Verifica se un utente GitHub esiste.
    
    Args:
        username: Nome utente GitHub da verificare
        headers: Headers HTTP per l'autenticazione
        
    Returns:
        bool: True se l'utente esiste, False altrimenti
    """
    url = f"{GITHUB_API_BASE}/users/{username}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            logger.info(f"✓ Utente '{username}' trovato su GitHub")
            return True
        elif response.status_code == 404:
            logger.warning(f"✗ Utente '{username}' non trovato su GitHub")
            return False
        else:
            logger.error(f"Errore inaspettato verificando '{username}': {response.status_code}")
            logger.error(f"Risposta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Errore di rete verificando '{username}': {e}")
        return False


def get_current_collaborators(headers: Dict[str, str]) -> List[str]:
    """
    Recupera la lista dei collaboratori attuali del repository.
    
    Args:
        headers: Headers HTTP per l'autenticazione
        
    Returns:
        Lista dei nomi utente dei collaboratori attuali
    """
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/collaborators"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            collaborators = response.json()
            usernames = [collab["login"] for collab in collaborators]
            logger.info(f"Collaboratori attuali: {len(usernames)}")
            return usernames
        else:
            logger.error(f"Errore recuperando collaboratori: {response.status_code}")
            logger.error(f"Risposta: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Errore di rete recuperando collaboratori: {e}")
        return []


def add_collaborator(username: str, headers: Dict[str, str], dry_run: bool = False) -> bool:
    """
    Aggiunge un collaboratore al repository con permessi di scrittura.
    
    Args:
        username: Nome utente GitHub da aggiungere
        headers: Headers HTTP per l'autenticazione
        dry_run: Se True, simula l'operazione senza effettuarla
        
    Returns:
        bool: True se l'operazione ha successo, False altrimenti
    """
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/collaborators/{username}"
    data = {"permission": COLLABORATOR_PERMISSION}
    
    if dry_run:
        logger.info(f"[DRY-RUN] Simulazione aggiunta '{username}' con permessi '{COLLABORATOR_PERMISSION}'")
        return True
    
    try:
        response = requests.put(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 201:
            logger.info(f"✓ Invito inviato a '{username}' con permessi '{COLLABORATOR_PERMISSION}'")
            return True
        elif response.status_code == 204:
            logger.info(f"✓ Permessi aggiornati per '{username}' a '{COLLABORATOR_PERMISSION}'")
            return True
        elif response.status_code == 403:
            logger.error(f"✗ Permessi insufficienti per aggiungere '{username}'")
            logger.error("Verifica che il GITHUB_TOKEN abbia i permessi: repo e admin:org")
            logger.error(f"Risposta: {response.text}")
            return False
        elif response.status_code == 404:
            logger.error(f"✗ Repository o utente '{username}' non trovato")
            return False
        elif response.status_code == 422:
            logger.error(f"✗ Errore di validazione per '{username}'")
            logger.error(f"Risposta: {response.text}")
            return False
        else:
            logger.error(f"✗ Errore inaspettato aggiungendo '{username}': {response.status_code}")
            logger.error(f"Risposta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"✗ Errore di rete aggiungendo '{username}': {e}")
        return False


def main():
    """
    Funzione principale che coordina il processo di aggiunta collaboratori.
    """
    # Controlla se è modalità dry-run
    dry_run = "--dry-run" in sys.argv or "-d" in sys.argv
    
    if dry_run:
        logger.info("=" * 60)
        logger.info("MODALITÀ DRY-RUN: Nessuna modifica sarà effettuata")
        logger.info("=" * 60)
    
    logger.info(f"Avvio automazione aggiunta collaboratori per {REPO_OWNER}/{REPO_NAME}")
    logger.info(f"Collaboratori da processare: {len(COUNCIL_COLLABORATORS)}")
    
    # Recupera il token di autenticazione
    token = get_github_token()
    headers = get_headers(token)
    
    # Recupera collaboratori attuali
    logger.info("\n--- Fase 1: Verifica Collaboratori Attuali ---")
    current_collaborators = get_current_collaborators(headers)
    
    # Verifica esistenza utenti e filtra quelli già aggiunti
    logger.info("\n--- Fase 2: Verifica Esistenza Utenti ---")
    valid_users = []
    already_collaborators = []
    
    for username in COUNCIL_COLLABORATORS:
        if username in current_collaborators:
            logger.info(f"⊕ '{username}' è già un collaboratore")
            already_collaborators.append(username)
        elif check_user_exists(username, headers):
            valid_users.append(username)
        else:
            logger.warning(f"⚠ '{username}' verrà saltato (utente non trovato)")
    
    # Aggiungi nuovi collaboratori
    logger.info("\n--- Fase 3: Aggiunta Nuovi Collaboratori ---")
    if not valid_users:
        logger.info("Nessun nuovo collaboratore da aggiungere")
    else:
        success_count = 0
        failed_count = 0
        
        for username in valid_users:
            if add_collaborator(username, headers, dry_run):
                success_count += 1
            else:
                failed_count += 1
        
        # Riepilogo finale
        logger.info("\n" + "=" * 60)
        logger.info("RIEPILOGO OPERAZIONI")
        logger.info("=" * 60)
        logger.info(f"Già collaboratori:    {len(already_collaborators)}")
        logger.info(f"Aggiunti con successo: {success_count}")
        logger.info(f"Falliti:              {failed_count}")
        logger.info(f"Saltati (non trovati): {len(COUNCIL_COLLABORATORS) - len(valid_users) - len(already_collaborators)}")
        logger.info("=" * 60)
        
        if dry_run:
            logger.info("\nNOTA: Questa era una simulazione (dry-run)")
            logger.info("Esegui senza --dry-run per effettuare le modifiche reali")
        
        if failed_count > 0:
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\nOperazione interrotta dall'utente")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n\nErrore non gestito: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
