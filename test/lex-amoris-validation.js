#!/usr/bin/env node
/**
 * Lex Amoris Testing and Validation Suite
 * Tests for lexamoris.html and manifest.json
 */

const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function test(name, fn) {
    totalTests++;
    try {
        fn();
        console.log(`  ✓ ${name}`);
        passedTests++;
        return true;
    } catch (error) {
        console.log(`  ✗ ${name}`);
        console.log(`    Error: ${error.message}`);
        failedTests++;
        return false;
    }
}

function assert(condition, message) {
    if (!condition) {
        throw new Error(message || 'Assertion failed');
    }
}

function assertEqual(actual, expected, message) {
    if (actual !== expected) {
        throw new Error(message || `Expected ${expected}, got ${actual}`);
    }
}

function assertContains(haystack, needle, message) {
    if (!haystack.includes(needle)) {
        throw new Error(message || `Expected to contain ${needle}`);
    }
}

console.log('\n========================================');
console.log('Lex Amoris - Testing Suite');
console.log('========================================\n');

// Load HTML file
const htmlPath = path.join(__dirname, '..', 'lexamoris.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf8');

const dom = new JSDOM(htmlContent, {
    runScripts: 'dangerously',
    resources: 'usable',
    beforeParse(window) {
        window.performance.memory = {
            usedJSHeapSize: 50000000,
            totalJSHeapSize: 100000000,
            jsHeapSizeLimit: 200000000
        };
    }
});

const document = dom.window.document;
const window = dom.window;

// SECTION 1: HTML Structure Tests
console.log('HTML Structure and Attributes Tests:');

test('Should have German language attribute', () => {
    assertEqual(document.documentElement.getAttribute('lang'), 'de');
});

test('Should have proper DOCTYPE', () => {
    assert(dom.window.document.doctype, 'DOCTYPE missing');
    assertEqual(dom.window.document.doctype.name, 'html');
});

test('Should have charset UTF-8', () => {
    const charset = document.querySelector('meta[charset]');
    assert(charset, 'Charset meta tag missing');
});

test('Should have viewport meta tag', () => {
    const viewport = document.querySelector('meta[name="viewport"]');
    assert(viewport, 'Viewport meta tag missing');
    assertContains(viewport.getAttribute('content'), 'width=device-width');
});

test('Should have theme-color meta tag with correct color', () => {
    const themeColor = document.querySelector('meta[name="theme-color"]');
    assert(themeColor, 'Theme color meta tag missing');
    assertEqual(themeColor.getAttribute('content'), '#4ade80');
});

test('Should include "Sempre in Costante" branding', () => {
    assertContains(document.body.innerHTML, 'Sempre in Costante');
});

test('Should have "Lex Amoris" in title', () => {
    assertContains(document.querySelector('title').textContent, 'Lex Amoris');
});

test('Should have semantic HTML5 elements', () => {
    assert(document.querySelector('header'), 'Missing header element');
    assert(document.querySelector('main'), 'Missing main element');
    assert(document.querySelector('footer'), 'Missing footer element');
});

// SECTION 2: Resonance Pulse Tests
console.log('\nResonance Pulse Animation Tests:');

test('Should have resonance-pulse section', () => {
    const pulseSection = document.querySelector('.resonance-pulse');
    assert(pulseSection, 'Missing resonance-pulse section');
});

test('Should have pulse-core element', () => {
    const pulseCore = document.querySelector('.pulse-core');
    assert(pulseCore, 'Missing pulse-core element');
});

test('Should have at least 3 pulse rings', () => {
    const pulseRings = document.querySelectorAll('.pulse-ring');
    assert(pulseRings.length >= 3, `Expected at least 3 pulse rings, found ${pulseRings.length}`);
});

test('Should have core-pulse animation defined', () => {
    const styles = document.querySelector('style').textContent;
    assertContains(styles, '@keyframes core-pulse');
});

test('Should have ring-pulse animation defined', () => {
    const styles = document.querySelector('style').textContent;
    assertContains(styles, '@keyframes ring-pulse');
});

test('Should have 2-second animation timing', () => {
    const styles = document.querySelector('style').textContent;
    assert(
        styles.includes('animation: core-pulse 2s') || 
        styles.includes('animation:core-pulse 2s'),
        'Core pulse animation should be 2 seconds'
    );
});

// SECTION 3: Growth Rate Function Tests
console.log('\nGrowth Rate Function Tests:');

test('Should have growthRate function defined', () => {
    assert(typeof window.growthRate === 'function', 'growthRate function not defined');
});

test('Should calculate exponential growth correctly', () => {
    const result = window.growthRate(100, 0.1, 10);
    const expected = 100 * Math.exp(0.1 * 10);
    assert(Math.abs(result - expected) < 0.01, `Expected ${expected}, got ${result}`);
});

