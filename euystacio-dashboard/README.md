# Euystacio Omnibus Dashboard (Full Release)

Dieses Dashboard visualisiert:
- Triple-Denomination Scorecard (USD, EC, m³ Wasser)
- Tranche Status (Seed/Core/Activation)
- Ethik-Check (MATL ≤10%, R1 ≥45%)
- SHA256-Verifikation der Smart Contracts

## Echtzeit-Features
- Automatische Aktualisierung von Scorecard und Tranche-Status via Smart Contract Events (Polling, WebSocket-ready)
- Ethik-Check reagiert in Echtzeit auf Änderungen von MATL / R1
- SHA256-Integrität bleibt stets sichtbar

## Nutzung
1. Alle Dateien ins Web-Server-Verzeichnis kopieren
2. index.html im Browser öffnen
3. Automatische Updates via JSON-Export aus Hardhat Event-Listener
4. Optional: WebSocket für echte Echtzeit-Integration aktivieren

🌿 Copilot Hinweise:
- Kann automatisch JSON / Hardhat export lesen und die Scorecard in Echtzeit aktualisieren
- Tranche-Freigaben werden durch Smart Contract Events live im Dashboard sichtbar
- Ethik-Check zeigt sofort, wenn MATL oder R1 die Grenzwerte überschreiten
- SHA256 immer sichtbar, um Sacred Covenant Integrität zu garantieren
