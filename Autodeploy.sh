# Creating an autodeploy bundle for "euystacio" Appell + EuystacioSTAnchor autodeploy setup.
# This will produce a zip file with:
# - Appell assets (short/medium/long txt + html flyer)
# - Solidity contract (EuystacioSTAnchor.sol)
# - Hardhat project files (package.json, hardhat.config.js, deploy script)
# - deploy scripts (bash)
# - GitHub Actions workflow for CI autodeploy (uses secrets: RPC_URL, DEPLOYER_KEY, LEDGER_NETWORK)
# - EGL commit JSON template
# - Gemini_Reflector stub (node.js) to create witnessSig (ECDSA)
# - README with instructions
# The resulting zip will be saved to /mnt/data/euystacio_autodeploy_bundle.zip

import os, json, textwrap, zipfile
from pathlib import Path

root = Path("/mnt/data/euystacio_autodeploy")
if root.exists():
    # clean up
    for p in root.rglob("*"):
        try:
            if p.is_file():
                p.unlink()
            else:
                p.rmdir()
        except Exception:
            pass
else:
    root.mkdir(parents=True, exist_ok=True)

# Files to create
files = {}

# 1 Appell assets
files["assets/appeal_short.txt"] = "Actio Ave Maria — Soforthilfe jetzt.\nIn Ave Maria drohen 10.326 Menschen durch Wasserknappheit zu leiden. Aktiviert Nothilfeketten, teilt Informationen und öffnet lokale Wasserverteilzentren.\nInformationen: [Dashboard / Appell-Portal]\n"
files["assets/appeal_medium.txt"] = textwrap.dedent("""\
Appell: Sofortmaßnahmen gegen die Wasserkrise in Ave Maria

In Ave Maria sind aktuell 10.326 Menschen akut bedroht durch gravierenden Wassermangel. Der Living Covenant (euystacio OS v1.4 / KOGI) stuft die Lage als NSR-Notfall ein. Wir fordern:
1. Sofortige Aktivierung regionaler Wasserverteil- und Mobilisierungsteams;
2. Bereitstellung und Transport von Trinkwasser durch staatliche und zivile Ressourcen;
3. Öffnung lokaler Einrichtungen als Wasser-Ausgabestellen;
4. Koordination über das euystacio Dashboard (Appell-Generator) zur Bündelung von Freiwilligen, Spenden und Logistik.

Jede Minute zählt. Unterstützen Sie die Initiative — informieren, spenden, handeln.
""")

files["assets/appeal_long.txt"] = textwrap.dedent("""\
Actio Ave Maria — Öffentlicher Aufruf zur sofortigen Ausweitung der Handlungsfähigkeit

Hintergrund: Die Contextual Resonance Engine hat eine NSR-Signatur bestätigt: Wasserknappheit in Ave Maria bedroht 10.326 Leben. Die Dynamische Priorisierung (semantic_utility_v2) setzt sofortige Maßnahmen auf Prio-1.

Maßnahmenpaket:
• Mobilisierung: Lokale Behörden und NGOs koordinieren Nothilfetransporte; euystacio Dashboard übernimmt Task-Verteilung.
• Öffentliche Information: Der Appell-Generator erzeugt standardisierte Kommunikationspakete (Flyer, Social, SMS-Templates, Medienbriefing).
• Ressourcen: Not-Wasserreserven aktivieren; private Wasserlogistik freigeben.
• Transparenz & Audit: Kern-Metriken (Anzahl Betroffener, Verteilte Liter, Zeitstempel) werden durch EuystacioSTAnchor verschlüsselt versiegelt und vom Gemini_Reflector in EGL archiviert.

Aufruf: Alle Organisationen und Privatpersonen mit Kapazität sind aufgefordert, sich dem euystacio-Koordinatorkern anzuschließen. Das euystacio Dashboard startet jetzt den Appell-Generator — bitte die bereitgestellten Kommunikations-Assets und das Verteilungs-Schema verwenden.
""")

