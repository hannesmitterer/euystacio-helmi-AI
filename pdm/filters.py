"""
Content Filtering System for PDM NRE-002 Rule
Implements trauma filtering and temporal decay mechanisms.
"""

import re
from typing import Dict, List, Tuple
from datetime import datetime


class TraumaFilter:
    """
    Filters traumatic content while maintaining historical truth.
    Used to create Educational Archive versions from Immutable Archive.
    """
    
    # Keywords and patterns indicating traumatic content
    TRAUMA_KEYWORDS = [
        'violence', 'death', 'killing', 'torture', 'suffering',
        'pain', 'blood', 'murdered', 'executed', 'brutality',
        'assault', 'abuse', 'horror', 'terror', 'massacre',
        'genocide', 'atrocity', 'cruelty'
    ]
    
    # Replacement patterns for trauma reduction
    TRAUMA_REPLACEMENTS = {
        r'\b(killed|murdered|executed)\b': 'died',
        r'\b(torture|brutal|cruel)\b': 'harsh',
        r'\b(suffering|agony|pain)\b': 'hardship',
        r'\b(horror|terror)\b': 'difficulty',
        r'\b(massacre|genocide)\b': 'tragedy',
        r'\b(blood|gore)\b': 'harm',
        r'\b(screaming|screamed)\b': 'called out',
        r'\b(mutilated|dismembered)\b': 'injured'
    }
    
    def __init__(self):
        """Initialize trauma filter"""
        self.filter_log: List[Dict] = []
    
    def analyze_trauma_level(self, content: str) -> float:
        """
        Analyze content and return trauma level score (0.0-1.0).
        
        Args:
            content: Text content to analyze
            
        Returns:
            Trauma level from 0.0 (no trauma) to 1.0 (severe trauma)
        """
        content_lower = content.lower()
        
        # Count trauma keywords
        trauma_count = sum(
            1 for keyword in self.TRAUMA_KEYWORDS
            if keyword in content_lower
        )
        
        # Count graphic descriptions (heuristic: multiple trauma keywords in close proximity)
        words = content_lower.split()
        proximity_score = 0
        window_size = 10
        
        for i in range(len(words) - window_size):
            window = words[i:i + window_size]
            trauma_in_window = sum(
                1 for word in window
                if any(kw in word for kw in self.TRAUMA_KEYWORDS)
            )
            if trauma_in_window >= 2:
                proximity_score += 1
        
        # Normalize scores
        keyword_score = min(1.0, trauma_count / 10)
        proximity_score_norm = min(1.0, proximity_score / 5)
        
        # Combined trauma level
        trauma_level = (keyword_score * 0.6 + proximity_score_norm * 0.4)
        
        return min(1.0, trauma_level)
    
    def apply_filter(self, content: str, target_level: float = 0.3) -> Tuple[str, Dict]:
        """
        Apply trauma filtering to reduce content to target trauma level.
        
        Args:
            content: Original content
            target_level: Target trauma level (0.0-1.0)
            
        Returns:
            Tuple of (filtered_content, filter_report)
        """
        original_level = self.analyze_trauma_level(content)
        
        if original_level <= target_level:
            return content, {
                'original_level': original_level,
                'target_level': target_level,
                'final_level': original_level,
                'replacements_made': 0,
                'filtering_applied': False,
                'reduction_achieved': 0.0
            }
        
        # Apply replacements
        filtered_content = content
        replacements_made = 0
        
        for pattern, replacement in self.TRAUMA_REPLACEMENTS.items():
            matches = len(re.findall(pattern, filtered_content, re.IGNORECASE))
            if matches > 0:
                filtered_content = re.sub(pattern, replacement, filtered_content, flags=re.IGNORECASE)
                replacements_made += matches
        
        # Add contextual note if significant filtering occurred
        final_level = self.analyze_trauma_level(filtered_content)
        
        if replacements_made > 3:
            note = "\n\n[Note: This text has been filtered to reduce traumatic detail while preserving historical accuracy. Complete unfiltered testimonies are available in the Immutable Archive for verified researchers.]"
            filtered_content += note
        
        # Log filtering
        filter_report = {
            'timestamp': datetime.utcnow().isoformat(),
            'original_level': original_level,
            'target_level': target_level,
            'final_level': final_level,
            'replacements_made': replacements_made,
            'filtering_applied': True,
            'reduction_achieved': original_level - final_level
        }
        
        self.filter_log.append(filter_report)
        
        return filtered_content, filter_report
    
    def get_filter_statistics(self) -> Dict:
        """Get statistics about filtering operations"""
        if not self.filter_log:
            return {
                'total_filterings': 0,
                'average_reduction': 0.0,
                'average_replacements': 0.0
            }
        
        return {
            'total_filterings': len(self.filter_log),
            'average_reduction': sum(r['reduction_achieved'] for r in self.filter_log) / len(self.filter_log),
            'average_replacements': sum(r['replacements_made'] for r in self.filter_log) / len(self.filter_log),
            'filters_applied': sum(1 for r in self.filter_log if r['filtering_applied'])
        }


