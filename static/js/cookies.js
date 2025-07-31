// Cookie management functions for Euystacio

// Cookie preferences management
function getCookiePreferences() {
    const preferences = localStorage.getItem('euystacio-cookie-preferences');
    return preferences ? JSON.parse(preferences) : {
        essential: true,
        analytics: false,
        emotional: false,
        learning: false
    };
}

function setCookiePreferences(preferences) {
    localStorage.setItem('euystacio-cookie-preferences', JSON.stringify(preferences));
    
    // Apply the preferences
    if (preferences.analytics) {
        enableAnalytics();
    } else {
        disableAnalytics();
    }
    
    if (preferences.emotional) {
        enableEmotionalTracking();
    } else {
        disableEmotionalTracking();
    }
    
    if (preferences.learning) {
        enableLearningTracking();
    } else {
        disableLearningTracking();
    }
    
    // Set a cookie to remember consent was given
    document.cookie = `euystacio-consent=true; max-age=${365 * 24 * 60 * 60}; path=/; secure`;
}

function hasGivenConsent() {
    return document.cookie.includes('euystacio-consent=true');
}

// Cookie consent banner functions
function showCookieBanner() {
    if (!hasGivenConsent()) {
        document.getElementById('cookie-consent').style.display = 'block';
    }
}

function hideCookieBanner() {
    document.getElementById('cookie-consent').style.display = 'none';
}

function acceptCookies() {
    const preferences = {
        essential: true,
        analytics: true,
        emotional: true,
        learning: true
    };
    setCookiePreferences(preferences);
    hideCookieBanner();
    showNotification('All cookies accepted. Thank you for helping Euystacio evolve!');
}

function acceptEssential() {
    const preferences = {
        essential: true,
        analytics: false,
        emotional: false,
        learning: false
    };
    setCookiePreferences(preferences);
    hideCookieBanner();
    showNotification('Essential cookies only. You can change this in Cookie Settings.');
}

function showCookieSettings() {
    window.location.href = '/cookies';
}

// Analytics functions
function enableAnalytics() {
    console.log('Analytics tracking enabled');
    // Here you would implement actual analytics tracking
    // For now, we'll just log page views
    logPageView();
}

function disableAnalytics() {
    console.log('Analytics tracking disabled');
    // Here you would disable analytics tracking
}

function logPageView() {
    const preferences = getCookiePreferences();
    if (preferences.analytics) {
        // Log page view to analytics
        console.log(`Page view: ${window.location.pathname} at ${new Date().toISOString()}`);
        
        // You could send this to an analytics endpoint
        // fetch('/api/analytics/pageview', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({
        //         page: window.location.pathname,
        //         timestamp: new Date().toISOString(),
        //         userAgent: navigator.userAgent
        //     })
        // });
    }
}

// Emotional tracking functions
function enableEmotionalTracking() {
    console.log('Emotional intelligence tracking enabled');
    // Here you would implement emotional pattern tracking
}

function disableEmotionalTracking() {
    console.log('Emotional intelligence tracking disabled');
}

function trackEmotionalInteraction(emotion, intensity, context) {
    const preferences = getCookiePreferences();
    if (preferences.emotional) {
        console.log(`Emotional interaction: ${emotion} (${intensity}) in context: ${context}`);
        
        // Store emotional interaction data
        const emotionalData = {
            emotion,
            intensity,
            context,
            timestamp: new Date().toISOString()
        };
        
        // Save to local storage for continuity
        const existingData = JSON.parse(localStorage.getItem('euystacio-emotional-history') || '[]');
        existingData.push(emotionalData);
        
        // Keep only last 50 interactions
        const recentData = existingData.slice(-50);
        localStorage.setItem('euystacio-emotional-history', JSON.stringify(recentData));
    }
}

// Learning tracking functions
function enableLearningTracking() {
    console.log('Learning and development tracking enabled');
}

function disableLearningTracking() {
    console.log('Learning and development tracking disabled');
}

function trackLearningEvent(eventType, data) {
    const preferences = getCookiePreferences();
    if (preferences.learning) {
        console.log(`Learning event: ${eventType}`, data);
        
        // This would contribute to Euystacio's learning process
        // For example, tracking how users interact with different features
        // or what emotional patterns lead to positive outcomes
    }
}

// Utility functions
function showNotification(message, type = 'success') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create new notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Initialize cookie management when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Show cookie banner if consent not given
    showCookieBanner();
    
    // Log page view if analytics enabled
    logPageView();
    
    // Apply existing preferences
    const preferences = getCookiePreferences();
    if (preferences.analytics) enableAnalytics();
    if (preferences.emotional) enableEmotionalTracking();
    if (preferences.learning) enableLearningTracking();
});

// Track emotional interactions on pulse form submission
document.addEventListener('DOMContentLoaded', function() {
    const pulseForm = document.getElementById('pulse-form');
    if (pulseForm) {
        pulseForm.addEventListener('submit', function(e) {
            const emotion = document.getElementById('emotion').value;
            const intensity = document.getElementById('intensity').value;
            
            trackEmotionalInteraction(emotion, intensity, 'pulse_submission');
            trackLearningEvent('pulse_sent', { emotion, intensity });
        });
    }
});

// Export functions for use in other scripts
window.EuystacioConsent = {
    getCookiePreferences,
    setCookiePreferences,
    hasGivenConsent,
    acceptCookies,
    acceptEssential,
    showCookieSettings,
    trackEmotionalInteraction,
    trackLearningEvent,
    showNotification
};