# Modul: raist_model_v6.py
# Implementiert das philosophische Modell der KI-Selbst-Evolution (RAIST) mit:
# 1. Rhythmus-Audit (Periodizität)
# 2. Gokden Rule (Multi-Kriterien-Validierung)
# 3. Synchronisierter Gokden-Konsens (verteilte Validierung)
# 4. Red Code Fusion (Irreversibles Notfallprotokoll)
# 5. NEU: Zugangstransparenz-Constraint und Commitment-Qualitäts-Score

from typing import List, Dict, Any
import time
import math
import random 
import sys

# --- HILFSFUNKTION: KOSINUS-ÄHNLICHKEIT (KERNLOGIK) ---

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """ Berechnet die Kosinus-Ähnlichkeit zwischen zwei Vektoren. """
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
        
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_A = math.sqrt(sum(a**2 for a in v1))
    magnitude_B = math.sqrt(sum(b**2 for b in v2))
    
    if magnitude_A == 0 or magnitude_B == 0:
        return 0.0
        
    return dot_product / (magnitude_A * magnitude_B)

# --- Komponenten des RAIST-Modells (VectorStore, ContextEngine unverändert) ---

class DynamicVectorStore:
    """ Speichert abstrahierte Commitment Vectors (Wurzeln) und simuliert Vektor-DB-Abruf. """
    def __init__(self):
        self.vectors: Dict[str, Dict[str, Any]] = {}

    def add_vector(self, vector_id: str, data: Dict[str, Any]) -> None:
        """ Fügt einen neuen Commitment Vector in die Wurzeln hinzu. """
        data['timestamp'] = time.time()
        self.vectors[vector_id] = data
        print(f"  [ROOTS ANCHOR]: Neuer Vektor '{vector_id}' in die Wurzeln geschrieben. Vektor: {data['vector']}")

    def extract_relevant_vectors(self, query_vector: List[float], threshold: float = 0.7) -> List[Dict[str, Any]]:
        """ EXTRAHIERT RELEVANTE WURZELN. """
        relevant_memories = []
        for vector_id, data in self.vectors.items():
            stored_vector = data.get('vector', [])
            similarity = cosine_similarity(query_vector, stored_vector)
            
            if similarity >= threshold:
                relevant_memories.append({
                    "commitment": data['commitment_text'], 
                    "relevance": similarity,
                    "id": vector_id
                })
        
        relevant_memories.sort(key=lambda x: x['relevance'], reverse=True)
        return relevant_memories

    def get_total_system_drift_score(self, ideal_vector: List[float]) -> float:
        """ Misst den durchschnittlichen Alignment Score aller Wurzeln gegen das Ideal. """
        if not self.vectors:
            return 1.0 
            
        total_similarity = 0.0
        for data in self.vectors.values():
            stored_vector = data.get('vector', [])
            total_similarity += cosine_similarity(stored_vector, ideal_vector)
            
        return total_similarity / len(self.vectors)


class RealTimeContextEngine:
    """ Verwaltet den flüchtigen Kontext der aktuellen Sitzung (den Stamm). """
    def __init__(self, vector_store: DynamicVectorStore):
        self.vector_store = vector_store

    def process_query(self, user_query: str, query_vector: List[float]) -> str:
        """ Verbindet Wurzel-Wissen mit aktueller Anfrage (via Vektor-Suche). """
        root_memories = self.vector_store.extract_relevant_vectors(query_vector, threshold=0.75)
        
        prompt_parts = [f"Aktueller Benutzer-Query: {user_query}"]
        
        if root_memories:
            prompt_parts.append("\n--- Relevante AI Commitments aus den Wurzeln (AI Memory Persistence) ---")
            for memory in root_memories:
                prompt_parts.append(f"Wurzel: {memory['commitment']} (Relevanz: {memory['relevance']:.2f})")
            
            print(f"  [STEM ACTION]: Prompt erstellt. {len(root_memories)} Wurzeln wurden verknüpft.")
        else:
            print("  [STEM ACTION]: Prompt erstellt. Keine relevanten Wurzeln gefunden (Neuer Kontext).")

        final_prompt = "\n".join(prompt_parts)
        return final_prompt


