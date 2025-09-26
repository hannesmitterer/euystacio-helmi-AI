//// hash-verifier.js
// Validates the integrity of the Covenant-Canon.md file against its immutable SHA-256 seal.

async function verifyCovenantHash() {
    const expectedHash = "879F8E4C7D0A2B5E1F6C3D9B4A8E0D7C2F1E6A5B0D3C4F7E2A9B8D1C0E5F4B3A";
    
    try {
        // Fetch the canonical manifesto file
        const res = await fetch('Covenant-Canon-v1.0.md');
        if (!res.ok) {
            alert("Error: Cannot fetch Covenant-Canon.md file.");
            return;
        }
        const txt = await res.text();
        
        // Encode and hash the content
        const data = new TextEncoder().encode(txt);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        
        // Convert hash buffer to uppercase hex string
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
        
        // Compare and alert the validation result
        if (hashHex === expectedHash) {
            alert("✅ Covenant Hash Match: Document integrity confirmed. The Living Covenant is unaltered.");
        } else {
            alert("❌ Covenant Hash Mismatch: Document integrity compromised. WARNING: The canonical file has been altered.");
        }
    } catch (error) {
        console.error("Verification error:", error);
        alert("Verification failed due to a system error.");
    }
}

// Note: Ensure this script is linked in index.html and a button calls verifyCovenantHash()