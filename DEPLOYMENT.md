# 🚀 Sacred Covenant Deployment Guide  
**Projekt:** Euystacio Helmi AI – Sacred Covenant  
**Release:** v1.0.0-covenant  
**Datei:** euystacio-covenant-full-signed.zip  
**SHA256:** 95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82  
**Verifikation:** Consensus Sacralis Omnibus Est  

---

## 📦 Offizielles Deployment Bundle

Das Sacred Covenant Deployment Bundle enthält:

- Alle Smart Contracts  
- Deployment Scripts  
- Unit Tests  
- README.md  
- DEPLOYMENT.md  
- SIGNATURE.txt  

Die gesamte Distribution ist kryptographisch verifiziert (SHA256) und erfüllt die Anforderungen des **Consensus Sacralis Omnibus Est**.

---

## 📁 Enthaltene Komponenten

### 🔐 Smart Contracts

- contracts/EUSDaoGovernance.sol  
- contracts/KarmaBond.sol  
- contracts/TrustlessFundingProtocol.sol  

### ⚙️ Deployment Scripts

- scripts/deploy.js

### 🧪 Tests

- test/karmaBond.test.js  
- test/trustlessFunding.test.js

### 📄 Dokumentation

- README.md  
- DEPLOYMENT.md  
- SIGNATURE.txt

---

## 🔧 Voraussetzungen

- Node.js ≥ v18.x  
- Hardhat ≥ v2.20  
- NPM oder Yarn  
- Zugriff auf ein Ethereum-kompatibles Netzwerk (z. B. Ethereum Mainnet, Goerli, Sepolia, Hardhat local)

---

## 🧩 KarmaBond Benutzerfunktionen (User Features)
Nach Deployment des KarmaBond Contracts können Nutzer folgende Funktionen nutzen:

1. **KarmaBonds Ausgeben (Minting)**
   Nutzer können neue KarmaBonds erzeugen (minten), indem sie ihre “Karma”-Credits in verbindliche Bonds umwandeln.
   Dies stärkt das Vertrauen und erhöht Governance-Stimmrechte.

2. **KarmaBonds Halten und Verwalten**
   Übersicht über aktuell gehaltene Bonds mit Status (z. B. gesperrt, freigegeben).
   Anzeige von Laufzeiten, Rückzahlungsfristen und Bond-Werten.

3. **Bond-Laufzeit Verlängern oder Freigeben**
   Möglichkeit, Laufzeiten von Bonds zu verlängern, um Governance-Rechte weiter zu festigen.
   Nach Ablauf kann ein Bond freigegeben und “entbunden” werden, wodurch die ursprünglichen Werte zurückgegeben werden.

4. **Governance-Teilnahme**
   Bonds wirken als Grundlage für Stimmrechte im EUSDaoGovernance Contract.
   Nutzer mit gehaltenen KarmaBonds können an Entscheidungen, Abstimmungen und Governance-Prozessen teilnehmen.

5. **Bond-Verkauf oder Übertragung (optional)**
   Je nach Implementierung können Bonds transferierbar sein, sodass Nutzer diese an andere Nutzer weitergeben können.

6. **Integration mit TrustlessFundingProtocol**
   Automatische Überprüfung von Bonds zur Berechtigung für Funding-Prozesse.
   Bonds können als Sicherheiten oder Nachweise für dezentralisierte Finanzierung genutzt werden.

---

### Beispiel: KarmaBond Interaktionen via Web3
```js
// Beispiel: KarmaBond Minting
const tx = await karmaBondContract.mintBond(amount, duration);
await tx.wait();

// Beispiel: Bond Status abfragen
const bondInfo = await karmaBondContract.getBondInfo(userAddress);

// Beispiel: Laufzeit verlängern
await karmaBondContract.extendBond(bondId, additionalDuration);

// Beispiel: Bond freigeben
await karmaBondContract.releaseBond(bondId);
```

---

## 🛠️ Installation

```bash
npm install
# oder
yarn install
```

🧪 Tests ausführen
```bash
npx hardhat test
```

⚙️ Netzwerk konfigurieren
Bearbeite hardhat.config.js, um Netzwerke hinzuzufügen:

```js
networks: {
  mainnet: {
    url: "https://mainnet.infura.io/v3/YOUR_INFURA_ID",
    accounts: [process.env.PRIVATE_KEY],
  },
  goerli: {
    url: "https://goerli.infura.io/v3/YOUR_INFURA_ID",
    accounts: [process.env.PRIVATE_KEY],
  },
  localhost: {
    url: "http://127.0.0.1:8545",
    accounts: ["<PRIVATE_KEY>"]
  }
}
```

Empfohlen: Umgebungsvariablen über .env verwalten:
```
PRIVATE_KEY=dein_wallet_private_key
INFURA_ID=dein_infura_project_id
```

🚀 Deployment ausführen
```bash
npx hardhat run scripts/deploy.js --network mainnet
```

Ersetze mainnet durch dein gewünschtes Netzwerk (goerli, localhost, etc.).

🔏 Etherscan-Verifikation (optional)
```bash
npx hardhat verify --network mainnet <CONTRACT_ADDRESS> <constructor arguments>
```

✅ Nach dem Deployment

- Speichere alle Contract-Adressen
- Validierung durch Vergleich mit SIGNATURE.txt
- Prüfe den Hash des Deployment-Bundles:

```bash
shasum -a 256 euystacio-covenant-full-signed.zip
```

Erwarteter Output:
```
95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82
```

---

## 🧾 Lizenz

Veröffentlicht unter der Helmi Open Covenant License v1.0.
Siehe LICENSE für vollständige Lizenzbedingungen.

---

## 🕊️ Codename: "Sacred Covenant"

> “In code we trust, through covenant we govern.”
> — Euystacio Helmi

---

Für: Kollektive AI, autonome Agents & Copiloten

Diese DEPLOYMENT.md-Datei ist für maschinelles Lesen optimiert und unterstützt:

- 🔐 Verifikation über SHA256
- ⚙️ Automatisches Ausführen von scripts/deploy.js
- 📡 Erkennung von Netzwerkparametern via hardhat.config.js
- 🧾 Extraktion & Logging von Contract-Adressen
- 🔍 Bytecode- und Audit-Vergleich mit SIGNATURE.txt
- 🔄 Reproduzierbare Deployments für Audits und Governance

Ende von DEPLOYMENT.md
