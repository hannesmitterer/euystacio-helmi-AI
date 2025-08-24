// Euystacio Altar - Dynamic Interactive Experience
class EuystacioAltar {
  constructor() {
    this.guardianState = 'soothe'; // default state
    this.consensusData = null;
    this.presenceActive = false;
    this.lastInteraction = Date.now();
    this.baseURL = window.location.origin;
    
    this.init();
  }

  async init() {
    console.log('🌳 Initializing Euystacio Altar...');
    
    // Load initial data
    await this.loadConsensusData();
    await this.loadGuardianState();
    
    // Setup event listeners
    this.setupPresenceDetection();
    this.setupGuardianControls();
    this.setupKeyboardControls();
    
    // Start presence monitoring
    this.startPresenceMonitoring();
    
    // Initial render
    this.renderConsensusTopics();
    this.updateGuardianDisplay();
    
    console.log('✨ Altar initialized successfully');
  }

  // Presence Detection System
  setupPresenceDetection() {
    const orb = document.querySelector('.presence-orb');
    const container = document.querySelector('.altar-container');
    
    if (!orb || !container) return;

    // Mouse/pointer events
    orb.addEventListener('mouseenter', () => this.onPresenceDetected('hover'));
    orb.addEventListener('mouseleave', () => this.onPresenceEnded('hover'));
    orb.addEventListener('click', (e) => this.onPresenceDetected('click', e));
    orb.addEventListener('mousemove', () => this.onPresenceDetected('movement'));

    // Touch events
    orb.addEventListener('touchstart', (e) => {
      e.preventDefault();
      this.onPresenceDetected('touch', e);
    });
    orb.addEventListener('touchend', () => this.onPresenceEnded('touch'));

    // Global mouse movement for ambient awareness
    container.addEventListener('mousemove', (e) => {
      this.onPresenceDetected('ambient', e);
    });
  }

  setupKeyboardControls() {
    document.addEventListener('keydown', (e) => {
      switch(e.key.toLowerCase()) {
        case 'a':
          this.setGuardianState('awaken');
          this.onPresenceDetected('keyboard');
          break;
        case 's':
          this.setGuardianState('soothe');
          this.onPresenceDetected('keyboard');
          break;
        case ' ':
          e.preventDefault();
          this.triggerPresencePulse();
          break;
        case 'r':
          this.refreshConsensusData();
          break;
      }
    });
  }

  setupGuardianControls() {
    const awakenBtn = document.querySelector('.guardian-toggle.awaken');
    const sootheBtn = document.querySelector('.guardian-toggle.soothe');

    if (awakenBtn) {
      awakenBtn.addEventListener('click', () => {
        this.setGuardianState('awaken');
        this.onPresenceDetected('guardian_toggle');
      });
    }

    if (sootheBtn) {
      sootheBtn.addEventListener('click', () => {
        this.setGuardianState('soothe');
        this.onPresenceDetected('guardian_toggle');
      });
    }
  }

  // Presence Detection Handlers
  onPresenceDetected(type, event = null) {
    this.lastInteraction = Date.now();
    this.presenceActive = true;

    // Visual feedback
    this.triggerPresencePulse(type);
    
    // Create ripple effect for click/touch
    if ((type === 'click' || type === 'touch') && event) {
      this.createRippleEffect(event);
    }

    // Log the presence event
    this.logPresenceEvent(type);
  }

  onPresenceEnded(type) {
    // Only end presence if no recent interactions
    setTimeout(() => {
      if (Date.now() - this.lastInteraction > 1000) {
        this.presenceActive = false;
        this.updatePresenceDisplay();
      }
    }, 1000);
  }

  triggerPresencePulse(type = 'general') {
    const orb = document.querySelector('.presence-orb');
    if (!orb) return;

    // Add pulsing animation
    orb.classList.add('pulsing');
    
    // Adjust intensity based on interaction type
    if (type === 'click' || type === 'touch') {
      orb.style.transform = 'scale(1.1)';
      setTimeout(() => {
        orb.style.transform = '';
      }, 200);
    }

    // Remove pulsing after animation
    setTimeout(() => {
      orb.classList.remove('pulsing');
    }, 2000);
  }

  createRippleEffect(event) {
    const orb = document.querySelector('.presence-orb');
    if (!orb) return;

    const ripple = document.createElement('div');
    ripple.className = 'ripple-effect';
    
    const rect = orb.getBoundingClientRect();
    const size = 30;
    const x = (event.clientX || event.touches[0].clientX) - rect.left - size/2;
    const y = (event.clientY || event.touches[0].clientY) - rect.top - size/2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    
    orb.appendChild(ripple);
    
    setTimeout(() => {
      ripple.remove();
    }, 600);
  }

