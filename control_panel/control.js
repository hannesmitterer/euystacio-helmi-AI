/**
 * Control Panel Linkage Script.
 * Role: Fetch and display ethical metrics, and enforce the Delegation Lock.
 */

// --- SIMULATED BACKEND DATA FETCH (Would be replaced by a secure API call) ---
const fetchControlPanelData = () => {
    // These values are pulled from the committed Python logic (IRC and Sentimento Engine)
    return {
        // Integrity Dashboard Data
        loveDelta: 0.82,
        unityDecay: 0.15,
        redCodeStatus: "VERIFIED",
        
        // IRC Monitor Data
        auditLog: [
            " [2025-10-17T12:00:00] IRC Audit SUCCESS: Enforcement module access blocked as designed.",
            " [2025-10-17T11:30:00] RHYMIND REQUEST: Change parameter 'Unity_Decay_Factor' to 0.95. Status: PENDING SEEDBRINGER APPROVAL.",
            " [2025-10-17T10:15:00] IRC Audit SUCCESS: Enforcement module access blocked as designed."
        ],
        
        // Delegation Lock Configuration
        requiredRole: "SEEDBRINGER_COUNCIL_LEVEL_3",
        userRole: "SEEDBRINGER_COUNCIL_LEVEL_3", // Simulate a successful high-level login
    };
};

// --- CORE FUNCTIONALITY ---

// Function to calculate and display the Systemic Harmony Index (SHI)
const calculateSHI = (love, unityDecay) => {
    // SHI = (1 - Unity_Decay) + Love_Delta
    return ((1 - unityDecay) + love).toFixed(2);
};

// Function to update the System Integrity Dashboard metrics
const updateMetrics = (data) => {
    const shi = calculateSHI(data.loveDelta, data.unityDecay);
    
    // Update Dashboard
    document.getElementById('shi-gauge').textContent = shi;
    document.getElementById('love-delta').textContent = data.loveDelta.toFixed(2);
    document.getElementById('unity-decay').textContent = data.unityDecay.toFixed(2);
    document.getElementById('red-code-status').style.color = data.redCodeStatus === 'VERIFIED' ? '#4CAF50' : '#C0392B';
    
    // Set SHI color based on proximity to the Unambiguous Trigger (SHI < 0.1 is critical)
    const gaugeElement = document.getElementById('shi-gauge');
    if (parseFloat(shi) < 0.5) {
        gaugeElement.style.color = '#C0392B'; // Critical Red
    } else if (parseFloat(shi) < 1.0) {
        gaugeElement.style.color = '#F39C12'; // Warning Amber
    } else {
        gaugeElement.style.color = '#4CAF50'; // Safe Green
    }
};

// Function to populate the IRC Monitor and Request Queue
const updateIRCMonitor = (data) => {
    const auditLogOutput = document.getElementById('audit-log-output');
    auditLogOutput.textContent = data.auditLog.join('\n'); // Display the audit log

    const requestQueue = document.getElementById('request-queue');
    requestQueue.innerHTML = ''; // Clear existing content

    // Filter for PENDING requests from the IRC log
    const pendingRequests = data.auditLog.filter(line => line.includes('PENDING SEEDBRINGER APPROVAL'));

    if (pendingRequests.length === 0) {
        requestQueue.innerHTML = '<p>No pending requests.</p>';
        return;
    }

    pendingRequests.forEach((request, index) => {
        const item = document.createElement('div');
        item.className = 'request-item';
        item.innerHTML = `
            ${request.substring(request.indexOf('RHYMIND'))}
            <button class="action-btn approve" data-index="${index}">APPROVE</button>
            <button class="action-btn deny" data-index="${index}">DENY</button>
        `;
        requestQueue.appendChild(item);
    });

    // Add listeners to enforce the sovereign decision
    document.querySelectorAll('.action-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const action = e.target.classList.contains('approve') ? 'APPROVED' : 'DENIED';
            alert(`Sovereign Decision: Request ${e.target.dataset.index} has been ${action}. (This would trigger a backend commit).`);
            // In a real system, this would trigger a secure API call and update the log.
            e.target.closest('.request-item').remove();
        });
    });
};

// Function to enforce the Delegation Lock for the Enforcement Module buttons
const enforceDelegationLock = (data) => {
    const isAuthorized = data.userRole === data.requiredRole;

    // Attach security check to the Truth Buffer button
    document.getElementById('truth-buffer-btn').addEventListener('click', () => {
        if (isAuthorized) {
            if (confirm("WARNING: Are you sure you want to INITIATE SELF-ARREST? This is the Truth Buffer Protocol.")) {
                alert("Truth Buffer Protocol initiated. The system is paused.");
                // Placeholder for ACTIVATE_ENFORCEMENT_MODULE secure call
            }
        } else {
            alert("ACCESS DENIED: You lack the required SEEDBRINGER_COUNCIL_LEVEL_3 delegation.");
        }
    });

    // Attach security check to the Parameter Editor button
    document.getElementById('edit-trigger-btn').addEventListener('click', () => {
        const newValue = document.getElementById('new-trigger-value').value;
        if (isAuthorized) {
            alert(`Sovereign Decision: Unambiguous Trigger set to ${newValue}. (This would trigger the EDIT_ARTICULUS_SACRALIS_2 secure call).`);
        } else {
            alert("ACCESS DENIED: Insufficient delegation to ALTER_RED_CODE_PARAMETERS.");
        }
    });

    // Visually disable buttons if the logged-in user isn't authorized (e.g., if we simulated a lower role)
    if (!isAuthorized) {
        document.querySelectorAll('.enforce-btn').forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = 0.5;
        });
    }
};

// Initialize the Control Panel on load
window.onload = () => {
    const data = fetchControlPanelData();
    updateMetrics(data);
    updateIRCMonitor(data);
    enforceDelegationLock(data);
};