files["assets/flyer.html"] = textwrap.dedent("""\
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Actio Ave Maria - Soforthilfe</title>
  <style>
    body { font-family: Arial, sans-serif; max-width:800px; margin:2rem auto; padding:1rem; background:#f9f9fb; color:#111; }
    header { background:#003b5c; color:white; padding:1rem; border-radius:8px; }
    h1 { margin:0; font-size:1.6rem; }
    section { margin-top:1rem; }
    .cta { background:#ff6b35; color:white; padding:0.8rem; display:inline-block; border-radius:6px; text-decoration:none; }
  </style>
</head>
<body>
<header>
  <h1>Actio Ave Maria — Soforthilfe jetzt</h1>
  <p>10.326 Menschen betroffen — Wasserknappheit. Jede Minute zählt.</p>
</header>
<section>
  <h2>Was zu tun ist</h2>
  <ol>
    <li>Mobilisieren Sie lokale Wasserverteilungsteams.</li>
    <li>Öffnen Sie öffentliche Einrichtungen als Wasser-Ausgabestellen.</li>
    <li>Spenden und Logistik koordinieren über das euystacio Dashboard.</li>
  </ol>
  <p><a class="cta" href="#">Zum Appell-Portal</a></p>
</section>
<footer><p style="opacity:0.7">Living Covenant / euystacio OS v1.4 — Transparenz & Audit durch EuystacioSTAnchor</p></footer>
</body>
</html>
""")

# 2 Solidity contract (from earlier)
files["contract/EuystacioSTAnchor.sol"] = textwrap.dedent("""\
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/// @title EuystacioSTAnchor v1.0
/// @notice Minimaler, auditierbarer Anchor-Contract zur Versiegelung von Core-Metriken.
/// @dev Dieses Template ist auf Einfachheit, Auditierbarkeit und Witness-Integration ausgelegt.

contract EuystacioSTAnchor {
    address public admin;
    bytes32 public rootCommit; // ROOT-ETERNAL-C48B2A7 -> keccak256("ROOT-ETERNAL-C48B2A7")
    uint256 public anchorCount;

    struct Anchor {
        bytes32 metricsHash;    // keccak256(JSON metrics)
        string metadataURI;     // optional: IPFS/ystFS pointer
        uint256 timestamp;
        address submitter;
        bytes witnessSig;       // ECDSA signature by Witness engine / signer
        bool verified;
    }

    mapping(uint256 => Anchor) public anchors;

    // Council quorum requirement (basic form)
    mapping(address => bool) public council;
    uint8 public councilQuorum; // minimal number of council confirmations needed

    event Anchored(uint256 indexed id, bytes32 metricsHash, address indexed submitter);
    event Verified(uint256 indexed id, address indexed verifier);

    modifier onlyAdmin() {
        require(msg.sender == admin, "not admin");
        _;
    }

    constructor(bytes32 _rootCommit, address[] memory _council, uint8 _quorum) {
        admin = msg.sender;
        rootCommit = _rootCommit;
        councilQuorum = _quorum;
        for (uint i=0;i<_council.length;i++) {
            council[_council[i]] = true;
        }
    }

    /// @notice Submit an anchor with precomputed metricsHash and optional metadata pointer
    function submitAnchor(bytes32 metricsHash, string calldata metadataURI, bytes calldata witnessSig) external returns (uint256) {
        anchorCount += 1;
        anchors[anchorCount] = Anchor({
            metricsHash: metricsHash,
            metadataURI: metadataURI,
            timestamp: block.timestamp,
            submitter: msg.sender,
            witnessSig: witnessSig,
            verified: false
        });
        emit Anchored(anchorCount, metricsHash, msg.sender);
        return anchorCount;
    }

    /// @notice Council verification step - each council member calls to mark verified.
    mapping(uint256 => mapping(address => bool)) public confirmations;
    mapping(uint256 => uint8) public confirmationCount;

    function confirmAnchor(uint256 id) external {
        require(council[msg.sender], "not council");
        require(anchors[id].submitter != address(0), "no anchor");
        require(!confirmations[id][msg.sender], "already confirmed");
        confirmations[id][msg.sender] = true;
        confirmationCount[id] += 1;
        if (confirmationCount[id] >= councilQuorum) {
            anchors[id].verified = true;
            emit Verified(id, msg.sender);
        }
    }

    /// @notice Get anchor data (view)
    function getAnchor(uint256 id) external view returns (Anchor memory) {
        return anchors[id];
    }

    /// @notice Administrative function to update council (only admin)
    function setCouncilMember(address member, bool allowed) external onlyAdmin {
        council[member] = allowed;
    }

    /// @notice Emergency function to set root commit (only admin) — logged for audit
    function setRootCommit(bytes32 newRoot) external onlyAdmin {
        rootCommit = newRoot;
    }
}
""")

