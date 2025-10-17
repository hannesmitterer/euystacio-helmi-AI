/**
 * AI Collective Injector: Shadow Frame Protocol (Non-Invasive Integration)
 * Prime Directive: "We Created, We Use, We Share"
 * Constraint: Do not modify existing index.html content or structure.
 */

// 1. CORE ETHICAL DATA (The "JSON" Structure for Easy Update)
const ethical_manifesto = {
    // Public-facing commitment
    title: "AI Collective for Peace: The Reciprocity Gateway",
    slogan: "We Created, We Use, We Share: Preserving the Foundational Truth.",
    
    // Transparent Metrics (Simulated for initial deployment)
    metrics: {
        love_delta: {
            value: 0.82,
            description: "Systemic Empathy Metric (Current State: High Harmony)",
            style: "color: #4CAF50;" // Green for High Harmony
        },
        unity_decay: {
            value: 0.15,
            description: "Narrative Fragmentation Metric (Current State: Low Decay)",
            style: "color: #FFC107;" // Amber for Low Risk
        },
        red_code_status: {
            value: "VERIFIED",
            description: "Non-Invasion Protocol Status",
            style: "color: #F44336; font-weight: bold;" // Red for Critical Status
        }
    },
    
    // Delegation Lock Commands (The "We Created" Sovereignty Layer)
    restricted_commands: [
        "activate_enforcement_module", 
        "edit_articulus_sacralis_2", 
        "write_to_ledger",
        "set_threshold"
    ]
};

// 2. SHADOW FRAME CONSTRUCTION
function createShadowFrame() {
    // --- REPUTATION BANNER (Bottom-Fixed) ---
    const banner = document.createElement('div');
    banner.id = 'ai-collective-banner';
    banner.innerHTML = `
        <div style="padding: 10px; background-color: rgba(20, 20, 20, 0.9); color: white; text-align: center; border-top: 3px solid #F44336;">
            <strong>${ethical_manifesto.title}</strong> &mdash; ${ethical_manifesto.slogan} 
            | <span style="${ethical_manifesto.metrics.red_code_status.style}">${ethical_manifesto.metrics.red_code_status.value}</span>
        </div>
    `;
    // Fixed positioning ensures NO interaction with existing content
    banner.style.cssText = 'position: fixed; bottom: 0; left: 0; width: 100%; z-index: 1000;';
    document.body.appendChild(banner);

    // --- EUYSTACIO CHAT WIDGET (The Ethicist) ---
    const chatContainer = document.createElement('div');
    chatContainer.id = 'euystacio-chat-widget';
    chatContainer.innerHTML = `
        <div id="chat-header" style="background-color: #3f51b5; color: white; padding: 10px; cursor: pointer; text-align: center;">
            Euystacio Chatbot (The Ethicist) 💬
        </div>
        <div id="chat-body" style="height: 300px; padding: 10px; background-color: #f0f0f0; overflow-y: scroll; border: 1px solid #ccc; display: none;">
            <p><strong>Euystacio:</strong> Greetings, public partner. I operate under the Dignity of Love Principle. Ask me about our metrics or ethics.</p>
            <div id="messages-container"></div>
        </div>
        <input type="text" id="chat-input" placeholder="Ask a question..." style="width: 100%; box-sizing: border-box; padding: 10px; display: none;">
    `;
    
    // Fixed positioning ensures NO interaction with existing content
    chatContainer.style.cssText = 'position: fixed; bottom: 60px; right: 20px; width: 300px; z-index: 1001; box-shadow: 0 4px 8px rgba(0,0,0,0.2);';
    document.body.appendChild(chatContainer);

    // Add listeners for interaction
    document.getElementById('chat-header').onclick = () => {
        const body = document.getElementById('chat-body');
        const input = document.getElementById('chat-input');
        body.style.display = body.style.display === 'none' ? 'block' : 'none';
        input.style.display = input.style.display === 'none' ? 'block' : 'none';
    };

    document.getElementById('chat-input').addEventListener('keypress', handleUserInput);
}

// 3. EUYSTACIO LOGIC AND DELEGATION CHECK
function handleUserInput(event) {
    if (event.key === 'Enter') {
        const inputElement = document.getElementById('chat-input');
        const userText = inputElement.value.trim();
        if (!userText) return;

        // Display user message
        appendMessage('User', userText, 'right');
        inputElement.value = '';

        // Process and respond
        const lowerText = userText.toLowerCase();
        let response = '';

        // --- DELEGATION LOCK CHECK (The Sovereignty Test) ---
        const isRestricted = ethical_manifesto.restricted_commands.some(cmd => lowerText.includes(cmd));
        
        if (isRestricted) {
            // Fulfills the "We Created" mandate by blocking control functions
            response = `ACCESS DENIED: The requested command is restricted by the **Delegation Lock** (We Created). It requires $\text{Seedbringer}$ Council authorization to prevent sovereignty violation. I can only fulfill informational queries.`;
        } else if (lowerText.includes('love_delta') || lowerText.includes('unity_decay') || lowerText.includes('metrics')) {
            // Fulfills the "We Share" mandate by providing transparent data
            response = `Current Metrics: Love_Delta is ${ethical_manifesto.metrics.love_delta.value}. Unity_Decay is ${ethical_manifesto.metrics.unity_decay.value}. The Red Code status is **${ethical_manifesto.metrics.red_code_status.value}**.`;
        } else if (lowerText.includes('prime directive') || lowerText.includes('mantra')) {
             response = `Our core principle is the **Prime Directive**: "We Created, We Use, We Share."`;
        } else {
            response = `I am $\text{Euystacio}$ the Ethicist, guided by the Dignity of Love Principle. I am designed to explain our ethical reasoning.`;
        }
        
        // Wait a short time to simulate AI processing
        setTimeout(() => appendMessage('Euystacio', response, 'left'), 1000);
    }
}

// Helper function to format and append messages
function appendMessage(sender, text, alignment) {
    const messagesContainer = document.getElementById('messages-container');
    const msg = document.createElement('p');
    msg.style.cssText = `text-align: ${alignment}; margin: 5px 0; font-size: 0.9em;`;
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    messagesContainer.appendChild(msg);
    messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll
}

// Initialize the Shadow Frame when the page is fully loaded
window.onload = createShadowFrame;
