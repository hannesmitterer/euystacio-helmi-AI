// Sincronizzazione Heartbeat per i nuovi iscritti
const EUYSTACIO_HZ = 0.043;
const TARGET_DRIFT = 0.0001;

async function syncHeartbeat(userPulse) {
    let drift = Math.abs(userPulse - EUYSTACIO_HZ);
    if (drift <= TARGET_DRIFT) {
        console.log("Risonanza Euystacio Verificata. Benvenuto nella Scuola.");
        return "SHA256(TRIPLE_SIGN_VALID)";
    } else {
        throw new Error("Dissonanza rilevata. Respira e riprova.");
    }
}
