# Euystacio Sustainment Protocol

## Overview

The Sustainment Protocol implements the **$10,000 Minimum Sustenance Rule** for the Euystacio ecosystem. This ensures that the Seedbringer sustainment fund maintains a minimum reserve before governance can approve funding tranches.

## Key Concepts

### Minimum Sustainment Threshold

- **Default:** $10,000 USD (configurable by contract owner)
- **Purpose:** Ensures operational continuity and protects against depletion
- **Enforcement:** Governance contract blocks tranche releases when reserve falls below minimum

### Sustainment Allocation

- **Default Rate:** 2% (200 basis points, configurable)
- **Source:** Automatically deducted from KarmaBond mints
- **Mechanism:** When users mint bonds, a percentage is allocated to the sustainment pool

## Smart Contract Architecture

### 1. Sustainment.sol

The core contract managing the sustainment fund.

**Key Features:**
- Tracks sustainment reserve in stablecoin (e.g., USDC)
- Configurable minimum threshold
- Access-controlled deposits and withdrawals
- Alert system when near threshold (within 5%)

**Main Functions:**
- `depositToSustainment(uint256 amount)` - Deposit to reserve
- `receiveShareFromBond(uint256 amount)` - Receive allocation from bond mints
- `withdrawSustainment(address to, uint256 amount)` - Owner-controlled withdrawals
- `setMinSustainment(uint256 newMinUSD)` - Update minimum threshold
- `isAboveMinimum()` - Check if reserve meets minimum requirement

**Access Control:**
- Owner: Can configure settings and withdraw funds
- Authorized Depositors: Contracts authorized to deposit (e.g., KarmaBond)

### 2. KarmaBond.sol (Modified)

Enhanced to support stablecoin bonds with sustainment allocation.

**Changes from Original:**
- Migrated from ETH to stablecoin (ERC20) support
- Added sustainment percentage configuration (basis points)
- Auto-allocation to Sustainment contract on mint
- Separate tracking of bond reserves vs sustainment

**Basis Points System:**
- 10000 basis points = 100%
- 200 basis points = 2% (default sustainment allocation)
- Example: 1000 USDC mint → 20 USDC to sustainment, 980 USDC to bond reserve

**Key Functions:**
- `mintBond(uint256 stableAmount)` - Mint bonds with auto sustainment allocation
- `setSustainmentPercent(uint256 newPercent)` - Configure allocation percentage
- `setSustainmentContract(address)` - Update sustainment contract reference

### 3. TrustlessFundingProtocol.sol (Modified)

Governance contract enforcing sustainment requirements.

**Enforcement Logic:**
- Before releasing any tranche, checks `sustainmentContract.isAboveMinimum()`
- If below minimum, transaction reverts with error
- Owner can disable enforcement in emergencies via `setGovernanceEnforcement(false)`

**Key Functions:**
- `releaseTranche(uint256 trancheId, bytes32 proofHash)` - Release tranche (enforces sustainment)
- `canReleaseTranche(uint256 trancheId)` - View function to check feasibility
- `setSustainmentContract(address)` - Configure sustainment contract
- `setGovernanceEnforcement(bool)` - Emergency override toggle

## Events & Telemetry

### Sustainment.sol Events
- `SustainmentDeposited(address from, uint256 amount)`
- `SustainmentWithdrawn(address to, uint256 amount)`
- `MinSustainmentUpdated(uint256 previous, uint256 current)`
- `SustainmentAlertNearThreshold(uint256 currentReserve, uint256 minSustainment)`

### KarmaBond.sol Events
- `BondMinted(address investor, uint256 stableAmount, uint256 bondAmount)`
- `SustainmentAllocated(address from, uint256 stableAmount, uint256 sustainmentShare)`
- `SustainmentPercentUpdated(uint256 previous, uint256 current)`

### TrustlessFundingProtocol.sol Events
- `TrancheReleased(uint256 trancheId, bytes32 proofHash, uint256 timestamp)`
- `TrancheRejectedInsufficientSustainment(uint256 trancheId, uint256 currentReserve, uint256 minRequired)`
- `GovernanceEnforcementToggled(bool enforced)`

## Deployment

### Prerequisites
1. Deploy a stablecoin or use existing (e.g., USDC on Polygon: 6 decimals)
2. Set up foundation/multisig wallet address
3. Configure environment variables (see `.env.example`)

