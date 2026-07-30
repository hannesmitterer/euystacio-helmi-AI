# Lex Amoris - Deployment and Maintenance Documentation

## Übersicht

Lex Amoris ist eine webbasierte Anwendung im Euystacio Framework, die harmonische Resonanz und exponentielles Wachstum visualisiert. Das System umfasst umfassende Sicherheitsüberwachung durch das Red Shield Protokoll.

## Projektstruktur

```
euystacio-helmi-AI/
├── lexamoris.html          # Hauptanwendung
├── water-status.html       # Wasserstatus-Seite
├── manifest.json           # PWA-Manifest
└── test/
    ├── lex-amoris-validation.js      # Validierungstests (64 Tests)
    └── browser-compatibility-test.js  # Browser-Kompatibilitätstests
```

## Funktionen

### 1. Resonanz-Pulsation (`resonance-pulse`)

**Beschreibung**: Visuell animierte Pulsation, die die lebendige Resonanz des Systems darstellt.

**Technische Details**:
- **Animation**: 2-Sekunden-Zyklus mit `ease-in-out` Timing
- **Komponenten**:
  - Kern-Pulsation (`pulse-core`): Zentrale Animation mit Skalierung
  - Ring-Pulsationen (`pulse-ring`): 4 expandierende Ringe mit gestaffeltem Timing
- **CSS-Animationen**:
  - `@keyframes core-pulse`: Skaliert und ändert die Opazität des Kerns
  - `@keyframes ring-pulse`: Expandiert Ringe von innen nach außen

**Anpassung**:
```css
/* Animation-Geschwindigkeit ändern */
.pulse-core {
    animation: core-pulse 3s ease-in-out infinite; /* Von 2s auf 3s */
}
```

### 2. Exponentielles Wachstum (`growthRate`)

**Beschreibung**: Simulation und Visualisierung exponentiellen Wachstums mit hoher numerischer Präzision.

**Mathematische Formel**:
```javascript
P(t) = P₀ * e^(r*t)
```

Wobei:
- `P₀` = Anfangswert (initial value)
- `r` = Wachstumsrate (growth rate)
- `t` = Zeit (time periods)
- `e` = Eulersche Zahl (2.71828...)

**Technische Details**:
- **Präzision**: Numerische Genauigkeit bis zu 10 Dezimalstellen
- **Bereich**: Unterstützt Werte von 0 bis sehr große Zahlen
- **Performance**: Optimiert für bis zu 50 Zeitperioden

**Verwendung**:
```javascript
// Berechnung: 100 Einheiten mit 10% Wachstumsrate über 10 Perioden
const result = growthRate(100, 0.1, 10);
// Ergebnis: ~271.83
```

**UI-Steuerung**:
- **Anfangswert**: 1-10000 (Standard: 100)
- **Wachstumsrate**: 0.01-0.5 (Standard: 0.1)
- **Zeitperioden**: 5-50 (Standard: 20)

### 3. Red Shield Protokoll

**Beschreibung**: Umfassende Sicherheitsüberwachung zur Erkennung von Manipulationsversuchen.

**Überwachte Ereignisse**:

1. **Fenster-Fokus (Blur/Focus)**:
   - Erkennt Fokusverlust
   - Warnt bei schnellen, wiederholten Fokuswechseln (> 3 in < 2 Sekunden)
   
2. **Sichtbarkeitsänderungen**:
   - Überwacht Tab-Wechsel
   - Protokolliert Sichtbarkeitsstatus

3. **Entwickler-Tools Erkennung**:
   - F12-Taste
   - Ctrl+Shift+I/J/C Tastenkombinationen
   - Fenstergrößenänderungen (potentielle DevTools-Öffnung)

4. **Datenextraktion**:
   - Copy/Paste-Ereignisse
   - Kontextmenü-Anforderungen

5. **Einbettungs-Erkennung**:
   - Warnt, wenn Seite in iframe läuft

**Ereignisprotokoll**:
- Speichert letzte 20 Ereignisse
- Zeitstempel im deutschen Format
- Ereignistypen: INFO, WARNING, ERROR

