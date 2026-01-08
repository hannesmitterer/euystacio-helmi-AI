# GitHub Collaborators Management

## Descrizione

Script Python per l'automazione dell'aggiunta dei membri del Council come collaboratori del repository `hannesmitterer/euystacio-helmi-AI`.

## Script: `add_collaborators.py`

### Funzionalità

Lo script automatizza completamente il processo di aggiunta collaboratori attraverso le GitHub REST API:

1. **Verifica Token**: Controlla la presenza e validità del GITHUB_TOKEN
2. **Verifica Collaboratori Attuali**: Recupera la lista dei collaboratori già presenti
3. **Verifica Esistenza Utenti**: Controlla che gli username GitHub siano validi
4. **Aggiunta Collaboratori**: Invia inviti ai nuovi collaboratori con permessi "Write"
5. **Gestione Errori**: Logging dettagliato di tutte le operazioni ed errori

### Collaboratori Configurati

Il script è configurato per aggiungere i seguenti membri del Council con permessi **"Write"** (push):

- `alfredmitterer` - alfred mitterer
- `sensisara81` - sensisara81
- `dietmarzuegg` - dietmar zuegg
- `claudiocalabrese` - claudio calabrese
- `consultantlaquila` - consultantlaquila
- `bioarchitettura-rivista` - bioarchitettura.rivista

> **Nota**: Gli username GitHub potrebbero dover essere verificati/aggiornati in caso di differenze tra nomi reali e username GitHub.

### Prerequisiti

1. **Python 3.x** installato
2. **requests library**: Già presente in `requirements.txt`
3. **GitHub Personal Access Token** con i seguenti permessi:
   - `repo` (full control of private repositories)
   - `admin:org` (full control of orgs and teams, read and write org projects)

### Configurazione

#### 1. Creare un GitHub Personal Access Token

1. Vai su GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Clicca "Generate new token (classic)"
3. Seleziona i seguenti permessi:
   - ✅ `repo` (tutte le opzioni sotto repo)
   - ✅ `admin:org` (almeno `write:org` e `read:org`)
4. Genera il token e copialo

#### 2. Configurare il Token

Imposta il token come variabile d'ambiente:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

Oppure aggiungi al file `.env`:

```
GITHUB_TOKEN=ghp_your_token_here
```

E carica con:

```bash
source .env
```

### Utilizzo

#### Modalità Dry-Run (Simulazione)

Consigliato per la prima esecuzione per verificare il funzionamento senza effettuare modifiche:

```bash
python3 scripts/add_collaborators.py --dry-run
```

#### Modalità Normale (Esecuzione Reale)

```bash
python3 scripts/add_collaborators.py
```

### Output di Esempio

```
============================================================
MODALITÀ DRY-RUN: Nessuna modifica sarà effettuata
============================================================
2025-12-12 19:00:00 - INFO - Avvio automazione aggiunta collaboratori per hannesmitterer/euystacio-helmi-AI
2025-12-12 19:00:00 - INFO - Collaboratori da processare: 6

--- Fase 1: Verifica Collaboratori Attuali ---
2025-12-12 19:00:01 - INFO - Collaboratori attuali: 3

--- Fase 2: Verifica Esistenza Utenti ---
2025-12-12 19:00:02 - INFO - ✓ Utente 'alfredmitterer' trovato su GitHub
2025-12-12 19:00:02 - INFO - ✓ Utente 'sensisara81' trovato su GitHub
2025-12-12 19:00:03 - INFO - ⊕ 'dietmarzuegg' è già un collaboratore
2025-12-12 19:00:03 - INFO - ✓ Utente 'claudiocalabrese' trovato su GitHub
2025-12-12 19:00:04 - INFO - ✓ Utente 'consultantlaquila' trovato su GitHub
2025-12-12 19:00:04 - WARNING - ✗ Utente 'bioarchitettura-rivista' non trovato su GitHub

--- Fase 3: Aggiunta Nuovi Collaboratori ---
2025-12-12 19:00:05 - INFO - [DRY-RUN] Simulazione aggiunta 'alfredmitterer' con permessi 'push'
2025-12-12 19:00:05 - INFO - [DRY-RUN] Simulazione aggiunta 'sensisara81' con permessi 'push'
2025-12-12 19:00:06 - INFO - [DRY-RUN] Simulazione aggiunta 'claudiocalabrese' con permessi 'push'
2025-12-12 19:00:06 - INFO - [DRY-RUN] Simulazione aggiunta 'consultantlaquila' con permessi 'push'

============================================================
RIEPILOGO OPERAZIONI
============================================================
Già collaboratori:    1
Aggiunti con successo: 4
Falliti:              0
Saltati (non trovati): 1
============================================================
```

### Gestione Errori

Lo script gestisce automaticamente i seguenti scenari di errore:

1. **Token Mancante**: Esce con messaggio chiaro se `GITHUB_TOKEN` non è configurato
2. **Permessi Insufficienti**: Segnala se il token non ha i permessi necessari
3. **Utente Non Trovato**: Salta utenti con username GitHub non validi
4. **Utente Già Collaboratore**: Rileva e salta utenti già aggiunti
5. **Errori di Rete**: Gestisce timeout e problemi di connessione
6. **Rate Limiting**: Rispetta i limiti API di GitHub

### Personalizzazione

Per modificare la lista dei collaboratori, edita la costante `COUNCIL_COLLABORATORS` nel file `scripts/add_collaborators.py`:

```python
COUNCIL_COLLABORATORS = [
    "username1",
    "username2",
    # aggiungi altri username qui
]
```

Per modificare il livello di permessi (default: "push" = Write), modifica:

```python
COLLABORATOR_PERMISSION = "push"  # Opzioni: "pull", "push", "admin", "maintain", "triage"
```

### Sicurezza

⚠️ **IMPORTANTE**: 

- **NON** committare mai il GITHUB_TOKEN nel repository
- Usa sempre variabili d'ambiente o file `.env` (che è in `.gitignore`)
- Rigenera il token se accidentalmente esposto
- Il token ha accesso completo al repository - conservalo in modo sicuro

### Troubleshooting

#### Errore "Bad credentials"
- Verifica che il token sia corretto e non scaduto
- Assicurati che il token abbia i permessi necessari

#### Errore "Not Found" per un utente
- Verifica che l'username GitHub sia corretto (case-sensitive)
- L'utente potrebbe aver cambiato username

#### Errore 403 "Forbidden"
- Il token non ha i permessi necessari
- Rigenera il token con i permessi `repo` e `admin:org`

#### Utenti non ricevono l'invito
- Controlla la sezione "Invitations" nelle impostazioni del repository
- Gli utenti devono accettare l'invito per diventare collaboratori attivi

### Riferimenti

- [GitHub REST API - Collaborators](https://docs.github.com/en/rest/collaborators)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Repository Permissions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-teams-and-people-with-access-to-your-repository)