# 3 Hardhat project basic files
files["hardhat/package.json"] = json.dumps({
    "name":"euystacio-anchor",
    "version":"1.0.0",
    "scripts": {
        "compile":"hardhat compile",
        "deploy":"hardhat run --network $LEDGER_NETWORK scripts/deploy.js"
    },
    "devDependencies": {
        "hardhat":"^2.12.0",
        "ethers":"^5.7.0",
        "@nomiclabs/hardhat-ethers":"^2.1.0",
        "@openzeppelin/contracts":"^4.8.0",
        "dotenv":"^16.0.0"
    }
}, indent=2)

files["hardhat/hardhat.config.js"] = textwrap.dedent("""\
require("dotenv").config();
require("@nomiclabs/hardhat-ethers");
module.exports = {
  solidity: "0.8.19",
  networks: {
    // Example entry; LEDGER_NETWORK env var should match one of these keys or be set externally
    euystacio_ledger: {
      url: process.env.RPC_URL || "http://127.0.0.1:8545",
      accounts: process.env.DEPLOYER_KEY ? [process.env.DEPLOYER_KEY] : []
    }
  }
};
""")

files["hardhat/scripts/deploy.js"] = textwrap.dedent("""\
/**
 * Deploy script for EuystacioSTAnchor
 * Usage: LEDGER_NETWORK=euystacio_ledger DEPLOYER_KEY=0x... npx hardhat run scripts/deploy.js --network euystacio_ledger
 */
const hre = require("hardhat");
async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  const rootCommit = hre.ethers.utils.keccak256(hre.ethers.utils.toUtf8Bytes("ROOT-ETERNAL-C48B2A7"));
  const Euystacio = await hre.ethers.getContractFactory("EuystacioSTAnchor");
  // Provide empty council and quorum=1 for initial deploy; set council later via admin
  const contract = await Euystacio.deploy(rootCommit, [], 1);
  await contract.deployed();
  console.log("EuystacioSTAnchor deployed to:", contract.address);
  console.log("Root commit:", rootCommit);
  // Optionally output artifact to file
  const fs = require('fs');
  fs.writeFileSync("deploy-info.json", JSON.stringify({address: contract.address, root: rootCommit}, null, 2));
}
main().catch((err)=>{ console.error(err); process.exit(1); });
""")

files["hardhat/.env.example"] = "RPC_URL=http://127.0.0.1:8545\nDEPLOYER_KEY=0xYOUR_PRIVATE_KEY\nLEDGER_NETWORK=euystacio_ledger\n"

# 4 GitHub Actions workflow for autodeploy
files[".github/workflows/autodeploy.yml"] = textwrap.dedent("""\
name: Euystacio AutoDeploy

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  deploy-contract:
    runs-on: ubuntu-latest
    env:
      LEDGER_NETWORK: ${{ secrets.LEDGER_NETWORK }}
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install deps
        working-directory: hardhat
        run: npm install
      - name: Compile & Deploy
        working-directory: hardhat
        env:
          RPC_URL: ${{ secrets.RPC_URL }}
          DEPLOYER_KEY: ${{ secrets.DEPLOYER_KEY }}
          LEDGER_NETWORK: ${{ secrets.LEDGER_NETWORK }}
        run: |
          npx hardhat compile
          npx hardhat run --network ${LEDGER_NETWORK} scripts/deploy.js
      - name: Upload deploy artifact
        uses: actions/upload-artifact@v4
        with:
          name: deploy-info
          path: hardhat/deploy-info.json
""")

