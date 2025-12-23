#!/usr/bin/env node
/**
 * Health check script for Euystacio Helmi AI
 * Checks if the application is healthy and responding
 */

const http = require('http');

const PORT = process.env.PORT || 3000;
const HEALTH_PATH = '/healthz';

const options = {
  host: 'localhost',
  port: PORT,
  path: HEALTH_PATH,
  timeout: 2000
};

const req = http.request(options, (res) => {
  if (res.statusCode === 200) {
    console.log('✅ Health check passed');
    process.exit(0);
  } else {
    console.error(`❌ Health check failed: HTTP ${res.statusCode}`);
    process.exit(1);
  }
});

req.on('error', (err) => {
  console.error(`❌ Health check failed: ${err.message}`);
  process.exit(1);
});

req.on('timeout', () => {
  console.error('❌ Health check timed out');
  req.destroy();
  process.exit(1);
});

req.end();
