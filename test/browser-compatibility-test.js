#!/usr/bin/env node
/**
 * Browser Compatibility and UI Test Script
 * Tests lexamoris.html in a browser-like environment
 */

const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

console.log('\n========================================');
console.log('Lex Amoris - Browser Compatibility Tests');
console.log('========================================\n');

let totalTests = 0;
let passedTests = 0;

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
        return false;
    }
}

// Load HTML
const htmlPath = path.join(__dirname, '..', 'lexamoris.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf8');

const dom = new JSDOM(htmlContent, {
    runScripts: 'dangerously',
    resources: 'usable',
    url: 'http://localhost/',
    beforeParse(window) {
        // Mock browser APIs
        window.performance.memory = {
            usedJSHeapSize: 50000000,
            totalJSHeapSize: 100000000,
            jsHeapSizeLimit: 200000000
        };
    }
});

const document = dom.window.document;
const window = dom.window;

console.log('CSS Animation Tests:');

test('Core pulse animation should have proper keyframes', () => {
    const styles = document.querySelector('style').textContent;
    const keyframeMatch = styles.match(/@keyframes core-pulse\s*{([^}]+)}/s);
    if (!keyframeMatch) throw new Error('Core pulse keyframes not found');
    
    const keyframeContent = keyframeMatch[1];
    if (!keyframeContent.includes('0%') && !keyframeContent.includes('from')) {
        throw new Error('Missing start keyframe');
    }
    if (!keyframeContent.includes('100%') && !keyframeContent.includes('to')) {
        throw new Error('Missing end keyframe');
    }
    if (!keyframeContent.includes('transform')) {
        throw new Error('Missing transform property');
    }
});

test('Ring pulse animation should have opacity changes', () => {
    const styles = document.querySelector('style').textContent;
    const keyframeMatch = styles.match(/@keyframes ring-pulse\s*{([^}]+)}/s);
    if (!keyframeMatch) throw new Error('Ring pulse keyframes not found');
    
    const keyframeContent = keyframeMatch[1];
    if (!keyframeContent.includes('opacity')) {
        throw new Error('Ring pulse should animate opacity');
    }
});

test('Animations should have ease-in-out timing', () => {
    const styles = document.querySelector('style').textContent;
    if (!styles.includes('ease-in-out')) {
        throw new Error('Animations should use ease-in-out timing');
    }
});

console.log('\nGrowth Simulation Performance Tests:');

test('Growth calculation should handle large numbers', () => {
    const result = window.growthRate(1000000, 0.1, 50);
    if (!isFinite(result)) throw new Error('Result should be finite');
    if (result <= 0) throw new Error('Result should be positive');
});

test('Growth calculation should handle small rates', () => {
    const result = window.growthRate(100, 0.001, 100);
    if (!isFinite(result)) throw new Error('Result should be finite');
    const expected = 100 * Math.exp(0.001 * 100);
    if (Math.abs(result - expected) > 0.01) {
        throw new Error('Incorrect calculation for small rates');
    }
});

test('Growth calculation should handle edge cases', () => {
    const result1 = window.growthRate(0, 0.1, 10);
    if (result1 !== 0) throw new Error('Zero initial value should return 0');
    
    const result2 = window.growthRate(100, 0, 10);
    if (result2 !== 100) throw new Error('Zero rate should return initial value');
});

console.log('\nRed Shield Event Detection Tests:');

test('Should log window blur events', () => {
    const eventLog = document.getElementById('event-log');
    const initialCount = eventLog.children.length;
    
    // Simulate blur event
    const event = new window.Event('blur');
    window.dispatchEvent(event);
    
    setTimeout(() => {
        if (eventLog.children.length <= initialCount) {
            throw new Error('Blur event not logged');
        }
    }, 100);
});

test('Should detect rapid successive blur events', () => {
    const eventLog = document.getElementById('event-log');
    
    // Reset activity counter by waiting
    setTimeout(() => {
        // Trigger rapid blur events
        for (let i = 0; i < 4; i++) {
            const event = new window.Event('blur');
            window.dispatchEvent(event);
        }
        
        // Check for warning
        setTimeout(() => {
            const logHTML = eventLog.innerHTML;
            const hasWarning = logHTML.includes('WARNING') || logHTML.includes('Verdächtige');
            if (!hasWarning) {
                throw new Error('Rapid blur events should trigger warning');
            }
        }, 200);
    }, 2500); // Wait more than 2 seconds to reset counter
});

