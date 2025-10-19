const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/healthz', (req, res) => {
  res.json({ status: 'ok', time: new Date().toISOString() });
});

const server = http.createServer(app);
const wss = new WebSocket.Server({ server, path: '/ws' });

wss.on('connection', function connection(ws, req) {
  // Optionally capture user id from URL path (req.url)
  try {
    ws.send(JSON.stringify({ text: 'Welcome to Euystacio Kernel' }));
  } catch (err) {
    console.error('ws send welcome error', err);
  }

  ws.on('message', function incoming(message) {
    const msg = message.toString();
    // Broadcast to all connected clients
    try {
      const payload = JSON.stringify({ text: msg });
      wss.clients.forEach(function each(client) {
        if (client.readyState === WebSocket.OPEN) {
          client.send(payload);
        }
      });
    } catch (err) {
      console.error('ws message handler error', err);
    }
  });

  ws.on('close', () => {
    // no-op
  });
});

server.listen(port, () => console.log(`Euystacio API listening on ${port}`));
