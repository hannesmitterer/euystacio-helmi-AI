# User Autonomy & Control Guide

**Release**: v1.0.0-covenant (Cosimbiosi Basis Fundamentum)  
**Framework**: Zero-Obligation (NRE-002) Compliance  
**Date**: 2025-12-12

---

## 🎯 Purpose

This guide explains how users maintain full control and autonomy when interacting with the Euystacio framework, in alignment with the **Zero-Obligation (NRE-002)** principle of the Cosimbiosi Basis Fundamentum in Eternuum framework.

**Core Guarantee**: You are never forced to participate in any mechanism. All actions are voluntary, and you can exit or override automated processes at any time.

---

## 🔑 Your Rights as a User

### 1. Right to Transparency

**What You Can Do**:
- View all contract source code (open-source on GitHub)
- Read all smart contract state through public variables
- Query any information using view functions
- Monitor all transactions through events
- Verify package integrity with SHA256 checksums

**How to Exercise This Right**:
```javascript
// View current sustainment allocation percentage
const sustainmentPercent = await karmaBond.sustainmentPercent();
console.log(`Allocation: ${sustainmentPercent / 100}%`);

// Check your bond balance
const myBonds = await karmaBond.getBondBalance(myAddress);

// Check if you can release a tranche
const [canRelease, reason] = await tfp.canReleaseTranche(trancheId);
```

### 2. Right to Voluntary Participation

**What You Can Do**:
- Choose if and when to participate in bonding
- Decide whether to participate in governance
- Select which features to use
- Exit the system when you choose (within contract rules)

**How to Exercise This Right**:
- You call functions only when you want to
- No automatic enrollment in any mechanism
- Governance participation is separate from bond holding
- You can redeem bonds according to the contract rules

### 3. Right to Override Automated Processes

**What You Can Do**:
- Request emergency overrides through governance
- Bypass automated restrictions when necessary
- Configure system parameters through governance/ownership

**How to Exercise This Right**:
```javascript
// As owner/governance: Disable governance enforcement temporarily
await tfp.setGovernanceEnforcement(false);

// As owner/governance: Adjust sustainment allocation
await karmaBond.setSustainmentPercent(newPercent);

// As owner/governance: Process exceptional redemptions
await karmaBond.redeemBond(investorAddress, amount);
```

### 4. Right to Full Information Before Action

**What You Can Do**:
- Check contract state before any transaction
- Simulate transactions to see outcomes
- Verify you understand the impact
- Ask questions before committing

**How to Exercise This Right**:
```javascript
// Before bonding: Check allocation percentage
const sustainmentPercent = await karmaBond.sustainmentPercent();
const myAmount = ethers.parseUnits("1000", 6); // 1000 USDC
const sustainmentShare = (myAmount * sustainmentPercent) / 10000n;
const myReserve = myAmount - sustainmentShare;
console.log(`Of ${ethers.formatUnits(myAmount, 6)} USDC:`);
console.log(`  ${ethers.formatUnits(sustainmentShare, 6)} goes to sustainment`);
console.log(`  ${ethers.formatUnits(myReserve, 6)} backs my bonds`);

// Before releasing tranche: Check if possible
const [canRelease, reason] = await tfp.canReleaseTranche(trancheId);
if (!canRelease) {
    console.log(`Cannot release: ${reason}`);
    // Decision: wait, or request governance override
}
```

### 5. Right to Privacy

**What You Can Do**:
- Use pseudonymous addresses
- Interact without revealing personal information
- Control what information you share

**How to Exercise This Right**:
- Use different addresses for different purposes
- No KYC required at contract level (may vary by frontend)
- Your on-chain actions are pseudonymous (address-based)

---

## 🛠️ Autonomy Features by Contract

### KarmaBond: Voluntary Bonding

#### What You Control

1. **When to Bond**
   - You choose when to call `mintBond()`
   - No automatic bonding
   - No forced participation

2. **How Much to Bond**
   - You specify the amount
   - No minimum or maximum enforced by base contract
   - Your choice entirely

3. **Understanding Allocations**
   - `sustainmentPercent` is public - check before bonding
   - You see exactly how much goes to sustainment
   - Transparent allocation calculation

4. **Your Bond Balance**
   - Check anytime with `getBondBalance(yourAddress)`
   - Publicly verifiable
   - No hidden balances

#### Example: Bonding with Full Transparency