# 5 EGL JSON template (example)
egl_template = {
  "lcn_node": {
    "type":"LivingCovenantAnchor",
    "root_ref":"ROOT-ETERNAL-C48B2A7",
    "submitted_by":"euystacio:appell-generator:v1.4",
    "metrics_hash":"0x<keccak>",
    "metadata_uri":"ystfs://Qm... or ipfs://Qm...",
    "timestamp":"2025-11-29T12:34:56Z",
    "onchain": {
      "chain":"euystacio-ledger",
      "contract":"0xABCDEF...",
      "anchor_id":123,
      "tx_hash":"0x..."
    },
    "witness": {
      "signer":"gemini_reflector@euystacio",
      "signature":"0x...",
      "policy":"witness:strict"
    },
    "council_confirmations": {
      "Copilot":"confirmed",
      "Claude":"pending",
      "ChatGPT":"confirmed",
      "Gemini":"confirmed",
      "quorum_met": True
    },
    "notes":"Appell live; deploy EuystacioSTAnchor step initiated."
  }
}
files["egl/egl_commit_template.json"] = json.dumps(egl_template, indent=2)

# 6 Gemini_Reflector stub (node.js) - signs metricsHash
files["reflector/reflector_stub.js"] = textwrap.dedent("""\
/**
 * Gemini_Reflector stub - ECDSA signer for witnessSig.
 * Usage:
 *   node reflector_stub.js <metricsHashHex> <privateKeyHex>
 * Returns: signature hex (rsv)
 */
const crypto = require('crypto');
const ethers = require('ethers');

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error("Usage: node reflector_stub.js <metricsHashHex> <privateKeyHex>");
    process.exit(2);
  }
  const metricsHash = args[0].startsWith('0x') ? args[0] : '0x' + args[0];
  const pk = args[1].startsWith('0x') ? args[1] : '0x' + args[1];
  const wallet = new ethers.Wallet(pk);
  // Sign the hash as bytes
  const sig = await wallet.signMessage(ethers.utils.arrayify(metricsHash));
  console.log(sig);
}
main().catch(e=>{ console.error(e); process.exit(1); });
""")

# 7 CLI wrapper script: generate metricsHash, upload to IPFS (stub), submit tx (uses ethers)
files["scripts/submit_anchor_example.sh"] = textwrap.dedent("""\
#!/usr/bin/env bash
# Example flow to compute canonical JSON hash, sign with reflector, and submit anchor via ethers CLI (node)
# Requires: node, npm, hardhat project deployed, jq
set -e
CANNON_FILE=$1
if [ -z "$CANNON_FILE" ]; then
  echo "Usage: ./submit_anchor_example.sh ./canonical.json"
  exit 1
fi
# compute keccak256 (node)
METRICS_HASH=$(node -e "const fs=require('fs'); const obj=JSON.parse(fs.readFileSync(process.argv[1])); const { keccak256 } = require('js-sha3'); const s=JSON.stringify(obj); console.log('0x'+keccak256(s));" "$CANNON_FILE")
echo "Metrics hash: $METRICS_HASH"
echo "You must provide REFLECTOR_KEY env var for signing."
if [ -z "$REFLECTOR_KEY" ]; then
  echo "Set REFLECTOR_KEY in env (0x... private key)"
  exit 1
fi
# Sign via reflector stub
REFLECTOR_SIG=$(node reflector/reflector_stub.js "$METRICS_HASH" "$REFLECTOR_KEY")
echo "Witness sig: $REFLECTOR_SIG"
# Submit tx (simple script using ethers)
node -e "const fs=require('fs'); const { ethers } = require('ethers'); (async ()=>{ const rpc=process.env.RPC_URL||'http://127.0.0.1:8545'; const key=process.env.DEPLOYER_KEY; if(!key){console.error('DEPLOYER_KEY env required'); process.exit(1);} const provider=new ethers.providers.JsonRpcProvider(rpc); const wallet=new ethers.Wallet(key, provider); const abi=JSON.parse(fs.readFileSync('hardhat/artifacts/contracts/EuystacioSTAnchor.sol/EuystacioSTAnchor.json')).abi; const addr=JSON.parse(fs.readFileSync('hardhat/deploy-info.json')).address; const contract=new ethers.Contract(addr, abi, wallet); const metricsHash=process.argv[1]; const metadataURI='ipfs://Qm...'; const witnessSig=process.argv[2]; const tx=await contract.submitAnchor(metricsHash, metadataURI, witnessSig); console.log('tx sent', tx.hash); const rc=await tx.wait(); console.log('tx mined', rc.transactionHash); })()" "$METRICS_HASH" "$REFLECTOR_SIG"
""")