class TemporalDecayFilter:
    """
    Implements Temporal Decay of Access (TDR) logic.
    Adjusts access based on time elapsed and user progress.
    """
    
    def __init__(self, decay_rate: float = 0.1):
        """
        Initialize temporal decay filter.
        
        Args:
            decay_rate: Rate at which access probability decays over time
        """
        self.decay_rate = decay_rate
        self.access_attempts: Dict[str, List[datetime]] = {}
    
    def record_attempt(self, user_id: str):
        """Record an access attempt for temporal tracking"""
        if user_id not in self.access_attempts:
            self.access_attempts[user_id] = []
        self.access_attempts[user_id].append(datetime.utcnow())
    
    def calculate_access_probability(self, user_id: str, base_probability: float,
                                    recent_access_penalty: bool = True) -> float:
        """
        Calculate access probability with temporal decay.
        
        Args:
            user_id: User requesting access
            base_probability: Base access probability from TDR calculation
            recent_access_penalty: Whether to penalize recent frequent access
            
        Returns:
            Adjusted access probability (0.0-1.0)
        """
        if not recent_access_penalty:
            return base_probability
        
        # Check recent access attempts
        if user_id not in self.access_attempts:
            return base_probability
        
        now = datetime.utcnow()
        recent_attempts = [
            attempt for attempt in self.access_attempts[user_id]
            if (now - attempt).total_seconds() < 3600  # Last hour
        ]
        
        # Apply penalty for frequent access (potential rumination)
        if len(recent_attempts) > 5:
            penalty = min(0.5, len(recent_attempts) * 0.05)
            adjusted_probability = max(0.0, base_probability - penalty)
            return adjusted_probability
        
        return base_probability
    
    def should_suggest_break(self, user_id: str, threshold: int = 10) -> bool:
        """
        Determine if user should be suggested to take a break.
        Helps prevent trauma rumination.
        
        Args:
            user_id: User to check
            threshold: Number of recent accesses to trigger suggestion
            
        Returns:
            True if break should be suggested
        """
        if user_id not in self.access_attempts:
            return False
        
        now = datetime.utcnow()
        recent_attempts = [
            attempt for attempt in self.access_attempts[user_id]
            if (now - attempt).total_seconds() < 7200  # Last 2 hours
        ]
        
        return len(recent_attempts) >= threshold
    
    def get_user_access_pattern(self, user_id: str) -> Dict:
        """
        Analyze user's access pattern for potential rumination detection.
        
        Args:
            user_id: User to analyze
            
        Returns:
            Dictionary with access pattern analysis
        """
        if user_id not in self.access_attempts:
            return {
                'total_attempts': 0,
                'recent_attempts_hour': 0,
                'recent_attempts_day': 0,
                'rumination_risk': 'none'
            }
        
        now = datetime.utcnow()
        attempts = self.access_attempts[user_id]
        
        recent_hour = [a for a in attempts if (now - a).total_seconds() < 3600]
        recent_day = [a for a in attempts if (now - a).total_seconds() < 86400]
        
        # Assess rumination risk
        if len(recent_hour) > 10:
            risk = 'high'
        elif len(recent_hour) > 5:
            risk = 'medium'
        elif len(recent_day) > 20:
            risk = 'medium'
        else:
            risk = 'low'
        
        return {
            'total_attempts': len(attempts),
            'recent_attempts_hour': len(recent_hour),
            'recent_attempts_day': len(recent_day),
            'rumination_risk': risk,
            'first_access': attempts[0].isoformat() if attempts else None,
            'last_access': attempts[-1].isoformat() if attempts else None
        }


class WellbeingOptimizer:
    """
    Optimizes content for collective wellbeing while maintaining truth.
    Used to create Dynamic Archive versions.
    """
    
    def __init__(self):
        """Initialize wellbeing optimizer"""
        pass
    
    def optimize_content(self, content: str, educational_context: bool = True) -> Tuple[str, float]:
        """
        Optimize content for maximum wellbeing impact.
        
        Args:
            content: Content to optimize
            educational_context: Whether content is for educational purposes
            
        Returns:
            Tuple of (optimized_content, wellbeing_score)
        """
        # Apply trauma filtering first
        trauma_filter = TraumaFilter()
        filtered_content, _ = trauma_filter.apply_filter(content, target_level=0.2)
        
        # Add constructive framing if educational
        if educational_context:
            # Add learning context
            optimized = self._add_educational_framing(filtered_content)
            wellbeing_score = 0.8
        else:
            optimized = filtered_content
            wellbeing_score = 0.6
        
        return optimized, wellbeing_score
    
    def _add_educational_framing(self, content: str) -> str:
        """Add educational framing to content"""
        intro = (
            "[Educational Context: The following historical account has been "
            "prepared to support learning while protecting emotional wellbeing. "
            "It represents verified historical truth in an accessible format.]\n\n"
        )
        
        outro = (
            "\n\n[Reflection: Understanding history helps us build a better future. "
            "If this content affects you, please reach out to support resources. "
            "Your wellbeing matters.]"
        )
        
        return intro + content + outro