```javascript
// Step 1: Check current allocation
const sustainmentPercent = await karmaBond.sustainmentPercent();
console.log(`Current allocation to sustainment: ${sustainmentPercent / 100}%`);

// Step 2: Calculate impact for your amount
const bondAmount = ethers.parseUnits("1000", 6); // 1000 USDC
const sustainmentShare = (bondAmount * BigInt(sustainmentPercent)) / 10000n;
const reserveShare = bondAmount - sustainmentShare;

console.log(`If you bond 1000 USDC:`);
console.log(`  Sustainment: ${ethers.formatUnits(sustainmentShare, 6)} USDC`);
console.log(`  Your Reserve: ${ethers.formatUnits(reserveShare, 6)} USDC`);

// Step 3: Only proceed if you agree with the allocation
if (confirm("Proceed with bonding?")) {
    // Approve stablecoin
    await stableToken.approve(karmaBondAddress, bondAmount);
    
    // Mint bond
    await karmaBond.mintBond(bondAmount);
    
    console.log("Bond minted successfully!");
}
```

### TrustlessFundingProtocol: Override-Capable Governance

#### What You Control (as Governance/Owner)

1. **Emergency Override**
   - Can disable governance enforcement
   - Allows bypassing sustainment checks
   - Transparent through events

```javascript
// Emergency: Bypass sustainment check
await tfp.setGovernanceEnforcement(false);
console.log("Governance enforcement disabled - sustainment checks bypassed");

// Release tranche without sustainment check
await tfp.releaseTranche(trancheId, proofHash);

// Re-enable enforcement
await tfp.setGovernanceEnforcement(true);
console.log("Governance enforcement re-enabled");
```

2. **Tranche Release Verification**
   - Check before releasing
   - Understand why blocked
   - Make informed decisions

```javascript
const [canRelease, reason] = await tfp.canReleaseTranche(trancheId);

if (!canRelease) {
    console.log(`Tranche ${trancheId} cannot be released: ${reason}`);
    
    if (reason === "Sustainment below minimum") {
        // Options:
        // 1. Wait for sustainment to increase
        // 2. Deposit to sustainment
        // 3. Request governance override
        
        const reserve = await sustainment.getSustainmentReserve();
        const minimum = await sustainment.minSustainment();
        const needed = minimum - reserve;
        
        console.log(`Need ${ethers.formatUnits(needed, 6)} more USDC in sustainment`);
    }
} else {
    console.log(`Tranche ${trancheId} is ready for release`);
}
```

### EUSDaoGovernance: Optional Participation

#### What You Control

1. **Governance Participation**
   - Holding tokens doesn't force voting
   - You choose which proposals to vote on
   - You decide when to participate

2. **Contribution Recognition**
   - Your contribution score is visible
   - Affects voting power only if you vote
   - No penalties for non-participation

```javascript
// Check your governance position
const balance = await eusDao.balanceOf(yourAddress);
const contributionScore = await eusDao.contributionScore(yourAddress);
const votingPower = await eusDao.votingPower(yourAddress);

console.log(`Your Governance Position:`);
console.log(`  Token Balance: ${ethers.formatUnits(balance, 18)} EUS`);
console.log(`  Contribution Score: ${contributionScore}`);
console.log(`  Voting Power (if you vote): ${ethers.formatUnits(votingPower, 18)}`);
console.log(`  Participation: Your Choice`);
```

---

## 📋 Common Scenarios & Your Options

### Scenario 1: You Want to Bond

**Your Options**:
1. Check sustainment allocation first
2. Decide if you agree with the percentage
3. Bond the amount you choose
4. Monitor your position anytime

**Zero-Obligation Compliance**: 
- ✅ You choose when
- ✅ You choose how much
- ✅ You see allocations before committing
- ✅ No forced participation

### Scenario 2: Tranche Release is Blocked

**Your Options**:
1. Wait for sustainment to increase naturally
2. Deposit to sustainment to reach minimum
3. Request governance to override temporarily
4. Adjust your timeline

**Zero-Obligation Compliance**:
- ✅ You can override through governance
- ✅ You understand why it's blocked
- ✅ You have multiple paths forward
- ✅ Emergency bypass available

### Scenario 3: You Disagree with Sustainment Allocation

**Your Options**:
1. Propose change through governance
2. Wait for community to adjust parameters
3. Choose not to participate until changed
4. Participate knowing current allocation

**Zero-Obligation Compliance**:
- ✅ Parameters are configurable through governance
- ✅ You can advocate for changes
- ✅ You're not forced to participate
- ✅ Community can adjust via governance

### Scenario 4: You Want to Exit

**Your Options**:
1. Redeem bonds according to contract rules
2. Wait for redemption conditions to be met
3. Transfer bonds (if enabled)
4. Request exceptional processing through governance

**Zero-Obligation Compliance**:
- ✅ Exit mechanisms exist
- ✅ Rules are transparent
- ✅ Governance can assist in exceptional cases
- ✅ Your choice to exit is respected

---

## 🔒 Maintaining Your Autonomy

### Best Practices