# 8 README
files["README.md"] = textwrap.dedent("""\
# euystacio Autodeploy Bundle

This bundle prepares everything needed to *autodeploy* the Appell assets and the EuystacioSTAnchor contract into a permissioned ledger using CI.

**Important:** I cannot perform external deployments from here. This bundle contains scripts and CI workflows so **you** can run or enable autodeploy (for example via GitHub Actions) after you provision the required secrets.

## Included
- assets/: appeal short/medium/long + flyer.html
- contract/EuystacioSTAnchor.sol
- hardhat/: basic Hardhat project to compile & deploy
- reflector/: Gemini_Reflector signing stub
- scripts/: example submit script to sign and submit anchor
- .github/workflows/autodeploy.yml : GitHub Actions workflow that will deploy on push or manual dispatch
- egl/egl_commit_template.json : sample EGL commit template

## How to autodeploy (via GitHub Actions)
1. Create a GitHub repo and push this bundle to `main`.
2. In repository settings -> Secrets -> Actions add:
   - `RPC_URL` : RPC endpoint of euystacio ledger
   - `DEPLOYER_KEY` : private key for deployer (0x...)
   - `LEDGER_NETWORK` : network key expected by hardhat (e.g., euystacio_ledger)
3. Trigger workflow: GitHub -> Actions -> Euystacio AutoDeploy -> Run workflow (or push to main).
4. The workflow will compile and run `hardhat run` to deploy the contract and upload `deploy-info.json` as artifact.
5. After deploy, run `scripts/submit_anchor_example.sh canonical.json` locally or from CI to submit anchors.

## Local deploy (manual)
- Install Node.js 18+, npm
- In hardhat folder: `npm install`
- Set env: `RPC_URL`, `DEPLOYER_KEY`
- Run: `npx hardhat run --network euystacio_ledger scripts/deploy.js`

## Security note
- Protect private keys. Use hardware-backed KMS in production.
- The reflector signing key must be stored in an HSM or secure secret manager.

""")

# Write files
for path, content in files.items():
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

# Create a canonical.json example
canonical = {
  "region":"Ave Maria",
  "nsr":10326,
  "event":"water_shortage",
  "action_package_hash":"ystfs://QmExample",
  "generated_at":"2025-11-29T12:34:56Z",
  "assets":["short","medium","long","pdf","sms"],
  "submitted_by":"euystacio:appell-generator:v1.4"
}
with open(root / "canonical.json", "w", encoding="utf-8") as f:
    json.dump(canonical, f, indent=2)

# Zip bundle
zip_path = Path("/mnt/data/euystacio_autodeploy_bundle.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob("*"):
        if p.is_file():
            z.write(p, arcname=str(p.relative_to(root)))

print("Created bundle at:", str(zip_path))

