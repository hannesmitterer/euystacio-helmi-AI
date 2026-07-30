# Lex Amoris - Troubleshooting Workflow Guide
## Sempre in Costante

**Version:** 1.0.0  
**Date:** 2025-01-11  
**Purpose:** Stakeholder guide for diagnosing and resolving Lex Amoris issues

---

## Quick Reference

| Issue Type | Severity | Resolution Time | Go To Section |
|------------|----------|-----------------|---------------|
| PWA Won't Install | 🟡 Medium | 5-10 min | [Section 1](#1-pwa-installation-issues) |
| Animations Laggy | 🟢 Low | 2-5 min | [Section 2](#2-animation-performance) |
| Red Shield Not Working | 🟡 Medium | 5 min | [Section 3](#3-security-features) |
| Growth Calculation Wrong | 🟡 Medium | 2-5 min | [Section 4](#4-calculation-issues) |
| Manifest Errors | 🔴 High | 5-10 min | [Section 5](#5-manifest-problems) |
| Visual Display Issues | 🟢 Low | 2-5 min | [Section 6](#6-display-problems) |
| Deployment Failures | 🔴 High | 10-20 min | [Section 7](#7-deployment-issues) |

---

## 1. PWA Installation Issues

### 1.1 "Add to Home Screen" Not Appearing

**Symptoms:**
- Install banner/button not visible
- No install prompt on mobile
- Can't add to home screen

**Diagnostic Steps:**

```bash
# Step 1: Check HTTPS
curl -I https://yourdomain.com/lexamoris.html | grep -i location

# Step 2: Validate manifest
curl https://yourdomain.com/manifest.json | python -m json.tool

# Step 3: Check browser DevTools
# Chrome: DevTools → Application → Manifest
# Look for errors or warnings
```

**Solution Checklist:**

- [ ] **Verify HTTPS is enabled**
  - PWAs require secure context (HTTPS or localhost)
  - Check certificate validity
  - No mixed content warnings

- [ ] **Validate manifest.json**
  ```bash
  # Online validator
  https://manifest-validator.appspot.com/
  
  # Or use jsonlint
  npm install -g jsonlint
  jsonlint manifest.json
  ```

- [ ] **Check HTML manifest link**
  ```html
  <!-- Should be present in <head> -->
  <link rel="manifest" href="/manifest.json">
  ```

- [ ] **Verify required manifest fields**
  - ✅ `name`
  - ✅ `short_name`
  - ✅ `start_url`
  - ✅ `display`
  - ✅ `icons` (at least 192x192 and 512x512)

- [ ] **Clear browser cache**
  - Chrome: Settings → Privacy → Clear browsing data
  - Firefox: Options → Privacy → Clear Data
  - Safari: Develop → Empty Caches

- [ ] **Test in incognito mode**
  - Eliminates extension conflicts
  - Fresh browser state

**Expected Result:**
After following steps, install prompt should appear or "Add to Home Screen" option should be available in browser menu.

---

### 1.2 PWA Installs But Won't Launch

**Symptoms:**
- Icon appears on home screen
- Tapping opens browser instead of standalone app
- Incorrect display mode

**Solution:**

1. **Check `start_url` accessibility**
   ```bash
   curl -I https://yourdomain.com/lexamoris.html
   # Should return 200 OK
   ```

2. **Verify `scope` configuration**
   - Ensure `start_url` is within `scope`
   - Current config: `scope: "/"` includes all paths

3. **Check `display` mode**
   - Should be `"standalone"` in manifest
   - Fallback modes defined in `display_override`

4. **Uninstall and reinstall PWA**
   - Remove from home screen
   - Clear site data
   - Reinstall fresh

---

## 2. Animation Performance

### 2.1 Choppy or Laggy Animations

**Symptoms:**
- Pulsating heart animation stutters
- Frame rate drops below 30fps
- Visible jank or tearing

**Quick Diagnostic:**

```javascript
// Paste in browser console
let lastTime = performance.now();
let frames = 0;

function checkFPS() {
  frames++;
  const currentTime = performance.now();
  
  if (currentTime >= lastTime + 1000) {
    console.log('FPS:', Math.round((frames * 1000) / (currentTime - lastTime)));
    frames = 0;
    lastTime = currentTime;
  }
  
  requestAnimationFrame(checkFPS);
}

requestAnimationFrame(checkFPS);
```

**Solution Steps:**

**1. Check System Resources**
- [ ] CPU usage < 80%
- [ ] Available RAM > 2GB
- [ ] GPU acceleration enabled
- [ ] Close unnecessary tabs/apps

**2. Browser Settings**
- [ ] Enable hardware acceleration
  - Chrome: `chrome://settings/system`
  - Firefox: `about:preferences` → Performance
- [ ] Disable browser extensions
- [ ] Update to latest browser version

**3. Code-Level Fixes**
- [ ] Check for JavaScript errors in console
- [ ] Verify CSS animations are GPU-accelerated
  ```css
  /* Should use transform (GPU) not left/top (CPU) */
  animation: resonance-pulse 4s ease-in-out infinite;
  ```
- [ ] Reduce animation complexity if needed

**4. Accessibility Check**
- [ ] Verify user doesn't have "Reduce Motion" enabled
  ```javascript
  // Check in console
  window.matchMedia('(prefers-reduced-motion: reduce)').matches
  // If true, animations are intentionally reduced
  ```

**Performance Targets:**
- ✅ 60 FPS constant
- ✅ CPU usage < 15% during animation
- ✅ Memory stable (no leaks)

---

### 2.2 Animation Timing Off

**Symptoms:**
- Pulse cycle not 4 seconds
- Inconsistent timing
- Animation speeds up/slows down

**Solution:**

1. **Verify CSS Animation**
   ```css
   @keyframes resonance-pulse {
     /* Should have 5 keyframes at 0%, 25%, 50%, 75%, 100% */
   }
   
   .resonance-heart {
     animation: resonance-pulse 4s ease-in-out infinite;
   }
   ```

2. **Check Browser DevTools**
   - Open Animations panel (Chrome)
   - Verify duration shows as 4000ms
   - Check timing function is `ease-in-out`

3. **Test Animation Timing**
   ```javascript
   // Measure one complete cycle
   const start = performance.now();
   const element = document.querySelector('.resonance-heart');
   
   element.addEventListener('animationiteration', () => {
     const elapsed = performance.now() - start;
     console.log('Cycle time:', elapsed, 'ms');
   }, { once: true });
   ```

**Expected:** 4000ms ± 50ms tolerance

---

## 3. Security Features

### 3.1 Red Shield Not Triggering

**Symptoms:**
- Can manipulate DOM without alert
- Console changes not detected
- No security events fired

**Diagnostic:**

```javascript
// Test 1: DOM manipulation
document.getElementById('resonanceLevel').textContent = '999';
// Expected: Red Shield alert appears

// Test 2: Console keywords
console.log('trying to hack this');
// Expected: Red Shield alert appears

// Test 3: Check listeners
window.addEventListener('redShieldActivated', (e) => {
  console.log('Security event detected:', e.detail);
});
```

**Solutions:**

**1. Check JavaScript Loaded**
- [ ] Open DevTools Console
- [ ] No JavaScript errors present
- [ ] `initializeRedShield` function exists
  ```javascript
  typeof initializeRedShield === 'function'
  ```

**2. Verify MutationObserver Support**
```javascript
'MutationObserver' in window
// Should return true
```

**3. Check Event Listeners**
```javascript
// Should show security listener
getEventListeners(window)
```

**4. Reload Page**
- Fresh initialization
- Clear console
- Try manipulation test again

**5. Browser Compatibility**
- Chrome 26+: ✅ Full support
- Firefox 14+: ✅ Full support
- Safari 6+: ✅ Full support
- IE 11: ⚠️ Partial support

---

### 3.2 False Positives

**Symptoms:**
- Alert triggers on normal usage
- Clicking buttons shows warning
- Expected actions blocked

**Solution:**

1. **Check Function Call Stack**
   - Alert should only fire for external manipulation
   - Internal functions whitelisted:
     - `updateResonanceLevel`
     - `updateGrowthRate`
     - `resetMetrics`

2. **Verify Stack Trace Check**
   ```javascript
   const currentStack = new Error().stack;
   // Should include authorized function names
   ```

3. **Update Whitelist if Needed**
   - Add new authorized functions to stack check
   - Test thoroughly after changes

---

## 4. Calculation Issues

### 4.1 Exponential Growth Returns NaN

**Symptoms:**
- Growth rate shows `NaN`
- Resonance level shows `NaN`
- Console errors present

**Diagnostic:**

```javascript
// Test basic calculation
calculateExponentialGrowth(1, 0.05, 10)
// Expected: ~1.629

// Check input types
console.log(
  typeof baseValue,  // should be 'number'
  typeof rate,       // should be 'number'
  typeof time        // should be 'number'
);
```

**Solutions:**

**1. Input Validation**
- [ ] All inputs are numbers (not strings)
- [ ] No `undefined` or `null` values
- [ ] Rate is between 0 and 2
- [ ] Time is positive

**2. Check for Infinity**
```javascript
// Values too large
if (!isFinite(result)) {
  console.log('Overflow detected');
}
```

**3. Reset to Defaults**
- Click "Reset Metrics" button
- Reload page
- Try calculation again

---

### 4.2 Growth Values Incorrect

**Symptoms:**
- Results don't match expected values
- Calculations seem off
- Inconsistent results

**Diagnostic Table:**

| Base | Rate | Time | Expected | Formula |
|------|------|------|----------|---------|
| 1 | 0.05 | 10 | 1.629 | 1 × (1.05)^10 |
| 10 | 0.1 | 5 | 16.105 | 10 × (1.1)^5 |
| 100 | 0.01 | 100 | 270.481 | 100 × (1.01)^100 |

**Test Each Case:**
```javascript
function testGrowth() {
  const tests = [
    [1, 0.05, 10, 1.629],
    [10, 0.1, 5, 16.105],
    [100, 0.01, 100, 270.481]
  ];
  
  tests.forEach(([base, rate, time, expected]) => {
    const result = calculateExponentialGrowth(base, rate, time);
    const diff = Math.abs(result - expected);
    console.log(`Test: ${base}, ${rate}, ${time}`);
    console.log(`Expected: ${expected}, Got: ${result}`);
    console.log(`Difference: ${diff} (${diff < 0.01 ? 'PASS' : 'FAIL'})`);
  });
}

testGrowth();
```

**If Tests Fail:**
1. Check `Math.pow` implementation
2. Verify rate clamping logic
3. Review overflow protection
4. Compare with reference implementation

---

## 5. Manifest Problems

### 5.1 Manifest Not Loading (404 Error)

**Symptoms:**
- 404 error in Network tab
- Icons don't load
- Theme color not applied

**Diagnostic:**

```bash
# Check file exists
ls -la /path/to/manifest.json

# Check accessibility
curl https://yourdomain.com/manifest.json

# Validate JSON syntax
cat manifest.json | python -m json.tool
```

**Solutions:**

**1. Verify File Path**
- [ ] File named exactly `manifest.json`
- [ ] Located in website root directory
- [ ] Case-sensitive (use lowercase)

**2. Check HTML Link**
```html
<!-- In lexamoris.html <head> -->
<link rel="manifest" href="/manifest.json">
<!-- NOT href="manifest.json" (relative) -->
```

**3. Configure MIME Type**
- Server should serve as `application/manifest+json`
- Apache `.htaccess`:
  ```apache
  AddType application/manifest+json .json
  ```
- Nginx:
  ```nginx
  types {
    application/manifest+json json;
  }
  ```

**4. Check File Permissions**
```bash
chmod 644 manifest.json
# Should be readable by web server
```

---

### 5.2 Icons Not Displaying

**Symptoms:**
- Default browser icon shown
- App icon missing on home screen
- Blank icon in app switcher

**Solution:**

**1. Validate Icon Data URIs**
```javascript
// Test in console
const img = new Image();
img.src = 'data:image/svg+xml,...'; // Copy from manifest
img.onload = () => console.log('Icon loaded successfully');
img.onerror = () => console.log('Icon failed to load');
```

**2. Check Icon Sizes**
- [ ] At least one icon ≥ 192x192
- [ ] At least one icon ≥ 512x512
- [ ] All sizes declared in manifest

**3. Verify SVG Syntax**
```xml
<!-- Icons should be valid SVG -->
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'>
  <circle cx='256' cy='256' r='256' fill='#ff1744'/>
  <text x='256' y='340' font-size='280' text-anchor='middle' fill='white'>❤</text>
</svg>
```

**4. Test Icon Rendering**
- Copy data URI from manifest
- Paste in browser address bar
- Should render SVG correctly

---

### 5.3 Shortcuts Not Working

**Symptoms:**
- Shortcuts don't appear in app menu
- Clicking shortcuts does nothing
- URLs not navigating correctly

**Browser Support Check:**

| Browser | Shortcuts Support |
|---------|------------------|
| Chrome 96+ | ✅ Full |
| Edge 96+ | ✅ Full |
| Firefox | ⚠️ Limited |
| Safari | ⚠️ Partial |

**Solution:**

1. **Verify Shortcut Structure**
   ```json
   {
     "shortcuts": [
       {
         "name": "Activate Resonance",
         "url": "/lexamoris.html?action=resonate",
         "icons": [...]
       }
     ]
   }
   ```

2. **Check URL Accessibility**
   ```bash
   curl "https://yourdomain.com/lexamoris.html?action=resonate"
   # Should return 200 OK
   ```

3. **Test in Supported Browser**
   - Install PWA in Chrome/Edge
   - Long-press app icon
   - Shortcuts should appear

---

## 6. Display Problems

### 6.1 Responsive Design Issues

**Symptoms:**
- Layout broken on mobile
- Elements overlapping
- Text too small/large

**Diagnostic:**

```javascript
// Check viewport
console.log({
  width: window.innerWidth,
  height: window.innerHeight,
  devicePixelRatio: window.devicePixelRatio
});
```

**Solutions:**

**1. Verify Viewport Meta Tag**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**2. Test Responsive Breakpoints**
- 375px (mobile): ✅ Single column layout
- 768px (tablet): ✅ Grid responsive
- 1920px (desktop): ✅ Max width container

**3. Check CSS Clamp Functions**
```css
font-size: clamp(2rem, 5vw, 4rem);
/* min: 2rem, preferred: 5vw, max: 4rem */
```

**4. Test in DevTools**
- Toggle device toolbar
- Test various screen sizes
- Check for horizontal scroll

---

### 6.2 Colors Not Matching

**Symptoms:**
- Theme color different than expected
- Branding colors wrong
- Contrast issues

**Color Reference:**

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| Primary | `#ff1744` | Main accents, heart |
| Secondary | `#f50057` | Gradients, glow |
| Accent | `#ff4081` | Highlights |
| Background | `#0a0a0f` | Page background |
| Text Light | `#ffffff` | Main text |
| Text Muted | `#b0b0b0` | Secondary text |

**Verification:**

```javascript
// Check computed styles
const heart = document.querySelector('.resonance-heart::before');
const style = getComputedStyle(heart);
console.log('Color:', style.color);
// Should be rgb(255, 23, 68) = #ff1744
```

**Common Issues:**
- [ ] Browser dark mode override
- [ ] Custom stylesheets interfering
- [ ] Color profile differences
- [ ] Display calibration

---

### 6.3 Text Not Readable

**Symptoms:**
- Text too small
- Low contrast
- Font not loading

**Accessibility Check:**

```javascript
// Contrast ratio calculator
function getContrastRatio(fg, bg) {
  // Simplified version
  const luminance = (color) => {
    // Convert hex to RGB and calculate luminance
    // L = 0.2126 * R + 0.7152 * G + 0.0722 * B
  };
  
  const L1 = luminance(fg);
  const L2 = luminance(bg);
  const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
  
  return ratio;
}

// Should be > 4.5:1 for WCAG AA
```

**Solutions:**

1. **Check Font Size**
   - Minimum: 16px (1rem) for body text
   - Headings: Responsive with `clamp()`

2. **Verify Contrast**
   - Text on dark: ≥ 4.5:1 ratio
   - Large text: ≥ 3:1 ratio

3. **Font Loading**
   - Uses system fonts (immediate load)
   - No external font dependencies

---

## 7. Deployment Issues

### 7.1 GitHub Pages Not Deploying

**Symptoms:**
- Changes not visible on live site
- 404 errors on production
- Old version still showing

**Diagnostic:**

```bash
# Check GitHub Pages status
curl -I https://username.github.io/euystacio-helmi-AI/lexamoris.html

# Check deployment logs
# GitHub repo → Actions → Latest workflow run

# Verify branch
git branch --show-current
```

**Solutions:**

**1. Verify GitHub Pages Settings**
- Go to repo Settings → Pages
- Source: Correct branch (main/gh-pages)
- Folder: / (root) or /docs
- Custom domain: If applicable

**2. Check File Deployment**
```bash
# Ensure files committed
git status

# Push to correct branch
git add lexamoris.html manifest.json
git commit -m "Deploy Lex Amoris"
git push origin main
```

**3. Clear GitHub Pages Cache**
- Make a small change
- Commit and push
- Wait 2-5 minutes for rebuild

**4. Check Build Logs**
- Actions tab in GitHub
- Look for errors in workflow
- Fix any issues and re-run

---

### 7.2 IPFS Upload Issues

**Symptoms:**
- CID not generating
- Files not pinned
- Gateway timeout

**Diagnostic:**

```bash
# Check IPFS daemon
ipfs id

# Test file add
ipfs add lexamoris.html

# Check pinned files
ipfs pin ls
```

**Solutions:**

**1. Initialize IPFS**
```bash
# Install IPFS
npm install -g ipfs

# Initialize
ipfs init

# Start daemon
ipfs daemon &
```

**2. Add Files**
```bash
# Add individual files
ipfs add lexamoris.html
ipfs add manifest.json

# Or add directory
ipfs add -r /path/to/project
```

**3. Pin Files**
```bash
# Pin to ensure persistence
ipfs pin add <CID>

# Verify pinned
ipfs pin ls --type recursive
```

**4. Test Gateway Access**
```bash
# Replace <CID> with actual value
curl https://ipfs.io/ipfs/<CID>

# Or use local gateway
curl http://localhost:8080/ipfs/<CID>
```

**5. Update Manifest**
```json
{
  "related_applications": [
    {
      "platform": "web",
      "url": "https://ipfs.io/ipfs/<ACTUAL_CID>"
    }
  ]
}
```

---

### 7.3 Custom Domain SSL Issues

**Symptoms:**
- HTTPS warnings
- Certificate invalid
- Mixed content errors

**Solution:**

**1. Verify DNS Configuration**
```bash
# Check A records
dig yourdomain.com A

# Check CNAME
dig lexamoris.yourdomain.com CNAME
```

**2. Enable HTTPS**
- GitHub Pages: Automatically provided
- Custom server: Use Let's Encrypt
  ```bash
  certbot --apache -d lexamoris.yourdomain.com
  # Or for nginx
  certbot --nginx -d lexamoris.yourdomain.com
  ```

**3. Fix Mixed Content**
- All resources must use HTTPS
- Check for `http://` links
- Update to `https://` or protocol-relative `//`

**4. Force HTTPS Redirect**
```apache
# Apache .htaccess
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

```nginx
# Nginx
server {
    listen 80;
    server_name lexamoris.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 8. Emergency Procedures

### 8.1 Critical Failure - Site Down

**Immediate Actions:**

1. **Check Service Status**
   ```bash
   # GitHub Pages
   https://www.githubstatus.com/
   
   # IPFS
   https://status.ipfs.io/
   ```

2. **Verify Hosting**
   ```bash
   curl -I https://yourdomain.com/lexamoris.html
   # Check status code and response
   ```

3. **Rollback if Needed**
   ```bash
   # Git rollback
   git log --oneline
   git revert <bad-commit-hash>
   git push origin main
   ```

4. **Notify Stakeholders**
   - Email/Slack notification
   - Status page update
   - ETA for resolution

### 8.2 Data Corruption

**If files are corrupted:**

1. **Restore from Git**
   ```bash
   # Reset to last known good commit
   git checkout <commit-hash> -- lexamoris.html manifest.json
   git commit -m "Restore from backup"
   git push origin main
   ```

2. **Verify Integrity**
   ```bash
   # Check file hashes
   sha256sum lexamoris.html manifest.json
   # Compare with known good hashes
   ```

3. **Test Locally**
   ```bash
   # Before deploying
   python3 -m http.server 8000
   # Open http://localhost:8000/lexamoris.html
   # Verify all functions work
   ```

---

## 9. Preventive Maintenance

### 9.1 Regular Health Checks

**Weekly Tasks:**
- [ ] Check site accessibility (5 min)
- [ ] Review browser console for errors (2 min)
- [ ] Test PWA install process (3 min)
- [ ] Monitor performance metrics (5 min)

**Monthly Tasks:**
- [ ] Run full testing suite (30 min)
- [ ] Update browser compatibility matrix (15 min)
- [ ] Review analytics (if enabled) (20 min)
- [ ] Check for browser updates (10 min)

**Quarterly Tasks:**
- [ ] Security audit (2 hours)
- [ ] Performance optimization review (1 hour)
- [ ] Accessibility audit (1 hour)
- [ ] Backup verification (30 min)

### 9.2 Monitoring Setup

**Uptime Monitoring:**
```javascript
// Setup with service like UptimeRobot
// Monitor: https://yourdomain.com/lexamoris.html
// Interval: 5 minutes
// Alerts: Email + SMS
```

**Performance Monitoring:**
```javascript
// Google Analytics (optional)
// Lighthouse CI (automated)
// Web Vitals reporting
```

---

## 10. Support Resources

### 10.1 Contact Information

**Primary Support:**
- Email: hannes.mitterer@gmail.com
- GitHub Issues: https://github.com/hannesmitterer/euystacio-helmi-AI/issues

**Documentation:**
- Testing Log: `LEX_AMORIS_TESTING_LOG.md`
- README: `README.md`
- Code Comments: Inline in source files

### 10.2 External Resources

**PWA Resources:**
- W3C Spec: https://www.w3.org/TR/appmanifest/
- MDN Guide: https://developer.mozilla.org/en-US/docs/Web/Manifest
- Google PWA: https://web.dev/progressive-web-apps/

**Testing Tools:**
- Lighthouse: Chrome DevTools
- PWA Builder: https://www.pwabuilder.com/
- Manifest Validator: https://manifest-validator.appspot.com/

**Browser DevTools:**
- Chrome: F12 or Ctrl+Shift+I
- Firefox: F12 or Ctrl+Shift+I
- Safari: Cmd+Option+I (enable first in preferences)

---

## Appendix: Common Error Messages

| Error Message | Meaning | Solution Section |
|--------------|---------|------------------|
| "Service worker registration failed" | SW not found | [7.1](#71-github-pages-not-deploying) |
| "Manifest parsing failed" | Invalid JSON | [5.1](#51-manifest-not-loading-404-error) |
| "Icon could not be downloaded" | Icon URL/data invalid | [5.2](#52-icons-not-displaying) |
| "start_url is not in scope" | Scope configuration | [1.2](#12-pwa-installs-but-wont-launch) |
| "calculateExponentialGrowth is not defined" | JS not loaded | [4.1](#41-exponential-growth-returns-nan) |
| "MutationObserver is not defined" | Browser not supported | [3.1](#31-red-shield-not-triggering) |

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-01-11  
**Maintained By:** Euystacio Helmi AI Framework

**Sempre in Costante - Always in Constant Resonance**
