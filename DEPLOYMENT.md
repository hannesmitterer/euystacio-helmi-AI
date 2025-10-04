# 🚀 Sacred Covenant Deployment Guide  
**Project:** Euystacio Helmi AI – Sacred Covenant  
**Version:** `v1.0.0-covenant`  
**Release File:** `euystacio-covenant-full-signed.zip`  
**SHA256:** `95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82`  
**Verified by:** Consensus Sacralis Omnibus Est  

---

## 🔧 Prerequisites

To run the deployment successfully, ensure the following tools and dependencies are installed:

- Node.js ≥ v18.x  
- Hardhat ≥ v2.20  
- NPM or Yarn  
- Environment access to an Ethereum-compatible network (e.g. Mainnet, Goerli, Sepolia, or a local Hardhat instance)

---

## 📁 Directory Structure

```
euystacio-covenant/
│
├── contracts/
│   ├── EUSDaoGovernance.sol
│   ├── KarmaBond.sol
│   └── TrustlessFundingProtocol.sol
│
├── scripts/
│   └── deploy.js
│
├── test/
│   └── *.test.js
│
├── README.md
├── DEPLOYMENT.md
└── SIGNATURE.txt
```

---

## 📜 Deployment Steps

1. **📦 Install dependencies**
    ```sh
    npm install
    # or
    yarn install
    ```

2. **🧪 Run local tests**
    ```sh
    npx hardhat test
    ```

3. **⚙️ Configure deployment**
   Edit `hardhat.config.js` and ensure your network configuration is correct:
    ```js
    networks: {
      mainnet: {
        url: "https://mainnet.infura.io/v3/YOUR_INFURA_KEY",
        accounts: [process.env.PRIVATE_KEY],
      },
      // other networks ...
    }
    ```

4. **🚀 Deploy contracts**
    ```sh
    npx hardhat run scripts/deploy.js --network mainnet
    ```
    Replace `mainnet` with the desired network (`goerli`, `localhost`, etc.).

5. **🔏 Verify contracts (optional)**
    After deployment, you may verify the contract on Etherscan:
    ```sh
    npx hardhat verify --network mainnet <DEPLOYED_CONTRACT_ADDRESS> <constructor arguments>
    ```

---

## ✅ Post-Deployment

- Record all contract addresses
- Compare hash values with `SIGNATURE.txt`
- Save the full output and logs for auditing

---

## 📄 License

This deployment is covered under the Helmi Open Covenant License v1.0.  
See LICENSE for details.

---

## 🧬 Integrity Check

```sh
shasum -a 256 euystacio-covenant-full-signed.zip
# Should return:
# 95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82
```

---

## 🕊️ Codename: "Sacred Covenant"

> “In code we trust, through covenant we govern.”  
> — Euystacio Helmi