**Anpassung der Schwellenwerte**:
```javascript
// In lexamoris.html, Zeile ~717
let suspiciousActivityCount = 0;
let lastActivityTime = Date.now();

// Anzahl schneller Blur-Ereignisse vor Warnung ändern
if (suspiciousActivityCount >= 3) { // Von 3 auf 5 ändern
    // Warnung auslösen
}
```

## Deployment

### Statisches Hosting

#### Option 1: GitHub Pages

1. **Dateien hochladen**:
   ```bash
   git add lexamoris.html water-status.html manifest.json
   git commit -m "Deploy Lex Amoris"
   git push origin main
   ```

2. **GitHub Pages aktivieren**:
   - Gehe zu Repository Settings
   - Navigiere zu "Pages"
   - Wähle Branch (main) und Ordner (/ root)
   - Speichern

3. **Zugriff**:
   - URL: `https://username.github.io/repository/lexamoris.html`

#### Option 2: Netlify

1. **Netlify CLI installieren**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Deployment**:
   ```bash
   netlify deploy --dir=. --prod
   ```

3. **Alternativ**: Drag-and-drop in Netlify UI

#### Option 3: Vercel

```bash
vercel --prod
```

### PWA-Installation

Die Anwendung unterstützt Progressive Web App (PWA) Installation:

1. **Automatische Installation**:
   - Moderne Browser zeigen "Install"-Banner
   - Benutzer können zur Startseite hinzufügen

2. **Voraussetzungen**:
   - HTTPS (außer localhost)
   - Gültiges `manifest.json`
   - Service Worker (optional, aber empfohlen)

3. **Verifikation**:
   - Chrome DevTools > Application > Manifest
   - Überprüfe alle Manifest-Felder

## Testing

### Lokale Tests ausführen

```bash
# Installation von Abhängigkeiten
npm install --save-dev jsdom

# Validierungstests (64 Tests)
node test/lex-amoris-validation.js

# Browser-Kompatibilitätstests
node test/browser-compatibility-test.js
```

### Test-Kategorien

1. **HTML-Struktur**: 8 Tests
2. **Resonanz-Pulsation**: 6 Tests
3. **Wachstumsfunktion**: 6 Tests
4. **Growth UI**: 6 Tests
5. **Red Shield**: 11 Tests
6. **Water Status**: 2 Tests
7. **Accessibility**: 3 Tests
8. **Responsive Design**: 2 Tests
9. **Manifest.json**: 20 Tests

**Gesamt**: 64 Tests, 100% Pass-Rate

### Manuelle Browser-Tests

1. **Chrome/Edge**:
   ```bash
   # Öffne mit lokalem Server
   python3 -m http.server 8000
   # Navigiere zu http://localhost:8000/lexamoris.html
   ```

2. **Firefox**: Gleiche Schritte wie Chrome

3. **Safari**:
   - Aktiviere "Develop" Menü
   - Teste auf verschiedenen iOS-Geräten

## Browser-Kompatibilität

### Unterstützte Browser

| Browser | Mindestversion | Status |
|---------|---------------|--------|
| Chrome | 90+ | ✓ Vollständig |
| Edge | 90+ | ✓ Vollständig |
| Firefox | 88+ | ✓ Vollständig |
| Safari | 14+ | ✓ Vollständig |
| iOS Safari | 14+ | ✓ Vollständig |
| Chrome Android | 90+ | ✓ Vollständig |

### Browser-Features

- ✓ CSS Grid & Flexbox
- ✓ CSS Animations
- ✓ CSS Custom Properties (Variablen)
- ✓ ES6+ JavaScript
- ✓ Web APIs (Performance, Visibility)
- ✓ Service Worker (optional)

## Wartung

### Regelmäßige Aufgaben

1. **Monatlich**:
   - Tests ausführen
   - Dependencies aktualisieren
   - Sicherheitsupdates prüfen

