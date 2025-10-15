let provider;
let signer;
let userAddress;
let bondContract, trustContract;

const bondAbi = [
  "function invest() payable",
  "function investments(address) view returns (uint256)",
  "event InvestmentMade(address indexed investor, uint256 amount)",
  "event Redeemed(address indexed investor, uint256 amount)"
];
const trustAbi = [
  "function releaseTranche(uint256 trancheId, bytes32 proofHash)",
  "event TrancheReleased(uint256 indexed trancheId, bytes32 proofHash, uint256 timestamp)"
];

// Replace with actual deployed addresses after deployment
let BOND_ADDRESS = "";      // fill after deploy
let TRUST_ADDRESS = "";     // fill after deploy

document.getElementById("bondAddress").textContent = BOND_ADDRESS || "set after deploy";
document.getElementById("trustAddress").textContent = TRUST_ADDRESS || "set after deploy";

async function connect() {
  if (!window.ethereum) {
    alert("MetaMask not found");
    return;
  }
  provider = new ethers.BrowserProvider(window.ethereum);
  await provider.send("eth_requestAccounts", []);
  signer = await provider.getSigner();
  userAddress = await signer.getAddress();
  document.getElementById("address").textContent = userAddress;
  initContracts();
}

function initContracts() {
  if (BOND_ADDRESS) bondContract = new ethers.Contract(BOND_ADDRESS, bondAbi, signer);
  if (TRUST_ADDRESS) trustContract = new ethers.Contract(TRUST_ADDRESS, trustAbi, signer);

  // subscribe to events via provider (public)
  if (bondContract) {
    bondContract.on("InvestmentMade", (investor, amount) => {
      appendEvent(`InvestmentMade: ${investor} - ${ethers.formatEther(amount)} ETH`);
    });
  }
  if (trustContract) {
    trustContract.on("TrancheReleased", (trancheId, proofHash, timestamp) => {
      appendEvent(`TrancheReleased: ${trancheId} proof=${proofHash} ts=${new Date(Number(timestamp) * 1000).toISOString()}`);
    });
  }
}

function appendEvent(text) {
  const container = document.getElementById("events");
  const el = document.createElement("div");
  el.textContent = `[${new Date().toISOString()}] ${text}`;
  container.prepend(el);
}

async function invest() {
  if (!bondContract) return alert("KarmaBond contract not set");
  const amt = document.getElementById("investAmt").value;
  const value = ethers.parseEther(String(amt));
  try {
    document.getElementById("investStatus").textContent = "Sending transaction...";
    const tx = await bondContract.connect(signer).invest({ value });
    document.getElementById("investStatus").textContent = `Tx sent: ${tx.hash}`;
    await tx.wait();
    document.getElementById("investStatus").textContent = `Investment confirmed: ${tx.hash}`;
  } catch (e) {
    document.getElementById("investStatus").textContent = `Error: ${e.message || e}`;
  }
}

async function releaseTranche() {
  if (!trustContract) return alert("TrustlessFundingProtocol contract not set");
  const id = Number(document.getElementById("trancheId").value || 1);
  const proof = document.getElementById("proofText").value || "proof";
  const proofHash = ethers.formatBytes32String(proof);
  try {
    document.getElementById("releaseStatus").textContent = "Sending release tx...";
    const tx = await trustContract.connect(signer).releaseTranche(id, proofHash);
    document.getElementById("releaseStatus").textContent = `Tx sent: ${tx.hash}`;
    await tx.wait();
    document.getElementById("releaseStatus").textContent = `Tranche released: ${tx.hash}`;
  } catch (e) {
    document.getElementById("releaseStatus").textContent = `Error: ${e.message || e}`;
  }
}

// bind UI
document.getElementById("connectBtn").onclick = connect;
document.getElementById("investBtn").onclick = invest;
document.getElementById("releaseBtn").onclick = releaseTranche;