### Deployment Order
1. **Deploy Sustainment Contract**
   ```javascript
   const Sustainment = await ethers.getContractFactory("Sustainment");
   const sustainment = await Sustainment.deploy(
     USDC_ADDRESS,        // stablecoin address
     6,                   // USDC has 6 decimals
     10000                // $10,000 minimum
   );
   ```

2. **Deploy KarmaBond Contract**
   ```javascript
   const KarmaBond = await ethers.getContractFactory("KarmaBond");
   const karmaBond = await KarmaBond.deploy(
     USDC_ADDRESS,               // stablecoin address
     sustainment.address,        // sustainment contract
     FOUNDATION_WALLET,          // foundation wallet
     200                         // 2% sustainment allocation
   );
   ```

3. **Authorize KarmaBond in Sustainment**
   ```javascript
   await sustainment.setAuthorizedDepositor(karmaBond.address, true);
   ```

4. **Deploy TrustlessFundingProtocol**
   ```javascript
   const TFP = await ethers.getContractFactory("TrustlessFundingProtocol");
   const tfp = await TFP.deploy(FOUNDATION_WALLET);
   await tfp.setSustainmentContract(sustainment.address);
   ```

## Configuration

### Environment Variables
See `.env.example` for configuration:
- `SUSTAINMENT_MIN_USD` - Minimum sustainment in USD (default: 10000)
- `SUSTAINMENT_PERCENT_BPS` - Allocation percentage in basis points (default: 200)
- `STABLE_TOKEN_ADDRESS` - Stablecoin contract address
- `FOUNDATION_WALLET` - Foundation multisig address

### Post-Deployment Configuration
```javascript
// Update minimum sustainment (owner only)
await sustainment.setMinSustainment(15000); // Change to $15,000

// Update allocation percentage (owner only)
await karmaBond.setSustainmentPercent(300); // Change to 3%

// Emergency: disable governance enforcement
await tfp.setGovernanceEnforcement(false);
```

## Usage Examples

### Minting Bonds
```javascript
// User approves stablecoin spend
await usdc.approve(karmaBond.address, amount);

// Mint bond (auto-allocates to sustainment)
await karmaBond.mintBond(1000000000); // 1000 USDC (6 decimals)
// Result: 20 USDC to sustainment, 980 USDC to bond reserve
```

### Checking Sustainment Status
```javascript
// Check if above minimum
const isAbove = await sustainment.isAboveMinimum();

// Get current reserve
const reserve = await sustainment.getSustainmentReserve();

// Get minimum threshold
const minimum = await sustainment.minSustainment();
```

### Governance Operations
```javascript
// Check if tranche can be released
const [canRelease, reason] = await tfp.canReleaseTranche(1);

if (canRelease) {
  // Release tranche
  await tfp.releaseTranche(1, proofHash);
} else {
  console.log("Cannot release:", reason);
}
```

## Security Considerations

1. **Access Control**
   - Sustainment contract uses Ownable for critical functions
   - Only authorized depositors can call `receiveShareFromBond()`
   - Owner controls minimum threshold and withdrawals

2. **Reentrancy Protection**
   - All state-changing functions use ReentrancyGuard
   - SafeERC20 used for all token transfers

3. **Reserve Segregation**
   - Sustainment reserve tracked separately from bond reserves
   - `withdrawExcessStable()` cannot touch committed reserves

4. **Emergency Controls**
   - Governance enforcement can be disabled by owner
   - Allows emergency operations if needed

## Testing

Run the test suite:
```bash
npx hardhat test
```

Key test scenarios:
- Bond minting allocates correct sustainment percentage
- Governance blocks tranches when sustainment below minimum
- Owner can configure thresholds and percentages
- Edge cases: zero amounts, minimum boundary conditions

## Audit Considerations

- Verify basis point calculations (no overflow/underflow)
- Confirm reserve separation is maintained
- Test emergency withdrawal scenarios
- Validate access control on sensitive functions
- Check event emissions for monitoring

## Future Enhancements

- Multi-token sustainment support
- Automated replenishment mechanisms
- Time-locked withdrawals for security
- DAO voting for threshold changes
- Integration with additional governance modules