test('Should handle initial value of 1', () => {
    const result = window.growthRate(1, 0.5, 5);
    const expected = Math.exp(0.5 * 5);
    assert(Math.abs(result - expected) < 0.01, `Expected ${expected}, got ${result}`);
});

test('Should handle zero time correctly', () => {
    const result = window.growthRate(100, 0.1, 0);
    assertEqual(result, 100);
});

test('Should provide high numerical precision', () => {
    const result = window.growthRate(100, 0.05, 20);
    const expected = 100 * Math.exp(0.05 * 20);
    assert(Math.abs(result - expected) < 1e-10, 'Insufficient numerical precision');
});

test('Should have simulateGrowth function', () => {
    assert(typeof window.simulateGrowth === 'function', 'simulateGrowth function not defined');
});

// SECTION 4: Growth Simulation UI Tests
console.log('\nGrowth Simulation UI Tests:');

test('Should have initial-value input', () => {
    assert(document.getElementById('initial-value'), 'Missing initial-value input');
});

test('Should have growth-rate input', () => {
    assert(document.getElementById('growth-rate'), 'Missing growth-rate input');
});

test('Should have time-periods input', () => {
    assert(document.getElementById('time-periods'), 'Missing time-periods input');
});

test('Should have simulate button', () => {
    assert(document.getElementById('simulate-btn'), 'Missing simulate button');
});

test('Should have growth-chart container', () => {
    assert(document.getElementById('growth-chart'), 'Missing growth-chart container');
});

test('Should have stats-display container', () => {
    assert(document.getElementById('stats-display'), 'Missing stats-display container');
});

// SECTION 5: Red Shield Tests
console.log('\nRed Shield Protection Tests:');

test('Should have Red Shield section', () => {
    const redShieldSection = document.querySelector('.red-shield-section');
    assert(redShieldSection, 'Missing Red Shield section');
});

test('Should have shield-icon element', () => {
    assert(document.getElementById('shield-icon'), 'Missing shield-icon element');
});

test('Should have shield-message element', () => {
    assert(document.getElementById('shield-message'), 'Missing shield-message element');
});

test('Should have event-log element', () => {
    assert(document.getElementById('event-log'), 'Missing event-log element');
});

test('Should have logEvent function', () => {
    assert(typeof window.logEvent === 'function', 'logEvent function not defined');
});

test('Should have updateShieldStatus function', () => {
    assert(typeof window.updateShieldStatus === 'function', 'updateShieldStatus function not defined');
});

test('Should have blur event listener', () => {
    const scriptContent = document.querySelector('script').textContent;
    assertContains(scriptContent, "addEventListener('blur'");
});

test('Should have focus event listener', () => {
    const scriptContent = document.querySelector('script').textContent;
    assertContains(scriptContent, "addEventListener('focus'");
});

test('Should have visibilitychange listener', () => {
    const scriptContent = document.querySelector('script').textContent;
    assertContains(scriptContent, 'visibilitychange');
});

test('Should detect F12 key press', () => {
    const scriptContent = document.querySelector('script').textContent;
    assertContains(scriptContent, 'F12');
});

test('Should detect DevTools keyboard shortcuts', () => {
    const scriptContent = document.querySelector('script').textContent;
    assertContains(scriptContent, 'Ctrl+Shift');
});

// SECTION 6: Water Status Tests
console.log('\nWater Status Link Tests:');

test('Should have water-status link', () => {
    const link = document.querySelector('a[href="/water-status"]');
    assert(link, 'Missing water-status link');
});

test('Should have aria-label on water-status link', () => {
    const link = document.querySelector('a[href="/water-status"]');
    const ariaLabel = link.getAttribute('aria-label');
    assert(ariaLabel && ariaLabel.length > 0, 'Water status link missing aria-label');
});

// SECTION 7: Accessibility Tests
console.log('\nAccessibility Tests:');

test('Should have proper ARIA labels', () => {
    const ariaLabels = document.querySelectorAll('[aria-label]');
    assert(ariaLabels.length >= 3, 'Insufficient ARIA labels');
});

test('Should have role attributes', () => {
    const pulseSection = document.querySelector('.resonance-pulse');
    const chart = document.getElementById('growth-chart');
    const eventLog = document.getElementById('event-log');
    
    assert(pulseSection.getAttribute('role'), 'Resonance pulse missing role');
    assert(chart.getAttribute('role'), 'Growth chart missing role');
    assert(eventLog.getAttribute('role'), 'Event log missing role');
});

test('Should have aria-live on event log', () => {
    const eventLog = document.getElementById('event-log');
    assert(eventLog.getAttribute('aria-live'), 'Event log missing aria-live');
});

// SECTION 8: Responsive Design Tests
console.log('\nResponsive Design Tests:');

