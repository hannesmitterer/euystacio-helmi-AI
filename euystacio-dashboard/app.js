// Mock Data – kann per API oder Hardhat Export ersetzt werden
const scorecard = [
  { USD: 1000, EC: 500, m3: 50 },
  { USD: 2000, EC: 1000, m3: 120 },
];

const tranches = [
  { id: 1, name: "Seed Funding", status: "Released" },
  { id: 2, name: "Core Build", status: "Pending" },
  { id: 3, name: "Activation", status: "Pending" },
];

const ethics = { MATL: 9, R1: 50 };

// SHA256 simulation
const sha = "95ad98770f572e6d8764af4a85b878e67391740ceed124799d17178c76fe6b82";

// Populate Scorecard
const tbody = document.getElementById("scorecard-body");
scorecard.forEach(row => {
  const tr = document.createElement("tr");
  tr.innerHTML = `<td>${row.USD}</td><td>${row.EC}</td><td>${row.m3}</td>`;
  tbody.appendChild(tr);
});

// Populate Tranches
const ul = document.getElementById("tranches");
tranches.forEach(t => {
  const li = document.createElement("li");
  li.textContent = `Tranche ${t.id} – ${t.name}: ${t.status}`;
  ul.appendChild(li);
});

// Ethics Check
const ethicsStatus = document.getElementById("ethics-status");
ethicsStatus.textContent = (ethics.MATL <= 10 && ethics.R1 >= 45) ? "✔ Ethik erfüllt" : "✖ Ethik verletzt";

// SHA256
document.getElementById("sha-status").textContent = sha;