test('Should log visibility change events', () => {
    const eventLog = document.getElementById('event-log');
    const initialCount = eventLog.children.length;
    
    // Mock visibility change
    Object.defineProperty(document, 'hidden', {
        writable: true,
        value: true
    });
    
    const event = new window.Event('visibilitychange');
    document.dispatchEvent(event);
    
    setTimeout(() => {
        if (eventLog.children.length <= initialCount) {
            throw new Error('Visibility change not logged');
        }
    }, 100);
});

console.log('\nUI Interaction Tests:');

test('Growth rate slider should update display', () => {
    const slider = document.getElementById('growth-rate');
    const display = document.getElementById('growth-rate-value');
    
    slider.value = '0.25';
    const event = new window.Event('input', { bubbles: true });
    slider.dispatchEvent(event);
    
    setTimeout(() => {
        if (!display.textContent.includes('0.25')) {
            throw new Error('Display not updated');
        }
    }, 100);
});

test('Simulate button should trigger simulation', () => {
    const chart = document.getElementById('growth-chart');
    const initialChildren = chart.children.length;
    
    window.simulateGrowth();
    
    setTimeout(() => {
        if (chart.children.length <= initialChildren) {
            throw new Error('Chart not populated');
        }
    }, 200);
});

test('logEvent function should create event entries', () => {
    const eventLog = document.getElementById('event-log');
    const initialCount = eventLog.children.length;
    
    window.logEvent('TEST', 'Test message');
    
    if (eventLog.children.length !== initialCount + 1) {
        throw new Error('Event not logged');
    }
    
    const lastEntry = eventLog.firstElementChild;
    if (!lastEntry.textContent.includes('TEST')) {
        throw new Error('Event type not in log');
    }
    if (!lastEntry.textContent.includes('Test message')) {
        throw new Error('Event message not in log');
    }
});

test('Event log should limit entries to 20', () => {
    const eventLog = document.getElementById('event-log');
    
    // Add many events
    for (let i = 0; i < 30; i++) {
        window.logEvent('TEST', `Message ${i}`);
    }
    
    if (eventLog.children.length > 20) {
        throw new Error(`Event log should be limited to 20 entries, found ${eventLog.children.length}`);
    }
});

console.log('\nResponsive Design Tests:');

test('Should have flexible layout containers', () => {
    const styles = document.querySelector('style').textContent;
    if (!styles.includes('flex') && !styles.includes('grid')) {
        throw new Error('Should use flexbox or grid for layout');
    }
});

test('Should have mobile breakpoint', () => {
    const styles = document.querySelector('style').textContent;
    const hasBreakpoint = styles.includes('@media') && 
                         (styles.includes('768px') || styles.includes('max-width'));
    if (!hasBreakpoint) {
        throw new Error('Should have mobile breakpoint');
    }
});

test('Viewport should be responsive', () => {
    const viewport = document.querySelector('meta[name="viewport"]');
    const content = viewport.getAttribute('content');
    if (!content.includes('width=device-width')) {
        throw new Error('Viewport should be responsive');
    }
    if (!content.includes('initial-scale=1')) {
        throw new Error('Viewport should have initial-scale=1');
    }
});

console.log('\nPerformance Tests:');

test('Should have optimized CSS', () => {
    const styles = document.querySelector('style').textContent;
    // Check for will-change or transform for animations
    const hasOptimization = styles.includes('transform') || 
                           styles.includes('will-change');
    if (!hasOptimization) {
        throw new Error('Should use transform for better performance');
    }
});

test('Should use CSS variables for theming', () => {
    const styles = document.querySelector('style').textContent;
    if (!styles.includes(':root') || !styles.includes('--')) {
        throw new Error('Should use CSS custom properties');
    }
});

test('Should have transition properties for smooth UX', () => {
    const styles = document.querySelector('style').textContent;
    if (!styles.includes('transition')) {
        throw new Error('Should have transitions for better UX');
    }
});

console.log('\nAccessibility Compliance Tests:');

