// Echtzeit-Dashboard via JSON Polling (kann mit WebSocket erweitert werden)
/* Scorecard & Tranche-Status werden alle 5s aus data/*.json geladen */
function updateDashboard() {
  fetch('data/scorecard.json').then(r => r.json()).then(scorecard => {
    const tbody = document.getElementById("scorecard-body");
    tbody.innerHTML = "";
    scorecard.forEach(row => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${row.USD}</td><td>${row.EC}</td><td>${row.m3}</td>`;
      tbody.appendChild(tr);
    });
  });
  fetch('data/trancheStatus.json').then(r => r.json()).then(data => {
    const ul = document.getElementById("tranches");
    ul.innerHTML = "";
    data.tranches.forEach(t => {
      const li = document.createElement("li");
      li.textContent = `Tranche ${t.id} – ${t.name}: ${t.status} ${t.proof ? '(Proof: '+t.proof+')' : ''}`;
      ul.appendChild(li);
    });
  });
  fetch('data/ethics.json').then(r => r.json()).then(ethics => {
    const status = document.getElementById("ethics-status");
    status.textContent = (ethics.MATL <= 10 && ethics.R1 >= 45) ? "✔ Ethik erfüllt" : "✖ Ethik verletzt";
  });
  fetch('data/sha256.json').then(r => r.json()).then(sha => {
    document.getElementById("sha-status").textContent = sha.value;
  });
}
updateDashboard();
setInterval(updateDashboard, 5000);
