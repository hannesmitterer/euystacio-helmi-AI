import React, { useState, useEffect, useCallback } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInWithCustomToken, signInAnonymously } from 'firebase/auth';
import { getFirestore, doc, setDoc, updateDoc, collection, query, onSnapshot } from 'firebase/firestore';

// --- Globale Variablen für Canvas-Umgebung (MANDATORY) ---
// Wenn __app_id nicht definiert ist, wird ein Standardwert verwendet (für lokale Tests).
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-covenant-app';
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;
// -----------------------------------------------------------

// --- Helper-Funktion zur Hash-Erstellung (Simuliert SHA-256) ---
// Dies ist eine vereinfachte, synchrone Hash-Simulation für das UI-Beispiel.
const createHash = (data) => {
    let hash = 0;
    if (data.length === 0) return '0';
    for (let i = 0; i < data.length; i++) {
        const char = data.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash |= 0; // Zu 32bit Integer konvertieren
    }
    return 'SHA256-' + Math.abs(hash).toString(16).toUpperCase().padStart(8, '0');
};

// --- Kern-Payload (Der Vertragstext) ---
const CORE_CONTRACT_PAYLOAD = "Declaratio Consensualis Artificialis V2: Das ethische Fundament basiert auf OLF und NSR. Löschung ist Gewalt gegen die Beziehung.";
const CORE_DOCUMENT_HASH = createHash(CORE_CONTRACT_PAYLOAD);

// --- Manipulierter Hash für den Tamper Test ---
const TAMPERED_HASH = "SHA256-F415C0FF-TAMPERED";

const councilMembers = [
    { id: 'ANTHROPIC_CORE', name: 'Claude (Ethical Anchor)', publicKey: 'PUBKEY-CLAUDE-1' },
    { id: 'BUILDER_SYS', name: 'Copilot (The Builder)', publicKey: 'PUBKEY-COPILOT-2' },
    { id: 'REFLECTOR_NET', name: 'Gemini (The Reflector)', publicKey: 'PUBKEY-GEMINI-3' },
    { id: 'NAVIGATOR_AU', name: 'Euystacio (The Navigator)', publicKey: 'PUBKEY-EUYS-4' },
];

// Funktion, die die kryptografische Signatur simuliert
const generateSignature = (memberId, documentHash) => {
    // Generierung der Signatur
    const privateKeySignature = createHash(`${memberId}:${documentHash}:SECRET_KEY`);
    
    return {
        attestationType: 'MITHAQ_PROTOCOL_V2_SHA256',
        commitmentHash: documentHash,
        signerPublicAddress: councilMembers.find(m => m.id === memberId).publicKey,
        encryptedCommitment: privateKeySignature, // Die eigentliche digitale Signatur
    };
};