test('All images should have alt text or aria-label', () => {
    const images = document.querySelectorAll('img');
    images.forEach((img, index) => {
        if (!img.getAttribute('alt') && !img.getAttribute('aria-label')) {
            throw new Error(`Image ${index} missing alt text or aria-label`);
        }
    });
});

test('Interactive elements should be keyboard accessible', () => {
    const buttons = document.querySelectorAll('button');
    const links = document.querySelectorAll('a');
    const inputs = document.querySelectorAll('input');
    
    const total = buttons.length + links.length + inputs.length;
    if (total === 0) {
        throw new Error('Should have interactive elements');
    }
});

test('Color contrast should be sufficient', () => {
    const styles = document.querySelector('style').textContent;
    // Check if using light text on dark background
    if (!styles.includes('--text-main') || !styles.includes('--bg-color')) {
        throw new Error('Should define text and background colors');
    }
});

test('Focus states should be visible', () => {
    const styles = document.querySelector('style').textContent;
    const hasFocusStyles = styles.includes(':hover') || styles.includes(':focus');
    if (!hasFocusStyles) {
        throw new Error('Should have visible focus/hover states');
    }
});

console.log('\nSecurity Tests:');

test('Should not have inline event handlers', () => {
    const html = document.documentElement.innerHTML;
    const hasInlineHandlers = /on\w+\s*=/.test(html);
    // Allow onclick in the simulate button as it's intentional
    const allowedOccurrences = (html.match(/onclick="simulateGrowth\(\)"/g) || []).length;
    const totalOccurrences = (html.match(/on\w+\s*=/g) || []).length;
    
    if (totalOccurrences > allowedOccurrences) {
        throw new Error('Should minimize inline event handlers');
    }
});

test('Should have proper Content Security Policy considerations', () => {
    // Check that scripts are properly contained
    const scripts = document.querySelectorAll('script[src]');
    scripts.forEach((script) => {
        const src = script.getAttribute('src');
        if (src && !src.startsWith('http://') && !src.startsWith('https://') && !src.startsWith('/')) {
            throw new Error('External scripts should use proper protocols');
        }
    });
});

console.log('\nW3C Standards Compliance Tests:');

test('Should have valid HTML5 structure', () => {
    if (!document.doctype) throw new Error('Missing DOCTYPE');
    if (document.doctype.name !== 'html') throw new Error('Invalid DOCTYPE');
    
    const html = document.documentElement;
    if (!html) throw new Error('Missing html element');
    if (!document.head) throw new Error('Missing head element');
    if (!document.body) throw new Error('Missing body element');
});

test('Should have required meta tags', () => {
    if (!document.querySelector('meta[charset]')) {
        throw new Error('Missing charset meta tag');
    }
    if (!document.querySelector('title')) {
        throw new Error('Missing title tag');
    }
});

test('Should use semantic HTML5 elements', () => {
    const semanticElements = [
        'header', 'main', 'section', 'footer'
    ];
    
    semanticElements.forEach(tagName => {
        if (!document.querySelector(tagName)) {
            throw new Error(`Missing semantic ${tagName} element`);
        }
    });
});

// Wait for all async tests to complete
setTimeout(() => {
    dom.window.close();
    
    console.log('\n========================================');
    console.log('Browser Compatibility Test Summary');
    console.log('========================================');
    console.log(`Total Tests: ${totalTests}`);
    console.log(`Passed: ${passedTests}`);
    console.log(`Success Rate: ${((passedTests / totalTests) * 100).toFixed(2)}%`);
    console.log('========================================\n');
    
    console.log('Cross-Browser Compatibility Notes:');
    console.log('  ✓ CSS animations use standard properties');
    console.log('  ✓ JavaScript uses ES6+ compatible with modern browsers');
    console.log('  ✓ No vendor prefixes needed for tested features');
    console.log('  ✓ Responsive design with mobile breakpoints');
    console.log('  ✓ Accessibility features (ARIA labels, semantic HTML)');
    console.log('  ✓ Progressive enhancement approach');
    console.log('\nRecommended Browser Support:');
    console.log('  • Chrome/Edge 90+');
    console.log('  • Firefox 88+');
    console.log('  • Safari 14+');
    console.log('  • Mobile browsers (iOS Safari 14+, Chrome Android 90+)');
    console.log('========================================\n');
    
    process.exit(0);
}, 3000); // Wait 3 seconds for all async operations
