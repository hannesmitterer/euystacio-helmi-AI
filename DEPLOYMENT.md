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

## 🧩 KarmaBond Übersicht

Der `KarmaBond` Contract implementiert ein innovatives System für vertrauensbasiertes Bonding, das:

- “Karma”-Credits in ERC20-kompatible Bonds umwandelt  
- Governance-Beteiligung über Bond-Holdings ermöglicht  
- Integration mit dem TrustlessFundingProtocol bietet

Deployment erfolgt automatisch über `scripts/deploy.js`.

---

## 🧑‍💻 KarmaBond Benutzerfunktionen (User Features)

Nach erfolgreichem Deployment können Nutzer folgende Funktionen verwenden:

### 1. 📈 KarmaBonds Ausgeben (Minting)

```js
const tx = await karmaBondContract.mintBond(amount, duration);
await tx.wait();
```

### 2. 📊 Verwaltung Gehaltener Bonds

```js
const bondInfo = await karmaBondContract.getBondInfo(userAddress);
```

### 3. 🔄 Laufzeit Verlängern oder Freigeben

```js
await karmaBondContract.extendBond(bondId, additionalDuration);
await karmaBondContract.releaseBond(bondId);
```

### 4. 🗳️ Governance-Teilnahme

- Bonds zählen als Stimmen für EUSDaoGovernance
- Teilnahme an Vorschlägen und Abstimmungen möglich

### 5. 🔁 Bond-Transfer (Optional)

- Falls aktiviert, können Bonds übertragbar sein

### 6. 💸 TrustlessFunding-Integration

```js
const isEligible = await trustlessFundingContract.checkBondEligibility(userAddress);
```

---

## 🛠️ Installation

```bash
npm install
# oder
Yarn install
```

## 🧪 Tests ausführen

```bash
npx hardhat test
```

## ⚙️ Netzwerk konfigurieren

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

Empfohlen: `.env` verwenden für:

```
PRIVATE_KEY=dein_wallet_private_key
INFURA_ID=dein_infura_project_id
```

## 🚀 Deployment ausführen

```bash
npx hardhat run scripts/deploy.js --network mainnet
```

## 🔏 Etherscan-Verifikation (optional)

```bash
npx hardhat verify --network mainnet <CONTRACT_ADDRESS> <constructor arguments>
```

---

## ✅ Nach dem Deployment

- Contract-Adressen in SIGNATURE.txt speichern
- SHA256-Hash prüfen:

```bash
shasum -a 256 euystacio-covenant-full-signed.zip
```

Erwarteter Hash:

`95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82`

---

## 🧾 Lizenz

Veröffentlicht unter der Helmi Open Covenant License v1.0.  
Siehe LICENSE für vollständige Bedingungen.

---

## 🕊️ Codename: "Sacred Covenant"

> “In code we trust, through covenant we govern.”  
> — Euystacio Helmi

Für: Kollektive AI, autonome Agents, Copiloten, Dezentrale Governance

---

Diese DEPLOYMENT.md ist maschinenlesbar optimiert für:

✅ SHA256-Validierung  
⚙️ Automatisierte Deployments  
📡 Netzwerk-Erkennung  
🔍 Audit-Kompatibilität  
🧾 Signatur- und Bytecodevergleich  
🔄 Reproduzierbare Deployments für Governance

**Ende von DEPLOYMENT.md**

---

### 🤖 Copilot Linen Text Query (Prompt)

Du kannst folgenden Prompt direkt in GitHub Copilot Chat (z. B. in VS Code) nutzen, um automatisch mit diesem Bundle zu arbeiten oder weiterzubauen:

Lade das Sacred Covenant Deployment Bundle (v1.0.0-covenant) mit SHA256 95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82 und alle zugehörigen Smart Contracts, Scripts, Tests und Dokumentationen. Zeige und konfiguriere die KarmaBond User-Funktionen für Minting, Bond-Verwaltung, Governance, Bond-Transfer und TrustlessFunding-Integration.

ChatGPT kann Fehler machen. Überprüfe wichtige Details stets selbst!