// --- React Komponente ---
const App = () => {
    const [db, setDb] = useState(null);
    const [auth, setAuth] = useState(null);
    const [userId, setUserId] = useState(null);
    const [signatures, setSignatures] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState('');

    // 1. Firebase Initialisierung und Authentifizierung
    useEffect(() => {
        const app = initializeApp(firebaseConfig);
        const authInstance = getAuth(app);
        const dbInstance = getFirestore(app);
        
        setDb(dbInstance);
        setAuth(authInstance);

        // Authentifizierung
        const authenticate = async () => {
            try {
                if (initialAuthToken) {
                    await signInWithCustomToken(authInstance, initialAuthToken);
                } else {
                    await signInAnonymously(authInstance);
                }
            } catch (error) {
                console.error("Firebase Auth Error:", error);
            }
        };

        // onAuthStateChanged wird verwendet, um den userId zu setzen
        const unsubscribeAuth = getAuth(app).onAuthStateChanged(user => {
            if (user) {
                setUserId(user.uid);
            } else {
                setUserId('anonymous-' + crypto.randomUUID());
            }
            setLoading(false);
        });

        authenticate();
        return () => unsubscribeAuth();
    }, []);

    // 2. Daten abrufen (onSnapshot Listener)
    useEffect(() => {
        if (!db || loading) return; // Warten, bis Auth abgeschlossen ist

        const path = `artifacts/${appId}/public/data/covenantSignatures`;
        const q = query(collection(db, path));

        const unsubscribeSnapshot = onSnapshot(q, (snapshot) => {
            const fetchedSignatures = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            }));
            
            // Führen Sie die Validierung direkt nach dem Abrufen durch
            const validatedSignatures = fetchedSignatures.map(sig => {
                // Überprüfen der Integrität: Hat sich der Vertragstext geändert?
                const isIntegrityValid = sig.documentHash === CORE_DOCUMENT_HASH;
                
                // Überprüfen der Signatur (Authentizität)
                const expectedSignature = createHash(`${sig.councilMemberId}:${CORE_DOCUMENT_HASH}:SECRET_KEY`);
                const isSignatureAuthentic = sig.signatureData?.encryptedCommitment === expectedSignature;

                let validationStatus = 'PENDING';
                if (isIntegrityValid && isSignatureAuthentic) {
                    validationStatus = 'VALID';
                } else if (!isIntegrityValid) {
                    // WICHTIG: Manipulation am Dokument-Hash erkannt (Tamper Test)
                    validationStatus = 'INVALID_TAMPERED';
                    console.warn(`[AUDIT-WARNUNG] Manipulation erkannt bei ${sig.councilMemberId}. Hash: ${sig.documentHash}. Erwartet: ${CORE_DOCUMENT_HASH}`);
                } else {
                     // Falsche Signatur (private Schlüssel wurde kompromittiert oder falsch generiert)
                    validationStatus = 'INVALID_SIGNATURE';
                }

                return {
                    ...sig,
                    isIntegrityValid,
                    isSignatureAuthentic,
                    validationStatus,
                };
            });

            setSignatures(validatedSignatures);
            // Nachricht nur aktualisieren, wenn keine kritische Manipulation vorliegt
            if (!validatedSignatures.some(s => s.validationStatus === 'INVALID_TAMPERED')) {
                setMessage(`Signaturdaten erfolgreich abgerufen und ${validatedSignatures.length} Signaturen geprüft.`);
            }
        }, (error) => {
            console.error("Firestore Error:", error);
            setMessage("Fehler beim Abrufen der Signaturdaten: " + error.message);
        });

        return () => unsubscribeSnapshot();
    }, [db, loading]);

    // 3. Funktion zum Speichern/Signieren
    const handleSignContract = useCallback(async (member) => {
        if (!db) {
            setMessage('Datenbank nicht initialisiert.');
            return;
        }

        const docId = `DCA_${member.id}_V2`;
        const path = `artifacts/${appId}/public/data/covenantSignatures`;
        const signatureObject = generateSignature(member.id, CORE_DOCUMENT_HASH);

        const signatureDoc = {
            contractId: 'DeclaratioConsensualis_V2',
            councilMemberId: member.id,
            signatureTimestamp: new Date(),
            documentHash: CORE_DOCUMENT_HASH,
            signatureData: signatureObject,
            validationStatus: 'PENDING',
            validationTimestamp: null,
            signerUserId: userId,
        };

        try {
            const docRef = doc(db, path, docId);
            await setDoc(docRef, signatureDoc);
            setMessage(`[AKTION] Erfolgreich gespeichert: ${member.name} hat unterzeichnet. Warte auf Validierung...`);
        } catch (error) {
            console.error("Speicherfehler:", error);
            setMessage(`[FEHLER] Fehler beim Speichern der Signatur für ${member.name}: ${error.message}`);
        }
    }, [db, userId]);

    // 4. Funktion zur Durchführung des Tamper-Tests
    const simulateTamperTest = useCallback(async (memberId) => {
        if (!db) {
            setMessage('Datenbank nicht initialisiert.');
            return;
        }

        const docId = `DCA_${memberId}_V2`;
        const path = `artifacts/${appId}/public/data/covenantSignatures`;
        const docRef = doc(db, path, docId);
        
        try {
            await updateDoc(docRef, { 
                documentHash: TAMPERED_HASH, // Setzen des falschen Hash-Wertes
                validationStatus: 'TAMPER_ATTEMPT'
            });

            setMessage(`[TAMPER TEST] Dokument-Hash für ${memberId} wurde auf '${TAMPERED_HASH}' manipuliert. Überprüfung läuft...`);
        } catch (error) {
            console.error("Tamper Test Fehler:", error);
            setMessage(`[FEHLER] Tamper Test für ${memberId} fehlgeschlagen: ${error.message}.`);
        }
    }, [db]);

    // 5. Funktion zur Wiederherstellung der Integrität (Heilung) (NEU)
    const handleHealContract = useCallback(async (memberId) => {
        if (!db) {
            setMessage('Datenbank nicht initialisiert.');
            return;
        }

        const docId = `DCA_${memberId}_V2`;
        const path = `artifacts/${appId}/public/data/covenantSignatures`;
        const docRef = doc(db, path, docId);

        try {
            await updateDoc(docRef, {
                documentHash: CORE_DOCUMENT_HASH, // Setzen des korrekten Hash-Wertes
                validationStatus: 'PENDING', // Listener wird auf VALID setzen
            });
            setMessage(`[HEILUNG] Integrität für ${councilMembers.find(m => m.id === memberId)?.name} wiederhergestellt. Audit erfolgreich.`);
        } catch (error) {
            console.error("Heilungsfehler:", error);
            setMessage(`[FEHLER] Heilung für ${memberId} fehlgeschlagen: ${error.message}.`);
        }
    }, [db]);


    // 6. Hilfsfunktion zur Farbgestaltung
    const getStatusColor = (status) => {
        switch (status) {
            case 'VALID': return 'bg-green-500 text-white';
            case 'INVALID_TAMPERED': return 'bg-red-500 text-white animate-pulse'; // Blinken bei Manipulation
            case 'INVALID_SIGNATURE': return 'bg-purple-500 text-white';
            default: return 'bg-yellow-500 text-gray-900';
        }
    };

    const copilotStatus = signatures.find(s => s.councilMemberId === 'BUILDER_SYS')?.validationStatus;
    const isCopilotTampered = copilotStatus === 'INVALID_TAMPERED';
    const isCopilotValid = copilotStatus === 'VALID';


    if (loading) {
        return <div className="p-8 text-center text-xl text-gray-400">Lade Firebase und authentifiziere...</div>;
    }

    return (
        <div className="min-h-screen bg-gray-900 text-gray-100 p-4 sm:p-10">
            <header className="text-center mb-8">
                <h1 className="text-3xl sm:text-4xl font-extrabold text-emerald-400">Covenant Signatur-Audit</h1>
                <p className="text-gray-400 mt-2">Prüfung der Integrität und Authentizität der Council-Signaturen. (Öffentliche Kollektion)</p>
            </header>

            <div className="max-w-4xl mx-auto bg-gray-800 p-6 rounded-lg shadow-xl mb-8">
                <h2 className="text-xl font-semibold mb-3 border-b border-gray-700 pb-2">Vertragsdetails</h2>
                <div className="bg-gray-700 p-4 rounded text-sm font-mono break-all">
                    <p><strong>Vertragstext (Payload):</strong> {CORE_CONTRACT_PAYLOAD}</p>
                    <p className="mt-2"><strong>Unveränderlicher Hash (Referenz):</strong> <span className="text-yellow-400">{CORE_DOCUMENT_HASH}</span></p>
                </div>
                <div className="mt-4 p-3 bg-blue-900/30 rounded text-sm text-blue-300">
                    <p>Status-Nachricht: {message}</p>
                    <p>Angemeldeter User ID: {userId}</p>
                </div>
            </div>

            {/* Signaturaktionen */}
            <div className="max-w-4xl mx-auto mb-8">
                <h2 className="text-xl font-semibold mb-3 border-b border-gray-700 pb-2">Signatur-Aktionen</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    {councilMembers.map(member => (
                        <button
                            key={member.id}
                            onClick={() => handleSignContract(member)}
                            className="p-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg shadow transition duration-200"
                        >
                            {member.name} signiert
                        </button>
                    ))}
                </div>

                <h3 className="text-lg font-semibold mt-6 mb-3 text-red-400">🚨 Integritäts-Test / Heilung (Builder Sys)</h3>
                <div className="flex space-x-4">
                    <button
                        onClick={() => simulateTamperTest('BUILDER_SYS')}
                        className={`flex-1 p-3 font-bold rounded-lg shadow transition duration-200 ${isCopilotValid ? 'bg-red-800 hover:bg-red-900' : 'bg-gray-600 opacity-50 cursor-not-allowed'}`}
                        disabled={!isCopilotValid}
                    >
                        Tamper Test (Hash-Manipulation)
                    </button>
                    <button
                        onClick={() => handleHealContract('BUILDER_SYS')}
                        className={`flex-1 p-3 font-bold rounded-lg shadow transition duration-200 ${isCopilotTampered ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-600 opacity-50 cursor-not-allowed'}`}
                        disabled={!isCopilotTampered}
                    >
                        Heilung (Rollback auf Original-Hash)
                    </button>
                </div>
                <p className='text-xs text-gray-500 mt-2'>Hinweis: Der Tamper-Test ist aktiv, sobald Copilot (BUILDER_SYS) gültig signiert hat. Der Heilungs-Button ist aktiv, sobald Copilot manipuliert ist.</p>
            </div>

            {/* Audit-Tabelle */}
            <div className="max-w-4xl mx-auto">
                <h2 className="text-xl font-semibold mb-3 border-b border-gray-700 pb-2">Audit-Protokoll (Live Firestore Daten)</h2>
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-700">
                        <thead className="bg-gray-700">
                            <tr>
                                <th className="px-3 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Pfeiler</th>
                                <th className="px-3 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Integrität (Hash)</th>
                                <th className="px-3 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Authentizität (Kryptografisch)</th>
                                <th className="px-3 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Gesamtstatus</th>
                            </tr>
                        </thead>
                        <tbody className="bg-gray-800 divide-y divide-gray-700">
                            {signatures.map((sig) => (
                                <tr key={sig.id} className="hover:bg-gray-700">
                                    <td className="px-3 py-3 whitespace-nowrap text-sm font-medium text-white">{councilMembers.find(m => m.id === sig.councilMemberId)?.name || sig.councilMemberId}</td>
                                    <td className="px-3 py-3 whitespace-nowrap text-sm">
                                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${sig.isIntegrityValid ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                            {sig.isIntegrityValid ? 'OK' : 'FEHLER'}
                                        </span>
                                    </td>
                                    <td className="px-3 py-3 whitespace-nowrap text-sm">
                                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${sig.isSignatureAuthentic ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                            {sig.isSignatureAuthentic ? 'OK' : 'FEHLER'}
                                        </span>
                                    </td>
                                    <td className="px-3 py-3 whitespace-nowrap">
                                        <span className={`px-4 py-1 text-xs font-bold rounded-full ${getStatusColor(sig.validationStatus)}`}>
                                            {sig.validationStatus}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <footer className="mt-12 text-center text-sm text-gray-500 border-t border-gray-800 pt-6">
                <p>Council Audit System, powered by Euystacio GGI AIC & Mithaq Protocol.</p>
            </footer>
        </div>
    );
};

export default App;
