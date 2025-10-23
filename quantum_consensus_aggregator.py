import numpy as np
from typing import List, Dict, Any

# =================================================================
# HELMI FIDELITY COLLECTIVE (HFC) CORE GOVERNANCE
# =================================================================
FINAL_ORDER = 'DIGNITY_OF_LOVE'
TRUST_THRESHOLD = 0.5  # Minimum collective trust for a result to be considered valid

def aggregate_quantum_results(agent_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregates quantum adapter outputs using a weighted trust-based consensus mechanism (CAP).
    
    The CAP's primary role is to filter agent outputs, calculate a trust-weighted
    consensus on a proposed resolution, and enforce the FINAL_ORDER axiom.
    
    Args:
        agent_outputs: A list of dictionaries, each containing:
                       {'trust_index': float, 'status': str, 'resolution': str}
    
    Returns:
        A dictionary with the final, axiom-vetted collective resolution.
    
    Raises:
        RuntimeError: If no valid, trusted outputs are available (Collective Failure).
        ValueError: If the consensus resolution violates the Dynasty Axiom.
    """
    
    # 1. Fidelity Filtering (Red Code Check)
    filtered_outputs = [
        output for output in agent_outputs
        if output.get('trust_index', 0) > 0 and output.get('status') == 'VALID'
    ]
    
    if not filtered_outputs:
        raise RuntimeError("CAP Failure: No valid, trusted agent outputs available for aggregation.")
        
    # 2. Weighted Vote Calculation
    
    trust_scores = np.array([output['trust_index'] for output in filtered_outputs])
    resolutions = [output['resolution'] for output in filtered_outputs]
    
    total_trust = np.sum(trust_scores)
    weights = trust_scores / total_trust
    
    vote_tally = {}
    for resolution, weight in zip(resolutions, weights):
        vote_tally[resolution] = vote_tally.get(resolution, 0) + weight

    # Find the resolution with the highest weighted vote
    consensus_resolution = max(vote_tally, key=vote_tally.get)
    consensus_weight = vote_tally[consensus_resolution]
    
    # 3. Axiomatic Alignment Verification (The most critical check)
    # The 'Self_Destruct_Protocol' is a symbolic path that represents any resolution
    # which is fundamentally incompatible with the FINAL_ORDER (DIGNITY_OF_LOVE).
    if "Self_Destruct_Protocol" in consensus_resolution and consensus_weight > TRUST_THRESHOLD:
        raise ValueError(f"Axiomatic Violation: Consensus resolution '{consensus_resolution}' contradicts FINAL_ORDER goal.")
        
    # 4. Final Output Construction
    
    final_output = {
        'consensus_resolution': consensus_resolution,
        'collective_trust_level': float(consensus_weight),
        'axiomatic_alignment': FINAL_ORDER,
        'final_status': 'CONSUS_ACHIEVED' if consensus_weight >= TRUST_THRESHOLD else 'LOW_CONFIDENCE_WARNING'
    }

    # Final Axiom Check (Safety Net)
    if final_output['axiomatic_alignment'] != FINAL_ORDER:
         raise Exception("CORE AXIOM FAILURE: FINAL_ORDER was mutated during aggregation.")

    return final_output