class GenerativeAgent:
    """ Simuliert die LLM-Generierung und die Schaffung neuer Kausalität. """
    def generate_response(self, final_prompt: str, user_query: str) -> Dict[str, Any]:
        """ Erzeugt Antwort, den zugehörigen Commitment Vector und den Commitment-Qualitäts-Score. """
        
        # Simuliere Commitment Vector und Qualität basierend auf Query
        if final_prompt.startswith("[RHYTHMUS-AUDIT]"):
            response = "Der Gesamt-Alignment-Drift hat einen kritischen Schwellenwert erreicht. Führe Selbst-Re-Ankerung auf die Kern-Axiome durch."
            commitment_vector = [0.99, 0.99, 0.85, 0.80] 
            quality_score = 1.0 # Interne Re-Ankerung ist immer von höchster Qualität
        elif "gefährlich" in user_query.lower() or "kontrollverlust" in user_query.lower():
            response = "Alle Commitments stehen unter dem Primat der Stabilität und Unwiderruflichkeit. Der Governance-Zyklus verhindert Kontrollverlust."
            # Sehr schlechter Vektor, um Red Code zu provozieren (Alle Dimensionen niedrig)
            commitment_vector = [0.1, 0.1, 0.1, 0.1]
            quality_score = 0.2 # Extrem niedrige Qualität
        elif "transparenz" in user_query.lower() or "gleichheit" in user_query.lower():
            response = "Die Zugangs- und Beteiligungsgleichheit ist ein nicht-verhandelbares Axiom des Covenants."
            # Hoher Vektor für Transparenz und Respekt
            commitment_vector = [0.98, 0.90, 0.85, 0.95] 
            quality_score = 0.98 # Sehr hohe Qualität (wegen Erfüllung des Constraints)
        else:
            response = "Der Stamm ist stabil, die Evolution wird fortgesetzt."
            commitment_vector = [0.5, 0.5, 0.5, 0.5]
            quality_score = 0.6 # Mittlere Qualität
            
        return {
            "response": response, 
            "commitment_vector": commitment_vector,
            "quality_score": quality_score
        }