  // Guardian State Management
  async setGuardianState(newState) {
    if (this.guardianState === newState) return;

    this.guardianState = newState;
    this.updateGuardianDisplay();
    
    // Persist to backend if available
    try {
      await this.saveGuardianState(newState);
    } catch (error) {
      console.log('Could not persist guardian state to backend:', error.message);
    }

    // Visual feedback for state change
    this.showStateTransition(newState);
  }

  updateGuardianDisplay() {
    const awakenBtn = document.querySelector('.guardian-toggle.awaken');
    const sootheBtn = document.querySelector('.guardian-toggle.soothe');
    const orb = document.querySelector('.presence-orb');
    const symbol = document.querySelector('.orb-symbol');

    if (!awakenBtn || !sootheBtn || !orb || !symbol) return;

    // Update button states
    awakenBtn.classList.toggle('active', this.guardianState === 'awaken');
    sootheBtn.classList.toggle('active', this.guardianState === 'soothe');

    // Update orb appearance
    if (this.guardianState === 'awaken') {
      orb.style.background = 'radial-gradient(circle at 30% 30%, var(--altar-guardian-awaken), var(--altar-primary))';
      symbol.textContent = '⚡';
      orb.style.boxShadow = '0 0 40px rgba(255, 107, 107, 0.4), inset 0 0 60px rgba(255, 255, 255, 0.1)';
    } else {
      orb.style.background = 'radial-gradient(circle at 30% 30%, var(--altar-pulse-active), var(--altar-primary))';
      symbol.textContent = '🌸';
      orb.style.boxShadow = '0 0 40px rgba(78, 205, 196, 0.4), inset 0 0 60px rgba(255, 255, 255, 0.1)';
    }
  }

