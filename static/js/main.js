// Main JavaScript for Euystacio Dashboard

// Animation and interaction enhancements
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    setupInteractionTracking();
    setupAccessibility();
});

function initializeAnimations() {
    // Animate pulse items when they appear
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    // Observe pulse items for animation
    document.querySelectorAll('.pulse-item, .tutor-item, .reflection-item').forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(item);
    });
}

function setupInteractionTracking() {
    // Track which sections users interact with most
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.addEventListener('mouseenter', () => {
            window.EuystacioConsent?.trackLearningEvent('section_hover', {
                section: section.className || section.tagName
            });
        });
    });

    // Track form interactions
    const formElements = document.querySelectorAll('input, select, textarea');
    formElements.forEach(element => {
        element.addEventListener('focus', () => {
            window.EuystacioConsent?.trackLearningEvent('form_interaction', {
                element: element.name || element.id,
                type: 'focus'
            });
        });
    });
}

function setupAccessibility() {
    // Add keyboard navigation for custom elements
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                button.click();
            }
        });
    });

    // Add aria labels for better screen reader support
    const pulseItems = document.querySelectorAll('.pulse-item');
    pulseItems.forEach((item, index) => {
        item.setAttribute('aria-label', `Emotional pulse ${index + 1}`);
    });

    const tutorItems = document.querySelectorAll('.tutor-item');
    tutorItems.forEach((item, index) => {
        item.setAttribute('aria-label', `Guardian nomination ${index + 1}`);
    });
}

// Enhanced form validation
function validatePulseForm() {
    const emotion = document.getElementById('emotion').value;
    const intensity = document.getElementById('intensity').value;
    
    if (!emotion) {
        showValidationError('Please select an emotion to share with Euystacio.');
        return false;
    }
    
    if (intensity < 0 || intensity > 1) {
        showValidationError('Intensity must be between 0 and 1.');
        return false;
    }
    
    return true;
}

function showValidationError(message) {
    window.EuystacioConsent?.showNotification(message, 'error');
}

// Real-time dashboard updates
function setupRealTimeUpdates() {
    // Update dashboard every 30 seconds if user is active
    let lastActivity = Date.now();
    let updateInterval;

    function updateActivity() {
        lastActivity = Date.now();
    }

    // Track user activity
    ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
        document.addEventListener(event, updateActivity, true);
    });

    function checkForUpdates() {
        const timeSinceActivity = Date.now() - lastActivity;
        
        // Only update if user was active in the last 5 minutes
        if (timeSinceActivity < 5 * 60 * 1000) {
            refreshDashboardData();
        }
    }

    // Start update interval
    updateInterval = setInterval(checkForUpdates, 30000);

    // Clear interval when page is hidden
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            clearInterval(updateInterval);
        } else {
            updateInterval = setInterval(checkForUpdates, 30000);
        }
    });
}

async function refreshDashboardData() {
    try {
        // Refresh red code data
        await loadRedCode();
        
        // Refresh pulses (only if new ones exist)
        const currentPulseCount = document.querySelectorAll('.pulse-item').length;
        await loadPulses();
        const newPulseCount = document.querySelectorAll('.pulse-item').length;
        
        if (newPulseCount > currentPulseCount) {
            window.EuystacioConsent?.showNotification('New emotional pulses received!', 'info');
        }
        
        // Refresh reflections
        await loadReflections();
        
    } catch (error) {
        console.error('Error refreshing dashboard data:', error);
    }
}

// Emotional state visualization
function updateEmotionalVisualization(emotion, intensity) {
    const indicator = document.getElementById('current-emotion');
    if (indicator) {
        // Map emotions to emojis and colors
        const emotionMap = {
            hope: { emoji: '🌟', color: '#ffd700' },
            wonder: { emoji: '✨', color: '#87ceeb' },
            trust: { emoji: '🤝', color: '#90ee90' },
            love: { emoji: '💚', color: '#ff69b4' },
            humility: { emoji: '🙏', color: '#dda0dd' },
            curiosity: { emoji: '🔍', color: '#ffa500' },
            concern: { emoji: '😟', color: '#ffa07a' },
            gratitude: { emoji: '🙏', color: '#98fb98' }
        };
        
        const emotionData = emotionMap[emotion] || { emoji: '🌱', color: '#90ee90' };
        
        indicator.innerHTML = `${emotionData.emoji} ${emotion}`;
        indicator.style.backgroundColor = emotionData.color;
        indicator.style.opacity = intensity;
        
        // Add pulse animation
        indicator.style.animation = 'pulse 1s ease-in-out';
        setTimeout(() => {
            indicator.style.animation = '';
        }, 1000);
    }
}

// Add CSS animation for pulse effect
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .notification.error {
        background: #e74c3c;
    }
    
    .notification.info {
        background: #3498db;
    }
`;
document.head.appendChild(style);

// Initialize real-time updates if on dashboard
if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
    document.addEventListener('DOMContentLoaded', setupRealTimeUpdates);
}

// Enhanced pulse form handling
document.addEventListener('DOMContentLoaded', function() {
    const pulseForm = document.getElementById('pulse-form');
    if (pulseForm) {
        pulseForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!validatePulseForm()) {
                return;
            }
            
            const formData = new FormData(e.target);
            const emotion = formData.get('emotion');
            const intensity = parseFloat(formData.get('intensity'));
            
            // Update visualization immediately for responsiveness
            updateEmotionalVisualization(emotion, intensity);
            
            // Continue with original form submission logic
            await sendPulse(e);
        });
    }
});

// Export functions for global use
window.EuystacioMain = {
    updateEmotionalVisualization,
    refreshDashboardData,
    validatePulseForm
};