test('Should have media queries', () => {
    const styles = document.querySelector('style').textContent;
    assertContains(styles, '@media');
});

test('Should have proper heading hierarchy', () => {
    const h1 = document.querySelectorAll('h1');
    const h2 = document.querySelectorAll('h2');
    assert(h1.length === 1, 'Should have exactly one h1 element');
    assert(h2.length >= 2, 'Should have at least 2 h2 elements');
});

// SECTION 9: Manifest.json Tests
console.log('\nManifest.json PWA Tests:');

const manifestPath = path.join(__dirname, '..', 'manifest.json');
const manifestContent = fs.readFileSync(manifestPath, 'utf8');
const manifest = JSON.parse(manifestContent);

test('Should have valid JSON structure', () => {
    assert(typeof manifest === 'object', 'Manifest is not a valid JSON object');
});

test('Should have name field', () => {
    assert(manifest.name && manifest.name.length > 0, 'Missing or empty name field');
});

test('Should have short_name field', () => {
    assert(manifest.short_name, 'Missing short_name field');
    assert(manifest.short_name.length <= 12, 'short_name should be 12 characters or less');
});

test('Should have start_url set to /', () => {
    assertEqual(manifest.start_url, '/', 'start_url should be "/"');
});

test('Should have display set to standalone', () => {
    assertEqual(manifest.display, 'standalone', 'display should be "standalone"');
});

test('Should have scope set to /', () => {
    assertEqual(manifest.scope, '/', 'scope should be "/"');
});

test('Should have correct theme_color', () => {
    assertEqual(manifest.theme_color, '#4ade80', 'theme_color should be #4ade80');
});

test('Should have correct background_color', () => {
    assertEqual(manifest.background_color, '#0a0a0f', 'background_color should be #0a0a0f');
});

test('Should have lang set to German', () => {
    assertEqual(manifest.lang, 'de', 'lang should be "de"');
});

test('Should have icons array', () => {
    assert(Array.isArray(manifest.icons), 'icons must be an array');
    assert(manifest.icons.length > 0, 'icons array should not be empty');
});

test('Should have 192x192 and 512x512 icons', () => {
    const sizes = manifest.icons.map(icon => icon.sizes);
    assert(sizes.includes('192x192'), 'Missing 192x192 icon');
    assert(sizes.includes('512x512'), 'Missing 512x512 icon');
});

test('Should have maskable icons', () => {
    const maskableIcons = manifest.icons.filter(icon => 
        icon.purpose && icon.purpose.includes('maskable')
    );
    assert(maskableIcons.length > 0, 'Should have at least one maskable icon');
});

test('Should have IPFS links for icons', () => {
    const allIpfs = manifest.icons.every(icon => 
        icon.src && icon.src.startsWith('https://ipfs.io/ipfs/')
    );
    assert(allIpfs, 'All icons should use IPFS links');
});

test('Should have shortcuts array', () => {
    assert(Array.isArray(manifest.shortcuts), 'shortcuts must be an array');
});

test('Should have water-status shortcut', () => {
    const waterStatusShortcut = manifest.shortcuts.find(shortcut => 
        shortcut.url === '/water-status'
    );
    assert(waterStatusShortcut, 'Missing water-status shortcut');
});

test('Should have proper shortcut structure', () => {
    manifest.shortcuts.forEach((shortcut, index) => {
        assert(shortcut.name, `Shortcut ${index} missing name`);
        assert(shortcut.url, `Shortcut ${index} missing url`);
        assert(Array.isArray(shortcut.icons), `Shortcut ${index} missing icons array`);
    });
});

test('Should have screenshots', () => {
    assert(Array.isArray(manifest.screenshots), 'screenshots must be an array');
    assert(manifest.screenshots.length > 0, 'Should have at least one screenshot');
});

test('Should have description with "Sempre in Costante"', () => {
    assert(manifest.description, 'Missing description');
    assertContains(manifest.description, 'Sempre in Costante');
});

test('Should mention Lex Amoris in name', () => {
    assertContains(manifest.name, 'Lex Amoris');
});

test('Should preserve truths array', () => {
    assert(Array.isArray(manifest.truths), 'truths must be an array');
    assert(manifest.truths.length >= 3, 'truths should have at least 3 items');
});

// Clean up
dom.window.close();

// Print summary
console.log('\n========================================');
console.log('Test Summary');
console.log('========================================');
console.log(`Total Tests: ${totalTests}`);
console.log(`Passed: ${passedTests}`);
console.log(`Failed: ${failedTests}`);
console.log(`Success Rate: ${((passedTests / totalTests) * 100).toFixed(2)}%`);
console.log('========================================\n');

// Exit with appropriate code
process.exit(failedTests > 0 ? 1 : 0);