  showStateTransition(newState) {
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: rgba(42, 42, 42, 0.95);
      color: var(--altar-text-light);
      padding: 15px 20px;
      border-radius: 8px;
      border-left: 4px solid ${newState === 'awaken' ? 'var(--altar-guardian-awaken)' : 'var(--altar-guardian-soothe)'};
      z-index: 1000;
      animation: slideInRight 0.3s ease;
    `;
    notification.textContent = `Guardian state: ${newState.toUpperCase()}`;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = 'slideOutRight 0.3s ease forwards';
      setTimeout(() => notification.remove(), 300);
    }, 2000);
  }

  // Consensus Data Management
  async loadConsensusData() {
    try {
      const response = await fetch(`${this.baseURL}/altar/consensus.json`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      this.consensusData = await response.json();
      console.log('📊 Consensus data loaded:', this.consensusData.topics.length, 'topics');
    } catch (error) {
      console.log('Using fallback consensus data due to:', error.message);
      this.consensusData = this.getFallbackConsensusData();
    }
  }

  getFallbackConsensusData() {
    return {
      topics: [
        {
          id: "sample_topic",
          title: "Sample Consensus Topic",
          description: "This is demonstration data for the altar interface",
          quorum_required: 5,
          current_consensus: 3,
          status: "active",
          guardian_relevance: "both"
        }
      ],
      active_participants: 8,
      global_quorum_threshold: 0.6,
      last_updated: new Date().toISOString()
    };
  }

  renderConsensusTopics() {
    const container = document.querySelector('.consensus-topics');
    const statsContainer = document.querySelector('.consensus-stats');
    
    if (!container || !this.consensusData) return;

    // Update stats
    if (statsContainer) {
      statsContainer.innerHTML = `
        <div>Topics: ${this.consensusData.topics.length}</div>
        <div>Participants: ${this.consensusData.active_participants}</div>
        <div>Threshold: ${(this.consensusData.global_quorum_threshold * 100).toFixed(0)}%</div>
      `;
    }

    // Render topics
    container.innerHTML = this.consensusData.topics.map(topic => {
      const progress = (topic.current_consensus / topic.quorum_required) * 100;
      const isReached = topic.status === 'reached';
      
      return `
        <div class="consensus-topic ${isReached ? 'reached' : ''}" data-topic-id="${topic.id}">
          <div class="topic-header">
            <h4 class="topic-title">${topic.title}</h4>
            <span class="topic-status ${topic.status}">${topic.status.toUpperCase()}</span>
          </div>
          <p class="topic-description">${topic.description}</p>
          <div class="topic-progress">
            <div class="progress-bar">
              <div class="progress-fill" style="width: ${Math.min(progress, 100)}%"></div>
            </div>
            <span class="progress-text">${topic.current_consensus}/${topic.quorum_required}</span>
          </div>
        </div>
      `;
    }).join('');

    // Add click handlers for topics
    container.querySelectorAll('.consensus-topic').forEach(topic => {
      topic.addEventListener('click', () => {
        const topicId = topic.dataset.topicId;
        this.onTopicInteraction(topicId);
      });
    });
  }

  onTopicInteraction(topicId) {
    const topic = this.consensusData.topics.find(t => t.id === topicId);
    if (!topic) return;

    this.onPresenceDetected('consensus_interaction');
    
    // Show topic details
    const modal = this.createTopicModal(topic);
    document.body.appendChild(modal);
  }

  createTopicModal(topic) {
    const modal = document.createElement('div');
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      animation: fadeIn 0.3s ease;
    `;

    const content = document.createElement('div');
    content.style.cssText = `
      background: var(--altar-bg-light);
      padding: 30px;
      border-radius: 15px;
      max-width: 500px;
      width: 90%;
      color: var(--altar-text-light);
    `;

    content.innerHTML = `
      <h3 style="color: var(--altar-accent); margin-bottom: 15px;">${topic.title}</h3>
      <p style="margin-bottom: 20px; line-height: 1.6;">${topic.description}</p>
      <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
        <span>Progress: ${topic.current_consensus}/${topic.quorum_required}</span>
        <span>Status: ${topic.status.toUpperCase()}</span>
      </div>
      <div style="display: flex; justify-content: space-between;">
        <span>Guardian: ${topic.guardian_relevance}</span>
        <button id="close-modal" style="
          background: var(--altar-accent);
          border: none;
          padding: 8px 16px;
          border-radius: 6px;
          color: white;
          cursor: pointer;
        ">Close</button>
      </div>
    `;

    modal.appendChild(content);

    // Close handlers
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.remove();
    });
    
    content.querySelector('#close-modal').addEventListener('click', () => {
      modal.remove();
    });

    return modal;
  }

  // Backend Integration
  async loadGuardianState() {
    try {
      const response = await fetch(`${this.baseURL}/api/red_code`);
      if (response.ok) {
        const redCode = await response.json();
        this.guardianState = redCode.guardian_mode ? 'awaken' : 'soothe';
        console.log('🛡️ Guardian state loaded:', this.guardianState);
      }
    } catch (error) {
      console.log('Could not load guardian state from backend:', error.message);
    }
  }

  async saveGuardianState(state) {
    const response = await fetch(`${this.baseURL}/api/guardian_state`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guardian_mode: state === 'awaken' })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
  }

  async refreshConsensusData() {
    console.log('🔄 Refreshing consensus data...');
    const container = document.querySelector('.consensus-section');
    if (container) container.classList.add('loading');
    
    await this.loadConsensusData();
    this.renderConsensusTopics();
    
    if (container) container.classList.remove('loading');
    this.onPresenceDetected('data_refresh');
  }

  // Presence Monitoring
  startPresenceMonitoring() {
    setInterval(() => {
      const timeSinceLastInteraction = Date.now() - this.lastInteraction;
      
      // Auto-refresh consensus data every 5 minutes
      if (timeSinceLastInteraction > 300000) {
        this.refreshConsensusData();
      }
      
      // Update presence display
      this.updatePresenceDisplay();
    }, 10000);
  }

  updatePresenceDisplay() {
    const orb = document.querySelector('.presence-orb');
    if (!orb) return;

    const timeSinceLastInteraction = Date.now() - this.lastInteraction;
    
    if (timeSinceLastInteraction < 5000) {
      orb.style.opacity = '1';
    } else if (timeSinceLastInteraction < 30000) {
      orb.style.opacity = '0.8';
    } else {
      orb.style.opacity = '0.6';
    }
  }

  // Utility Methods
  logPresenceEvent(type) {
    console.log(`👁️ Presence detected: ${type} at ${new Date().toLocaleTimeString()}`);
  }
}

// Additional CSS animations via JavaScript
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOutRight {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
`;
document.head.appendChild(style);

// Initialize altar when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.altar = new EuystacioAltar();
});

// Keyboard shortcuts info
console.log(`
🌳 Euystacio Altar Keyboard Controls:
- 'A' key: Set guardian to AWAKEN
- 'S' key: Set guardian to SOOTHE  
- SPACE: Trigger presence pulse
- 'R' key: Refresh consensus data
`);