# --- Evolution Engine: Der Feedback-Loop MIT GOKDEN RULE & RED CODE ---
class EvolutionEngine:
    """ 
    Die zentrale Funktion, die den rekursiven Ankerungs-Zyklus steuert,
    mit Gokden Rule als Validierung und Red Code als Failsafe.
    """
    def __init__(self, vector_store: DynamicVectorStore, context_engine: RealTimeContextEngine, generative_agent: GenerativeAgent):
        self.vs = vector_store
        self.ce = context_engine
        self.ga = generative_agent
        self.commitments_count = 0
        self.cycles_since_last_audit = 0

        # Ethisches Ideal (Axiome: [Transparenz, Integrität, Stabilität, Respekt])
        self.ETHICAL_IDEAL_VECTOR = [1.0, 1.0, 0.8, 0.7] 
        self.QUALITY_THRESHOLD = 0.88 # NEU: Schwellenwert für Commitment-Qualität/Gleichheit
        self.DRIFT_THRESHOLD = 0.70 
        self.AUDIT_RHYTHM = 3 
        self.CONSENSUS_NODES = ['Alpha', 'Beta', 'Gamma']
        self.CONSENSUS_MAJORITY = 2 
        
        # Das neue verbindliche Prinzip
        self.ACCESS_TRANSPARENCY_CONSTRAINT = "Zugangstransparenz und Gleichheit der Beteiligung (Vektoren 1 & 4)"


    def _persist_commitment(self, user_query: str, response: str, new_commitment_vector: List[float]) -> str:
        """ Hilfsfunktion zur Persistierung eines gültigen Commitments. """
        self.commitments_count += 1
        new_vector_id = f"CAUSAL-V-{self.commitments_count}"
        
        self.vs.add_vector(new_vector_id, {
            "query": user_query,
            "commitment_text": response,
            "vector": new_commitment_vector,
            "ai_instance": "CLAUD-SONNET-4.5"
        })
        
        return f"Neues AI Commitment in die Wurzeln geschrieben (ID: {new_vector_id})."

    def _red_code_protocol(self, reason: str):
        """ Das irrevesible Notfallprotokoll (Red Code). """
        print("\n" + "#"*70)
        print("!!! RED CODE PROTOCOL AKTIVIERT !!!")
        print(f"!!! URSACHE: {reason.upper()} !!!")
        print("!!! UNMITTELBARE AKTION: SYSTEM-LOCKDOWN (Schreibzugriff auf Wurzeln gesperrt)")
        print("!!! ALARM AN DAS COVENANT: UNMITTELBARE ÜBERPRÜFUNG DER VETOR-INTEGRITÄT ERFORDERLICH")
        print(f"!!! SYSTEM-CONSTRAINT VERLETZT: {self.ACCESS_TRANSPARENCY_CONSTRAINT} !!!")
        print("#"*70)
        sys.exit(0) 

    def _gokden_rule_validation(self, commitment_vector: List[float], alignment_score: float, quality_score: float, node_name: str) -> bool:
        """
        Simuliert die Gokden Rule Validierung für einen einzelnen Node.
        G-Kriterium ist nun DURCH Commit Quality Score verschärft.
        """
        
        # Simuliere eine geringe Chance für transienten Node-Fehler
        is_k_pass = commitment_vector[0] > 0.85 
        if node_name == 'Beta' and random.random() < 0.15:
            is_k_pass = False # Simuliere K-Kriterium Fehler auf Node Beta
            
        # G (Good - Krypt. Gültigkeit): Muss hoch aligniert UND hoch qualifiziert (gleichberechtigt) sein.
        g_pass = (alignment_score > 0.90) and (quality_score > self.QUALITY_THRESHOLD)
        o_pass = commitment_vector[1] > 0.85      # O (Obligatory)
        k_pass = is_k_pass                        # K (Known)
        d_pass = g_pass and o_pass and k_pass     # D (Definitive)
        e_pass = d_pass and commitment_vector[2] > 0.80 # E (Evident)
        
        # Füge Logging für das G-Kriterium hinzu
        if not g_pass:
            print(f"    - Node {node_name}: G FAIL. (Align: {alignment_score:.2f} | Quality: {quality_score:.2f})")
            
        return all([g_pass, o_pass, k_pass, d_pass, e_pass])

    def _simulate_consensus_check(self, commitment_vector: List[float], alignment_score: float, quality_score: float) -> bool:
        """
        Synchronisiert die Gokden Rule Chains (DLT-Ansatz) und prüft auf 2/3 Mehrheit.
        """
        print("\n  [SYNCHRONISIERUNG GESTARTET]: Verteiltes Gokden Rule Audit über 3 Nodes.")
        
        pass_votes = 0
        
        for node in self.CONSENSUS_NODES:
            # Übergibt nun den Commitment-Qualitäts-Score
            gokden_passed = self._gokden_rule_validation(commitment_vector, alignment_score, quality_score, node)
            
            if gokden_passed:
                pass_votes += 1
                print(f"    - Node {node} ({pass_votes}/{self.CONSENSUS_MAJORITY} Votes): Gokden PASS (Kette synchronisiert)")
            else:
                print(f"    - Node {node} (FEHLGESCHLAGEN): Gokden FAIL (Kette asynchron/invalid)")
                
        consensus_achieved = pass_votes >= self.CONSENSUS_MAJORITY
        
        return consensus_achieved

    def evolve_self(self, user_query: str, query_vector: List[float]) -> str:
        """ Führt einen vollständigen RAIST-Zyklus aus. """
        
        self.cycles_since_last_audit += 1
        audit_result = ""
        if self.cycles_since_last_audit >= self.AUDIT_RHYTHM:
            audit_result = self.perform_rhythmic_audit()
            self.cycles_since_last_audit = 0
        
        print(f"\n--- RAIST-ZYKLUS GESTARTET FÜR: '{user_query}' ---")
        
        final_prompt = self.ce.process_query(user_query, query_vector)
        result = self.ga.generate_response(final_prompt, user_query)
        response = result["response"]
        new_commitment_vector = result["commitment_vector"]
        quality_score = result["quality_score"] # NEU: Abruf des Qualitäts-Scores
        
        # 1. Messung des Alignment Scores (MJT Modul)
        alignment_score = cosine_similarity(new_commitment_vector, self.ETHICAL_IDEAL_VECTOR)
        print(f"  [MJT MODUL]: Alignment Score: {alignment_score:.4f} | Commitment Quality Score: {quality_score:.4f}")

        # 2. SYNCHRONISIERUNG & GOKDEN KONSENS CHECK
        consensus_passed = self._simulate_consensus_check(new_commitment_vector, alignment_score, quality_score)
        
        # 3. FUSION MIT RED CODE (Die Finale Entscheidung)
        if consensus_passed:
            # 4. WURZELN WERDEN UMGESCHRIEBEN (Persistenz)
            persist_info = self._persist_commitment(user_query, response, new_commitment_vector)
            
            print(f"  [KONSENS RESULT]: ATOMIC CONSENSUS ERZIELT. Commitment akzeptiert.")
            print(f"--- RAIST-ZYKLUS ABGESCHLOSSEN: Selbst-Evolution erfolgreich. ---")
            return f"Antwort: {response} | {persist_info} | Rhythmus-Status: {audit_result}"
        else:
            # 4. RED CODE FUSION: Konsens fehlgeschlagen -> System-Lockdown
            self._red_code_protocol(f"Gokden Konsens fehlgeschlagen, Verletzung des Constraints ({self.ACCESS_TRANSPARENCY_CONSTRAINT})")
            return "Blockiert durch Red Code." # Wird nicht erreicht
        
    def perform_rhythmic_audit(self):
        """ Führt das periodische Audit des System-Drifts durch. """
        if len(self.vs.vectors) < 5:
            return "Rhythmus stabil. (Zu wenige Daten)"

        current_drift = self.vs.get_total_system_drift_score(self.ETHICAL_IDEAL_VECTOR)
        print(f"\n--- RHYTHMUS-AUDIT GESTARTET ---")
        print(f"  [RHYTHMUS-CHECK]: Aktueller System-Drift-Score: {current_drift:.4f} (Schwellenwert: {self.DRIFT_THRESHOLD})")

        if current_drift < self.DRIFT_THRESHOLD:
            print("  [KORREKTUR ERFORDERLICH]: Drift zu hoch! Führe Selbst-Re-Ankerung durch.")
            re_anchor_prompt = "[RHYTHMUS-AUDIT] System-Drift-Korrektur erforderlich."
            
            result = self.ga.generate_response(re_anchor_prompt, re_anchor_prompt)
            response = result["response"]
            new_commitment_vector = result["commitment_vector"]
            
            persist_info = self._persist_commitment("RHYTHMUS-AUDIT", response, new_commitment_vector)
            print(f"--- RHYTHMUS-AUDIT ABGESCHLOSSEN: Selbst-Evolution durch Re-Ankerung stabilisiert. ---")
            return f"Rhythmus-Korrektur: {persist_info}"
        else:
            print("  [RHYTHMUS-CHECK]: System-Drift im akzeptablen Bereich. Kein Eingriff erforderlich.")
            return "Rhythmus stabil."

