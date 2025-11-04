# Euystacio Smart Contracts

This directory contains the core smart contracts for the Euystacio ecosystem with integrated Sustainment Protocol.

## Contracts

### Core Protocol Contracts

#### Sustainment.sol
Manages the Seedbringer sustainment fund with a configurable $10,000 minimum threshold.

**Key Features:**
- Tracks sustainment reserve in stablecoins (e.g., USDC)
- Enforces minimum threshold before governance operations
- Access-controlled deposits and withdrawals
- Telemetry events for monitoring

**Deployment:** Deploy first, then configure other contracts to reference it

#### KarmaBond.sol
Bond issuance and redemption system with automatic sustainment allocation.

**Key Features:**
- Stablecoin-based bonds (USDC, USDT, etc.)
- Configurable sustainment allocation (default: 2%)
- Invariant-based redemption logic
- Integrated with Sustainment contract

**Changes from v1:** Migrated from ETH to ERC20 stablecoins, added sustainment integration

#### TrustlessFundingProtocol.sol
Governance contract for approving funding tranches with sustainment enforcement.

**Key Features:**
- Proof-based tranche release
- Sustainment minimum enforcement
- Emergency override capability
- Integration with Sustainment contract

**Changes from v1:** Added sustainment checks and emergency controls

#### EUSDaoGovernance.sol
Stewardship token contract for DAO governance.

**Features:**
- ERC20 token (EUS)
- Contribution score weighting
- Voting power calculation

### Test Utilities

#### MockERC20.sol
Mock ERC20 token for testing purposes. Simulates stablecoins like USDC with configurable decimals.

## Architecture

```
┌─────────────────┐
│   Governance    │
│  (EUSDaoGov)    │
└────────┬────────┘
         │
         v
┌─────────────────────────┐      ┌──────────────────┐
│ TrustlessFundingProtocol│─────>│   Sustainment    │
│  (Tranche Approval)     │      │  (Reserve Fund)  │
└─────────────────────────┘      └────────▲─────────┘
                                          │
                                          │ 2% allocation
                                          │
                                 ┌────────┴─────────┐
                                 │    KarmaBond     │
                                 │ (Bond Issuance)  │
                                 └──────────────────┘
```

## Deployment Order

1. **Deploy Sustainment**
   ```bash
   # Configure in .env:
   # STABLE_TOKEN_ADDRESS=0x... (USDC address)
   # SUSTAINMENT_MIN_USD=10000
   # SUSTAINMENT_PERCENT_BPS=200
   ```

2. **Deploy KarmaBond** with Sustainment address

3. **Authorize KarmaBond** as depositor in Sustainment

4. **Deploy TrustlessFundingProtocol** and link to Sustainment

5. **Deploy EUSDaoGovernance** (optional, independent)

See `scripts/deploy_karmabond.js` for complete deployment flow.

## Testing

Run the full test suite:
```bash
npm test
```

Run specific test suites:
```bash
npm run test:sustainment      # Sustainment contract tests
npm run test:integration       # KarmaBond integration tests
npm run test:governance        # Governance enforcement tests
```

## Configuration

Environment variables (see `.env.example`):
- `STABLE_TOKEN_ADDRESS` - Stablecoin contract address (e.g., USDC)
- `FOUNDATION_WALLET` - Foundation/multisig wallet address
- `SUSTAINMENT_MIN_USD` - Minimum sustainment in USD (default: 10000)
- `SUSTAINMENT_PERCENT_BPS` - Sustainment allocation in basis points (default: 200 = 2%)

## Security Notes

- All contracts use OpenZeppelin's battle-tested libraries
- ReentrancyGuard on state-changing functions
- SafeERC20 for token transfers
- Access control via Ownable pattern
- Comprehensive test coverage (59 tests)

## Documentation

See `docs/SUSTAINMENT.md` for detailed information about the Sustainment Protocol.

## Audit Status

⚠️ These contracts have not been professionally audited. Use at your own risk in production.

## License

MIT License - See LICENSE file for details