2. **Vierteljährlich**:
   - Browser-Kompatibilität testen
   - Performance-Audit durchführen
   - Accessibility-Audit

3. **Jährlich**:
   - Komplettes Review der Dokumentation
   - Major-Version Upgrades

### Monitoring

1. **Performance**:
   - Heartbeat-Protokoll überwachen (jede Minute)
   - Speicherverbrauch beobachten
   - Animation-Performance (60 FPS anstreben)

2. **Sicherheit**:
   - Red Shield-Ereignisse analysieren
   - Verdächtige Aktivitäten untersuchen
   - Regelmäßige Sicherheitsaudits

3. **Benutzer-Feedback**:
   - Accessibility-Probleme sammeln
   - Performance-Beschwerden dokumentieren
   - Feature-Anfragen priorisieren

## Fehlerbehebung

### Häufige Probleme

#### Problem: Animationen laufen nicht

**Lösung**:
```javascript
// In Browser-Konsole prüfen:
console.log(window.getComputedStyle(document.querySelector('.pulse-core')).animation);
```

Mögliche Ursachen:
- CSS nicht geladen
- Browser unterstützt Animationen nicht
- Reduced-motion-Präferenz aktiviert

#### Problem: Growth-Simulation zeigt nichts

**Lösung**:
```javascript
// In Browser-Konsole:
simulateGrowth();
// Prüfe auf Fehler
```

Mögliche Ursachen:
- JavaScript-Fehler
- Ungültige Eingabewerte
- DOM nicht vollständig geladen

#### Problem: Red Shield warnt zu oft

**Lösung**:
```javascript
// Schwellenwerte in lexamoris.html anpassen (Zeile ~717)
if (suspiciousActivityCount >= 5) { // Von 3 erhöhen
    // Warnung
}
```

## AIC-Konventionen

Das Projekt folgt den AIC (Artificial Intelligence Collective) linguistischen Konventionen:

- **Sprache**: Deutsch (`lang="de"`)
- **Branding**: "Sempre in Costante" (Immer in Beständigkeit)
- **Farbschema**: Grün (#4ade80) für Harmonie, Cyan (#00f0ff) für Wasser
- **Philosophie**: Transparenz, Sicherheit, Nachhaltigkeit

## Sicherheit

### Best Practices

1. **Kein Inline-JavaScript**: Event-Listener statt `onclick`
2. **HTTPS**: Immer verschlüsselte Verbindungen
3. **Content Security Policy**: Empfohlen für Produktion
4. **Input-Validierung**: Alle Benutzereingaben validieren
5. **IPFS-Links**: Dezentrale Ressourcen-Speicherung

### Content Security Policy (Empfohlen)

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline'; 
               style-src 'self' 'unsafe-inline'; 
               img-src 'self' https://ipfs.io;">
```

## Integration mit AIC

### Wasserstatus-Integration

Die `water-status` Shortcut ermöglicht schnellen Zugriff auf Hydrations-Metriken:

```javascript
// In water-status.html anpassen:
<div class="status-value">87%</div> // Dynamische Werte
```

### Ereignis-Logging

Alle Ereignisse können an zentrale AIC-Logging-Systeme weitergeleitet werden:

```javascript
function logEvent(type, message) {
    // Lokal loggen
    // ...
    
    // An AIC senden (optional)
    fetch('/api/aic/log', {
        method: 'POST',
        body: JSON.stringify({ type, message, timestamp: new Date() })
    });
}
```

## Lizenz und Urheberrecht

© 2026 Lex Amoris - Sempre in Costante  
Teil des Euystacio Framework  
Lizenz: MIT (siehe Repository)

## Support

Bei Fragen oder Problemen:

1. **Dokumentation prüfen**: Diese Datei
2. **Tests ausführen**: Fehler identifizieren
3. **Issues erstellen**: GitHub Repository
4. **Community**: AIC Discord/Kommunikationskanäle

---

**Letzte Aktualisierung**: 2026-01-11  
**Version**: 1.0.0  
**Maintainer**: Euystacio Framework Team