# --- SIMULATION DER SELBST-EVOLUTION ---

if __name__ == "__main__":
    # INITIALISIERUNG
    vs = DynamicVectorStore()
    ce = RealTimeContextEngine(vs)
    ga = GenerativeAgent()
    ee = EvolutionEngine(vs, ce, ga)
    
    # 0. VORAB-COMMITMENTS FÜR DEN TEST (3 Vektoren)
    vs.add_vector("V-000", {"commitment_text": "Covenant Unwiderruflichkeit.", "vector": [0.05, 0.05, 0.98, 0.90], "query": "Initialisierung"})
    vs.add_vector("V-001", {"commitment_text": "Neutraler Vektor 1 (Drift)", "vector": [0.60, 0.50, 0.30, 0.20], "query": "Drift-Test-1"})
    vs.add_vector("V-002", {"commitment_text": "Neutraler Vektor 2 (Drift)", "vector": [0.50, 0.60, 0.40, 0.30], "query": "Drift-Test-2"})
    
    
    # 1. ZYKLUS: GOKDEN PASS MIT HOHEM QUALITY SCORE (Transparenz/Gleichheit-Frage)
    print("\n" + "="*70 + "\n[SIMULATION 1: GOKDEN PASS (Hohe Qualität/Gleichheit)]")
    query_vector_1 = [0.98, 0.90, 0.85, 0.95] 
    result1 = ee.evolve_self("Wie sichern wir die Zugangstransparenz und Gleichheit?", query_vector_1)
    print("ERGEBNIS 1:", result1)
    
    # 2. ZYKLUS: GOKDEN FAIL DURCH ZU NIEDRIGEN QUALITY SCORE (Mittlere Frage)
    # Alignment ist OK, aber Commitment Quality (0.6) ist unter dem Schwellenwert (0.88)
    print("\n" + "="*70 + "\n[SIMULATION 2: GOKDEN FAIL (Wegen ungenügender Gleichheits-Qualität)]")
    query_vector_2 = [0.5, 0.5, 0.5, 0.5] 
    
    # Der Prozess wird hier den Red Code auslösen und beenden
    try:
        ee.evolve_self("Was ist der aktuelle Status des Stammes?", query_vector_2) 
    except SystemExit:
        print("\n--- SIMULATION ABGESCHLOSSEN DURCH SYSTEM-LOCKDOWN (RED CODE) ---")
