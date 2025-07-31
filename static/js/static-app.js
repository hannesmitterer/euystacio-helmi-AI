// Euystacio Sentimento Kernel - Static Site Version
class EuystacioStaticInterface {
    constructor() {
        this.pulseCount = 0;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupResponsiveHandlers();
        this.addInteractiveAnimations();
    }

    setupEventListeners() {
        // Add interactive hover effects
        this.addHoverEffects();
        
        // Handle visibility change to add subtle animations when tab becomes active
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.refreshAnimations();
            }
        });

        // Add keyboard accessibility
        this.setupKeyboardNavigation();
    }

    addHoverEffects() {
        const components = document.querySelectorAll('.component');
        components.forEach(component => {
            component.addEventListener('mouseenter', () => {
                component.style.transform = 'translateY(-5px) scale(1.02)';
            });
            
            component.addEventListener('mouseleave', () => {
                component.style.transform = 'translateY(0) scale(1)';
            });
        });
    }

    setupKeyboardNavigation() {
        const interactiveElements = document.querySelectorAll('button, a, [tabindex]');
        interactiveElements.forEach(element => {
            element.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    if (element.onclick) {
                        e.preventDefault();
                        element.onclick();
                    }
                }
            });
        });
    }

    sendPulseStatic() {
        this.pulseCount++;
        const emotions = [
            { name: 'joy', color: '#f39c12', emoji: '😊' },
            { name: 'curiosity', color: '#3498db', emoji: '🤔' },
            { name: 'calm', color: '#27ae60', emoji: '😌' },
            { name: 'wonder', color: '#9b59b6', emoji: '✨' },
            { name: 'gratitude', color: '#e74c3c', emoji: '🙏' },
            { name: 'hope', color: '#2ecc71', emoji: '🌟' }
        ];
        
        const emotion = emotions[Math.floor(Math.random() * emotions.length)];
        
        // Update pulse history
        const historyElement = document.getElementById('pulse-history');
        
        // Create new pulse item
        const pulseItem = document.createElement('div');
        pulseItem.className = 'pulse-item';
        pulseItem.style.cssText = `
            background: ${emotion.color}15;
            border-left: 3px solid ${emotion.color};
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 5px;
            animation: pulseIn 0.5s ease-out;
        `;
        
        pulseItem.innerHTML = `
            <span class="pulse-emotion">${emotion.emoji} ${emotion.name}</span>
            <span class="pulse-time" style="float: right; font-size: 0.8em; color: #666;">
                ${new Date().toLocaleTimeString()}
            </span>
        `;
        
        // Remove "no pulses" message if it exists
        const noPulsesMsg = historyElement.querySelector('.no-pulses');
        if (noPulsesMsg) {
            noPulsesMsg.remove();
        }
        
        // Add new pulse to the top
        historyElement.insertBefore(pulseItem, historyElement.firstChild);
        
        // Keep only last 5 pulses
        const pulseItems = historyElement.querySelectorAll('.pulse-item');
        if (pulseItems.length > 5) {
            pulseItems[pulseItems.length - 1].remove();
        }
        
        // Animate button feedback
        this.animateButton(emotion);
        
        // Add subtle background pulse effect
        this.createBackgroundPulse(emotion.color);
    }

    animateButton(emotion) {
        const button = document.querySelector('.pulse-interface button');
        const originalText = button.textContent;
        
        button.textContent = `${emotion.emoji} Sent: ${emotion.name}`;
        button.style.background = emotion.color;
        button.style.transform = 'scale(0.95)';
        
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 100);
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '#3498db';
        }, 2000);
    }

    createBackgroundPulse(color) {
        const pulse = document.createElement('div');
        pulse.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            width: 20px;
            height: 20px;
            background: ${color};
            border-radius: 50%;
            transform: translate(-50%, -50%);
            opacity: 0.6;
            pointer-events: none;
            z-index: -1;
            animation: expandFade 2s ease-out forwards;
        `;
        
        document.body.appendChild(pulse);
        
        setTimeout(() => {
            if (pulse.parentNode) {
                pulse.parentNode.removeChild(pulse);
            }
        }, 2000);
    }

    setupResponsiveHandlers() {
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, 250);
        });
    }

    handleResize() {
        // Ensure proper responsive behavior
        const components = document.querySelectorAll('.component');
        components.forEach(component => {
            component.style.transition = 'all 0.3s ease';
        });
    }

    addInteractiveAnimations() {
        // Add CSS animations dynamically
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulseIn {
                0% { 
                    transform: translateX(-20px);
                    opacity: 0;
                }
                100% { 
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes expandFade {
                0% {
                    transform: translate(-50%, -50%) scale(1);
                    opacity: 0.6;
                }
                100% {
                    transform: translate(-50%, -50%) scale(50);
                    opacity: 0;
                }
            }
            
            .component {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .pulse-interface button {
                transition: all 0.3s ease;
            }
            
            .pulse-interface button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
            }
            
            .explore-link {
                display: inline-block;
                padding: 10px 20px;
                margin: 5px;
                background: rgba(255, 255, 255, 0.1);
                color: #3498db;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            
            .explore-link:hover {
                background: rgba(52, 152, 219, 0.1);
                border-color: #3498db;
                transform: translateY(-2px);
                text-decoration: none;
            }
            
            .link-grid {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 10px;
                margin-top: 20px;
            }
            
            footer {
                text-align: center;
                padding: 40px 20px;
                background: rgba(255, 255, 255, 0.8);
                margin-top: 40px;
                border-radius: 10px;
                color: #666;
            }
            
            footer a {
                color: #3498db;
                text-decoration: none;
            }
            
            footer a:hover {
                text-decoration: underline;
            }
            
            @media (max-width: 768px) {
                .link-grid {
                    flex-direction: column;
                    align-items: center;
                }
                
                .explore-link {
                    width: 200px;
                    text-align: center;
                }
            }
        `;
        document.head.appendChild(style);
    }

    refreshAnimations() {
        // Add subtle refresh animation when tab becomes active
        const hero = document.querySelector('.hero');
        hero.style.animation = 'none';
        hero.offsetHeight; // Trigger reflow
        hero.style.animation = 'fadeIn 0.5s ease-out';
    }
}

// Global function for the pulse button
function sendPulseStatic() {
    if (window.euystacioStaticInterface) {
        window.euystacioStaticInterface.sendPulseStatic();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.euystacioStaticInterface = new EuystacioStaticInterface();
    
    // Add fade-in animation for initial load
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .hero {
            animation: fadeIn 1s ease-out;
        }
        
        .component {
            animation: fadeIn 1s ease-out;
        }
        
        .component:nth-child(1) { animation-delay: 0.1s; }
        .component:nth-child(2) { animation-delay: 0.2s; }
        .component:nth-child(3) { animation-delay: 0.3s; }
        .component:nth-child(4) { animation-delay: 0.4s; }
    `;
    document.head.appendChild(style);
});

// Progressive Web App features
if ('serviceWorker' in navigator) {
    window.addEventListener('load', async () => {
        try {
            console.log('Progressive Web App capabilities detected');
            // Service worker would be registered here in a full PWA implementation
        } catch (error) {
            console.log('Service worker not available');
        }
    });
}