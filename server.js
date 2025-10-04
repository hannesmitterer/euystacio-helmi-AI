const express = require("express");
const { WebSocketServer } = require("ws");
const app = express();
const port = 4000;

const wss = new WebSocketServer({ port: 4001 });

let nodes = Array.from({ length: 50 }, (_, i) => ({
  id: i + 1,
  type: i % 3 === 0 ? "Nutrient+Water" : i % 3 === 1 ? "Shelter" : "Medicine",
  resources: { food: 100, water: 100, shelter: 100, medicine: 100 }
}));

function updateResources() {
  nodes = nodes.map(node => {
    const newResources = { ...node.resources };
    if (node.type === "Nutrient+Water") {
      newResources.food = Math.max(0, newResources.food - Math.random() * 5);
      newResources.water = Math.max(0, newResources.water - Math.random() * 5);
    } else if (node.type === "Shelter") {
      newResources.shelter = Math.max(0, newResources.shelter - Math.random() * 3);
    } else if (node.type === "Medicine") {
      newResources.medicine = Math.max(0, newResources.medicine - Math.random() * 4);
    }
    return { ...node, resources: newResources };
  });

  // Copilot Redistribution
  nodes.forEach(node => {
    const resType = node.type === "Nutrient+Water" ? ["food","water"] :
                    node.type === "Shelter" ? ["shelter"] : ["medicine"];
    const critical = resType.some(r => node.resources[r] < 20);
    if (!critical) return;

    // find donor nodes
    const donors = nodes.filter(d =>
      d.type === node.type &&
      resType.every(r => d.resources[r] > 60)
    );
    donors.forEach(donor => {
      resType.forEach(r => {
        const donorAmount = donor.resources[r];
        const needed = 80 - node.resources[r]; // target after transfer
        const transfer = Math.min(donorAmount - 40, needed, 10); // never drain below 40%, max 10 per step
        node.resources[r] += transfer;
        donor.resources[r] -= transfer;
      });
    });
  });
}

setInterval(() => {
  updateResources();
  wss.clients.forEach(client => {
    client.send(JSON.stringify(nodes));
  });
}, 3000);

console.log(`WebSocket server running on ws://localhost:4001`);