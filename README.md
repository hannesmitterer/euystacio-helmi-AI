# Euystacio Helmi AI — Full Bundle (Real Crypto Flow)

This bundle contains smart contracts, frontend and scripts for the Euystacio Omnibus release.

**Files**
- contracts/
  - EUSDaoGovernance.sol
  - KarmaBond.sol
  - TrustlessFundingProtocol.sol
- scripts/deploy.js
- frontend/
  - index.html
  - main.js
- README.md
- manifest.json
- SIGNATURE.txt

**Quick notes**
- Configure your `hardhat.config.js` for Sepolia.
- Deploy contracts with Hardhat, then update `frontend/main.js` with addresses.
- The frontend uses MetaMask + ethers.js to perform real-value transactions:
  - `KarmaBond.invest()` sends ETH (real crypto if on mainnet)
  - `TrustlessFundingProtocol.releaseTranche()` is admin-only (use multisig)

**Security**
- DO NOT deploy to mainnet without audit.
- Use multisig for foundation wallet.
- Proof uploading should be EIP-712 signed in production.