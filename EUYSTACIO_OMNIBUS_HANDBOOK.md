# Euystacio Helmi AI – Complete Omnibus Handbook (English)

## 1. Introduction & Architecture

Euystacio Helmi AI is an ethically secured platform combining:

- **Smart Contracts:** `EUSDaoGovernance.sol`, `KarmaBond.sol`, `TrustlessFundingProtocol.sol`
- **Tranche Releases:** Automated and cryptographically secured
- **Live Dashboard:** Real-time investment visualization and ethics monitoring
- **KarmaBond Investments:** Ethical investment instruments based on virtue, transparency, and measurable impact

The system ensures ethical integrity, transparency, and real-time monitoring for all stakeholders.

---

## 2. Deploy & Tranche Management

The Master Control Script automates deployment:

- Deploys EUSDaoGovernance contract for DAO and token management
- Deploys KarmaBond contract for investor participation
- Deploys TrustlessFundingProtocol for automated tranche releases
- Sets up event listeners:
    - `TrancheReleased`: Updates dashboard on tranche status
    - `InvestmentMade`: Updates dashboard with new investment

Tranche releases are secured via SHA256 proofs. Violations of ethical invariants automatically block release, ensuring integrity.

**Tranches Overview:**

| Tranche | Purpose                                 | Proof Required            |
| ------- | --------------------------------------- | ------------------------ |
| 1       | Seed Funding – exterritorial hull purchase | GPS proof                |
| 2       | Core Build – Wind & Solar systems       | MATL ≤10% in test         |
| 3       | Activation – Digital Twin, Servers      | TC ≥ 98% data integrity   |

---

## 3. Live Dashboard

The dashboard provides:

- **Tranche Status:** Visual indicator for each tranche (Pending, Released)
- **KarmaBond Investments:** Real-time bar chart (USD, EC, m³ water)
- **Scorecard:** Tabular data showing total investments, impact metrics
- **Ethics Check:** MATL ≤10%, R1 ≥45%, automatically flags violations
- **SHA256 Verification:** Ensures contract integrity
- **Updates:** Via WebSocket events, no manual polling needed.

---

## 4. Investors Guide – Step by Step

**Step 1: Connect Wallet**
- Use MetaMask (or compatible wallet)
- Ensure you are connected to Sepolia Testnet
- Example wallet: `0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b`

**Step 2: Purchase KarmaBonds**
- Navigate to Dashboard → Investments
- Enter amount in USD or EC
- Smart contract automatically calculates m³ water impact:
    - Example: 1000 USD → 500 m³ water, 2% MATL improvement
- Confirm transaction in wallet

**Step 3: Verify Transaction**
- On success, dashboard updates Scorecard and KarmaBond Chart
- Check event logs:
    - `InvestmentMade(investor, amount)`
- Automatically updates JSON for front-end visualization

**Step 4: Monitoring Tranches**
- Dashboard shows each tranche’s status
- SHA256 Proof ensures the integrity of milestone data
- If an ethical invariant is violated, tranche release is blocked, and an alert appears on the dashboard

**Step 5: Redeem / Participate in Voting**
- KarmaBond tokens may confer:
    - Voting rights in DAO (via EUS Governance)
    - Allocation or redistribution based on ethical performance

---

## 5. Technical Details

- **Smart Contracts:** Open source on GitHub ([hannesmitterer/euystacio-helmi-ai](https://github.com/hannesmitterer/euystacio-helmi-ai))
- **Master Control Script:** Automates deploy, listens for events, updates dashboard JSON files
- **Dashboard:** HTML + JS + Chart.js; real-time WebSocket integration
- **Hardhat:** Testnet deploy, contract verification, and event emission

---

## 6. Workflow Diagram

```
[Investors] -> [KarmaBond Investments] -> [TrustlessFundingProtocol.sol] -> [Master Control Script]
      |
      v
[Tranche Release] -> [EUSDaoGovernance.sol]
      |
      v
[Live Dashboard]
  - Scorecard
  - Tranche Status
  - KarmaBond Chart
  - Ethics Check
  - SHA256
```
**Flows:** Investments -> Smart Contracts -> Tranche Release -> Dashboard  
**Real-time:** Hardhat events stream automatically to dashboard  
**Ethics check:** automated on MATL/R1, affects tranche release

---

## 7. Best Practices for Investors

- Always check ETH/ERC balances before investing
- Verify SHA256 hashes on dashboard to confirm contract integrity
- Prefer incremental investments to monitor real-time impact metrics
- Engage in DAO governance via EUS tokens to safeguard ethical invariants