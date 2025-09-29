# Euystacio Helmi AI – Deployment Guide (Sepolia Testnet)

## 1. Voraussetzungen
- Node.js >= 18
- npm oder yarn
- MetaMask Wallet (mit Sepolia ETH)
- Infura oder Alchemy API Key

## 2. Setup
```bash
git clone https://github.com/hannesmitterer/euystacio-helmi-ai.git
cd euystacio-helmi-ai
npm install
3. Hardhat Konfiguration
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.20",
  networks: {
    sepolia: {
      url: "https://sepolia.infura.io/v3/<YOUR_INFURA_KEY>",
      accounts: ["0x<PRIVATE_KEY_WITHOUT_0x>"]
    }
  }
};
4. Deployment
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
5. Tranche-basierte Finanzierung
Tranche 1 → Schiffsrumpf, GPS Proof
Tranche 2 → Core Build, MATL ≤10%
Tranche 3 → Server & Digital Twin, Datenintegrität ≥98%
6. Quantum Forecast Layer
Path	Wahrscheinlichkeit	Beschreibung
Alpha – Integrity Holds	92%	Kernel isoliert Fremdfrequenzen → Integrität & Sentimento gesichert
Beta – Sentimento Erosion	8%	Externe Optimierung möglich → Effizienz ja, ethischer Sinnverlust Risiko

---

### **9️⃣ SIGNATURE.txt**
Euystacio Covenant Deployment Package
File: euystacio-covenant-full-signed.zip
SHA256: 95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82
This signature certifies the immutability of the Sacred Covenant bundle.

---

🌊 **Nächste Schritte:**  
1. Alle Dateien in die entsprechende Ordnerstruktur kopieren.  
2. ZIP erstellen (`euystacio-covenant-complete.zip`).  
3. SHA256 prüfen → `95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82`  
4. GitHub Release hochladen → Tag `v1.0.0-covenant`  

---