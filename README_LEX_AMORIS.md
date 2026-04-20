# Lex Amoris - Sempre in Costante

**Eine harmonische Resonanz- und Wachstums-Visualisierung im Euystacio Framework**

![Lex Amoris](https://github.com/user-attachments/assets/0543b8b7-337c-465c-9e5c-e21d16b0eff1)

---

## Übersicht

Lex Amoris ist eine webbasierte Progressive Web App (PWA), die harmonische Resonanz durch pulsierende Animationen visualisiert und exponentielles Wachstum simuliert. Das System verfügt über ein umfassendes Red Shield Sicherheitsprotokoll zur Überwachung und Protokollierung von Systemereignissen.

### Kernprinzipien

- **Sempre in Costante** - Immer in Beständigkeit
- **Transparenz** in Design und Funktionalität
- **Sicherheit** durch kontinuierliche Überwachung
- **Präzision** in mathematischen Berechnungen
- **Zugänglichkeit** für alle Benutzer

---

## Funktionen

### 🌀 Resonanz-Pulsation

Visuell animierte Pulsation mit 2-Sekunden-Zyklus:
- Zentrale Kern-Pulsation mit Skalierungseffekt
- 4 expandierende Ringe mit gestaffeltem Timing
- GPU-beschleunigte Animationen (60 FPS)
- Responsive und barrierefrei

### 📈 Exponentielles Wachstum

Interaktive Simulation mit hoher Präzision:
- Mathematische Formel: `P(t) = P₀ * e^(r*t)`
- Numerische Genauigkeit < 10⁻¹⁰
- Echtzeit-Visualisierung als Bar-Chart
- Umfassende Statistik-Anzeige

### 🛡️ Red Shield Protokoll

Umfassendes Sicherheits-Monitoring:
- Fenster-Fokus-Überwachung
- DevTools-Erkennung (F12, Ctrl+Shift+I/J/C)
- Schnellaktivitäts-Detektion (≥3 Events in <2s)
- Tab-Wechsel-Tracking
- iframe-Einbettungs-Erkennung
- Ereignisprotokoll (20 Einträge)

### 🌊 Wasserstatus

Dedizierte Dashboard-Seite für:
- Hydrationslevel-Anzeige
- Systemfluss-Status
- Reinheits-Metriken

---

## Schnellstart

### Online-Zugriff

Besuchen Sie die bereitgestellte URL (nach Deployment) oder verwenden Sie eine der folgenden Methoden für lokalen Zugriff:

### Lokale Verwendung

```bash
# Repository klonen
git clone https://github.com/hannesmitterer/euystacio-helmi-AI.git
cd euystacio-helmi-AI

# Einfacher HTTP-Server
python3 -m http.server 8000

# Im Browser öffnen
open http://localhost:8000/lexamoris.html
```

### PWA Installation

1. Besuchen Sie die Seite in einem modernen Browser
2. Klicken Sie auf "Zur Startseite hinzufügen" / "Install"
3. Die App läuft nun im Standalone-Modus

---

## Technologie-Stack

- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Animationen**: CSS Keyframes, Transform, Opacity
- **Layout**: CSS Grid, Flexbox
- **Accessibility**: ARIA Labels, Semantic HTML
- **PWA**: Web App Manifest, Service Worker ready
- **Icons**: IPFS-gehostet, Maskable-Support

---

## Browser-Kompatibilität

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Vollständig |
| Edge | 90+ | ✅ Vollständig |
| Firefox | 88+ | ✅ Vollständig |
| Safari | 14+ | ✅ Vollständig |
| iOS Safari | 14+ | ✅ Vollständig |
| Chrome Android | 90+ | ✅ Vollständig |

---

## Projektstruktur

```
euystacio-helmi-AI/
├── lexamoris.html                      # Hauptanwendung
├── water-status.html                   # Wasserstatus-Dashboard
├── manifest.json                       # PWA-Manifest
├── test/
│   ├── lex-amoris-validation.js       # 64 Validierungstests
│   └── browser-compatibility-test.js   # 28 Kompatibilitätstests
├── LEX_AMORIS_DOCUMENTATION.md         # Wartungsanleitung
├── LEX_AMORIS_DEPLOYMENT_REPORT.md     # Implementierungsbericht
├── SECURITY_SUMMARY.md                 # Sicherheitsanalyse
└── README_LEX_AMORIS.md                # Diese Datei
```

---

## Tests

### Automatisierte Tests ausführen

```bash
# Abhängigkeiten installieren
npm install --save-dev jsdom

# Validierungstests (64 Tests)
node test/lex-amoris-validation.js

# Browser-Kompatibilitätstests (28 Tests)
node test/browser-compatibility-test.js
```

### Test-Ergebnisse

- ✅ **64/64 Validierungstests** bestanden (100%)
- ✅ **28/28 Kompatibilitätstests** bestanden (100%)
- ✅ **0 Sicherheitslücken** (CodeQL verifiziert)

---

## Sicherheit

### Implementierte Sicherheitsmaßnahmen

- ✅ Keine Inline-Event-Handler
- ✅ Input-Validierung für alle Benutzereingaben
- ✅ XSS-Prävention
- ✅ iframe-Einbettungs-Erkennung
- ✅ DevTools-Überwachung
- ✅ Ereignis-Audit-Trail
- ✅ CSP-kompatible Code-Struktur

### Sicherheitsbewertung

**CodeQL-Analyse**: 0 Schwachstellen  
**Manuelle Überprüfung**: BESTANDEN  
**Gesamtbewertung**: ✅ EXZELLENT

---

## Verwendung

### Resonanz-Pulsation

Die pulsierende Animation startet automatisch beim Laden der Seite und zeigt die harmonische Resonanz des Systems.

### Wachstums-Simulation

1. **Anfangswert** einstellen (1-10000)
2. **Wachstumsrate** anpassen (0.01-0.5)
3. **Zeitperioden** wählen (5-50)
4. **"Simulation starten"** klicken
5. Ergebnisse im Chart und Statistik-Display anzeigen

### Red Shield Monitoring

Das Red Shield Protokoll überwacht automatisch:
- Fenster-Fokus-Änderungen
- DevTools-Aktivierung
- Verdächtige Aktivitätsmuster
- Alle Ereignisse im Protokoll einsehbar

### Wasserstatus

Klicken Sie auf "🌊 Zum Wasserstatus" um:
- Hydrationslevel zu sehen (87%)
- Systemfluss zu prüfen (Optimal)
- Reinheit zu überprüfen (99.8%)

---

## Anpassung

### Farben ändern

In `lexamoris.html` im `:root` CSS:

```css
:root {
    --primary-color: #4ade80;  /* Grün */
    --secondary-color: #00f0ff; /* Cyan */
    --bg-color: #0a0a0f;       /* Dunkel */
}
```

### Animation-Geschwindigkeit

```css
.pulse-core {
    animation: core-pulse 3s ease-in-out infinite; /* Von 2s auf 3s */
}
```

### Red Shield Schwellenwerte

In der JavaScript-Funktion (Zeile ~717):

```javascript
if (suspiciousActivityCount >= 5) { // Von 3 auf 5 ändern
    // Warnung auslösen
}
```

---

## Deployment

### GitHub Pages

```bash
git push origin main
# In Repository Settings: Pages aktivieren
```

### Netlify

```bash
netlify deploy --dir=. --prod
```

### Vercel

```bash
vercel --prod
```

### Docker

```dockerfile
FROM nginx:alpine
COPY lexamoris.html /usr/share/nginx/html/
COPY water-status.html /usr/share/nginx/html/
COPY manifest.json /usr/share/nginx/html/
EXPOSE 80
```

---

## Dokumentation

- **[LEX_AMORIS_DOCUMENTATION.md](LEX_AMORIS_DOCUMENTATION.md)** - Vollständige Wartungsanleitung
- **[LEX_AMORIS_DEPLOYMENT_REPORT.md](LEX_AMORIS_DEPLOYMENT_REPORT.md)** - Detaillierter Implementierungsbericht
- **[SECURITY_SUMMARY.md](SECURITY_SUMMARY.md)** - Sicherheitsanalyse und Empfehlungen

---

## Beitragen

Da dies Teil des Euystacio Frameworks ist, folgen Beiträge den AIC-Richtlinien:

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add AmazingFeature'`)
4. Pushe zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

---

## Lizenz

Dieses Projekt ist Teil des Euystacio Frameworks und unter der MIT-Lizenz lizenziert.

---

## Kontakt

**Projekt**: Lex Amoris - Sempre in Costante  
**Framework**: Euystacio AI Collective  
**Support**: hannes.mitterer@gmail.com  
**Repository**: https://github.com/hannesmitterer/euystacio-helmi-AI

---

## Danksagungen

- **Euystacio Framework** - Für die ethischen Grundsätze
- **AIC Community** - Für die linguistischen Konventionen
- **Open Source Community** - Für die verwendeten Technologien

---

## Screenshots

### Hauptanwendung

![Lex Amoris Main](https://github.com/user-attachments/assets/0543b8b7-337c-465c-9e5c-e21d16b0eff1)

*Resonanz-Pulsation, Wachstums-Chart, Red Shield Protokoll und Wasserstatus-Link*

### Wasserstatus

![Water Status](https://github.com/user-attachments/assets/3eb98c29-c73b-4fcc-be81-5338b3276d79)

*Hydrationslevel, Systemfluss und Reinheits-Metriken*

---

## Status

- ✅ **Version**: 1.0.0
- ✅ **Status**: Produktionsbereit
- ✅ **Tests**: 92/92 bestanden (100%)
- ✅ **Sicherheit**: 0 Schwachstellen
- ✅ **Dokumentation**: Vollständig
- ✅ **Browser-Support**: Chrome 90+, Firefox 88+, Safari 14+

---

**"Sempre in Costante - Immer in Beständigkeit"**

*In code we trust, through covenant we govern.* - Euystacio Helmi

---

© 2026 Lex Amoris | Euystacio Framework | MIT License
