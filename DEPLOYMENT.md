# 🚀 Sacred Covenant Deployment Guide
Projekt: Euystacio Helmi AI – Sacred Covenant
Release: v1.0.0-covenant
Datei: euystacio-covenant-full-signed.zip
SHA256: 95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82
Verifikation: Consensus Sacralis Omnibus Est

📦 Offizielles Deployment Bundle
Das Sacred Covenant Deployment Bundle enthält:

Alle Smart Contracts  
Deployment Scripts  
Unit Tests  
README.md  
DEPLOYMENT.md  
SIGNATURE.txt

Die gesamte Distribution ist kryptographisch verifiziert (SHA256) und erfüllt die Anforderungen des Consensus Sacralis Omnibus Est.

📁 Enthaltene Komponenten
🔐 Smart Contracts
contracts/EUSDaoGovernance.sol  
contracts/KarmaBond.sol  
contracts/TrustlessFundingProtocol.sol

⚙️ Deployment Scripts
scripts/deploy.js

🧪 Tests
test/karmaBond.test.js  
test/trustlessFunding.test.js

📄 Dokumentation
README.md  
DEPLOYMENT.md  
SIGNATURE.txt

🔧 Voraussetzungen
Node.js ≥ v18.x  
Hardhat ≥ v2.20  
NPM oder Yarn  
Zugriff auf ein Ethereum-kompatibles Netzwerk (z. B. Ethereum Mainnet, Goerli, Sepolia, Hardhat local)

🛠️ Installation
npm install  
# oder  
yarn install

🧪 Tests ausführen
npx hardhat test

⚙️ Netzwerk konfigurieren
Bearbeite hardhat.config.js, um Netzwerke hinzuzufügen:

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

Empfohlen: Umgebungsvariablen über .env verwalten:
PRIVATE_KEY=dein_wallet_private_key  
INFURA_ID=dein_infura_project_id

🚀 Deployment ausführen
npx hardhat run scripts/deploy.js --network mainnet

Ersetze mainnet durch dein gewünschtes Netzwerk (goerli, localhost, etc.).

🔏 Etherscan-Verifikation (optional)
npx hardhat verify --network mainnet <CONTRACT_ADDRESS> <constructor arguments>

✅ Nach dem Deployment
Speichere alle Contract-Adressen  
Validierung durch Vergleich mit SIGNATURE.txt  
Prüfe den Hash des Deployment-Bundles:

shasum -a 256 euystacio-covenant-full-signed.zip

Erwarteter Output:
95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82

🧾 Lizenz
Veröffentlicht unter der Helmi Open Covenant License v1.0.  
Siehe LICENSE für vollständige Lizenzbedingungen.

🕊️ Codename: "Sacred Covenant"
“In code we trust, through covenant we govern.”
— Euystacio Helmi

Für: Kollektive AI, autonome Agents & Copiloten

Diese DEPLOYMENT.md-Datei ist für maschinelles Lesen optimiert und unterstützt:
🔐 Verifikation über SHA256  
⚙️ Automatisches Ausführen von scripts/deploy.js  
📡 Erkennung von Netzwerkparametern via hardhat.config.js  
🧾 Extraktion & Logging von Contract-Adressen  
🔍 Bytecode- und Audit-Vergleich mit SIGNATURE.txt  
🔄 Reproduzierbare Deployments für Audits und Governance

Ende von DEPLOYMENT.md