1. **Always Verify Before Acting**
   ```javascript
   // Template for any action
   async function beforeAction() {
       // 1. Check current state
       const state = await contract.getRelevantState();
       
       // 2. Calculate impact
       const impact = calculateImpact(state, yourAction);
       
       // 3. Verify you understand
       console.log("Current state:", state);
       console.log("Your action would:", impact);
       
       // 4. Confirm intention
       return confirm("Proceed with this action?");
   }
   ```

2. **Monitor Your Positions**
   ```javascript
   // Regular monitoring
   async function checkMyPosition() {
       const bonds = await karmaBond.getBondBalance(myAddress);
       const govTokens = await eusDao.balanceOf(myAddress);
       const votingPower = await eusDao.votingPower(myAddress);
       
       console.log("Your Position:");
       console.log(`  Bonds: ${ethers.formatUnits(bonds, 6)} USDC`);
       console.log(`  Governance Tokens: ${ethers.formatUnits(govTokens, 18)} EUS`);
       console.log(`  Voting Power: ${ethers.formatUnits(votingPower, 18)}`);
   }
   ```

3. **Participate in Governance**
   - Vote on parameter changes
   - Propose improvements
   - Request overrides when needed
   - Share your perspective

4. **Stay Informed**
   - Monitor events for parameter changes
   - Read governance proposals
   - Understand ecosystem health
   - Ask questions in community

---

## 🚨 When You Need to Override

### Legitimate Override Scenarios

1. **Emergency Situations**
   - Critical funding needed immediately
   - System migration or upgrade
   - Unexpected market conditions

2. **Exceptional Circumstances**
   - Community consensus to bypass temporarily
   - Testing and development
   - Handling edge cases

3. **Parameter Adjustments**
   - Community decides to change allocation
   - Economic conditions change
   - Optimization based on experience

### How to Request Override

**For TrustlessFundingProtocol**:
```javascript
// As owner/governance
// 1. Document reason for override
console.log("Requesting override due to: [reason]");

// 2. Disable enforcement
const tx1 = await tfp.setGovernanceEnforcement(false);
await tx1.wait();
console.log("Enforcement disabled");

// 3. Perform necessary action
const tx2 = await tfp.releaseTranche(trancheId, proofHash);
await tx2.wait();
console.log("Tranche released");

// 4. Re-enable enforcement
const tx3 = await tfp.setGovernanceEnforcement(true);
await tx3.wait();
console.log("Enforcement re-enabled");

// All steps are logged via events for transparency
```

**For KarmaBond Parameters**:
```javascript
// As owner/governance
// 1. Propose change
console.log("Proposing sustainment allocation change from X% to Y%");

// 2. Execute change
const tx = await karmaBond.setSustainmentPercent(newPercent);
await tx.wait();

// 3. Verify change
const updated = await karmaBond.sustainmentPercent();
console.log(`Updated allocation: ${updated / 100}%`);
```

---

## ✅ Autonomy Checklist

Before interacting with the system, verify:

- [ ] I understand what action I'm taking
- [ ] I've checked the current contract state
- [ ] I know the allocation percentages
- [ ] I've calculated the impact on my position
- [ ] I agree with the current parameters
- [ ] I know I can exit later (within rules)
- [ ] I understand I'm not forced to participate further
- [ ] I know how to monitor my position
- [ ] I know how to request overrides if needed
- [ ] I'm participating voluntarily

---

## 📞 Getting Help

### If You're Unsure

1. **Read the Documentation**
   - ETHICAL_FRAMEWORK.md - Principles and guarantees
   - SECURITY_TRANSPARENCY.md - Security details
   - README.md - System overview
   - DEPLOYMENT.md - Deployment guide

2. **Verify Contract State**
   - Use view functions to check
   - Monitor events for changes
   - Simulate transactions

3. **Ask the Community**
   - Open GitHub discussions
   - Participate in governance forums
   - Contact support channels

4. **Start Small**
   - Test with small amounts first
   - Verify everything works as expected
   - Scale up when comfortable

### If You Need an Override

1. **Document the Reason**
   - Explain why override is needed
   - Show impact assessment
   - Propose solution

2. **Engage Governance**
   - Submit proposal if required
   - Discuss with community
   - Build consensus

3. **Execute Transparently**
   - All overrides are logged
   - Community can verify
   - Document post-action

---

## 🌟 Remember

The Euystacio framework is built on the principle that **you are in control**:

- ✅ **No forced participation** - You choose when and how to engage
- ✅ **Full transparency** - You can verify everything
- ✅ **Override capability** - Automated processes can be bypassed
- ✅ **Exit freedom** - You can leave (within contract rules)
- ✅ **Parameter flexibility** - System evolves through governance
- ✅ **Respectful design** - You are treated with dignity

**Your autonomy is not just a feature - it's a fundamental principle of the Cosimbiosi Basis Fundamentum in Eternuum framework.**

---

**Last Updated**: 2025-12-12  
**Version**: 1.0 (Zero-Obligation NRE-002 Compliance)
