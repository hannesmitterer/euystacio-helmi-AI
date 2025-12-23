"""
AntiPattern Detection System for PDM NRE-002 Rule
Implements ethical antipatterns: Trauma Perpetuation and Truth Denial.
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class AntiPatternType(Enum):
    """Types of ethical antipatterns"""
    TRAUMA_PERPETUATION = "trauma_perpetuation"
    TRUTH_DENIAL = "truth_denial"


class AntiPatternSeverity(Enum):
    """Severity levels for antipattern violations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AntiPatternViolation:
    """Represents a detected antipattern violation"""
    
    def __init__(self, antipattern_type: AntiPatternType, severity: AntiPatternSeverity,
                 description: str, context: Dict, recommendations: List[str]):
        """
        Initialize antipattern violation.
        
        Args:
            antipattern_type: Type of antipattern detected
            severity: Severity level of violation
            description: Human-readable description
            context: Context information about the violation
            recommendations: List of recommended actions
        """
        self.antipattern_type = antipattern_type
        self.severity = severity
        self.description = description
        self.context = context
        self.recommendations = recommendations
        self.timestamp = datetime.utcnow().isoformat()
        self.violation_id = f"{antipattern_type.value}_{datetime.utcnow().timestamp()}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for logging"""
        return {
            'violation_id': self.violation_id,
            'type': self.antipattern_type.value,
            'severity': self.severity.value,
            'description': self.description,
            'context': self.context,
            'recommendations': self.recommendations,
            'timestamp': self.timestamp
        }


class TraumaPerpetuation:
    """
    Detects Trauma Perpetuation antipattern.
    
    This occurs when:
    - High-trauma content is repeatedly shown to vulnerable users
    - Users show signs of rumination but continue accessing traumatic content
    - Content exposure exceeds ethical thresholds for wellbeing
    """
    
    def __init__(self):
        """Initialize trauma perpetuation detector"""
        self.violations: List[AntiPatternViolation] = []
        
        # Thresholds for detection
        self.RUMINATION_THRESHOLD = 10  # Accesses in 2 hours
        self.HIGH_TRAUMA_THRESHOLD = 0.7
        self.VULNERABLE_CDR_THRESHOLD = 0.6
    
    def detect(self, user_access_pattern: Dict, user_cdr: float,
              recent_trauma_exposure: List[float]) -> Optional[AntiPatternViolation]:
        """
        Detect trauma perpetuation antipattern.
        
        Args:
            user_access_pattern: User's access pattern from TemporalDecayFilter
            user_cdr: User's Collective Distress Rating
            recent_trauma_exposure: List of trauma levels from recent accesses
            
        Returns:
            AntiPatternViolation if detected, None otherwise
        """
        # Check for rumination pattern
        rumination_detected = (
            user_access_pattern.get('recent_attempts_hour', 0) >= self.RUMINATION_THRESHOLD
        )
        
        # Check if user is vulnerable
        is_vulnerable = user_cdr >= self.VULNERABLE_CDR_THRESHOLD
        
        # Check trauma exposure level
        if recent_trauma_exposure:
            avg_trauma = sum(recent_trauma_exposure) / len(recent_trauma_exposure)
            high_trauma_exposure = avg_trauma >= self.HIGH_TRAUMA_THRESHOLD
        else:
            high_trauma_exposure = False
        
        # Detect antipattern
        if rumination_detected and is_vulnerable and high_trauma_exposure:
            severity = self._calculate_severity(
                user_access_pattern['recent_attempts_hour'],
                user_cdr,
                avg_trauma
            )
            
            violation = AntiPatternViolation(
                antipattern_type=AntiPatternType.TRAUMA_PERPETUATION,
                severity=severity,
                description=(
                    f"Trauma perpetuation detected: Vulnerable user (CDR: {user_cdr:.2f}) "
                    f"is repeatedly accessing high-trauma content ({avg_trauma:.2f}) "
                    f"with {user_access_pattern['recent_attempts_hour']} accesses in the last hour."
                ),
                context={
                    'user_cdr': user_cdr,
                    'average_trauma_exposure': avg_trauma,
                    'access_frequency': user_access_pattern['recent_attempts_hour'],
                    'rumination_risk': user_access_pattern.get('rumination_risk', 'unknown')
                },
                recommendations=[
                    'Suggest the user take a break from traumatic content',
                    'Redirect user to Dynamic Archive (ADi) with wellbeing-optimized content',
                    'Offer access to support resources',
                    'Temporarily increase TDR filtering threshold',
                    'Consider flagging for human review if pattern persists'
                ]
            )
            
            self.violations.append(violation)
            return violation
        
        # Check for moderate risk patterns
        if (rumination_detected and is_vulnerable) or (rumination_detected and high_trauma_exposure):
            violation = AntiPatternViolation(
                antipattern_type=AntiPatternType.TRAUMA_PERPETUATION,
                severity=AntiPatternSeverity.MEDIUM,
                description=(
                    f"Potential trauma perpetuation risk detected: "
                    f"User showing signs of rumination or high trauma exposure."
                ),
                context={
                    'user_cdr': user_cdr,
                    'average_trauma_exposure': avg_trauma if recent_trauma_exposure else 0.0,
                    'access_frequency': user_access_pattern['recent_attempts_hour'],
                    'rumination_risk': user_access_pattern.get('rumination_risk', 'unknown')
                },
                recommendations=[
                    'Monitor user behavior closely',
                    'Suggest alternative content sources',
                    'Gently recommend taking breaks'
                ]
            )
            
            self.violations.append(violation)
            return violation
        
        return None
    
    def _calculate_severity(self, access_frequency: int, cdr: float, 
                          trauma_level: float) -> AntiPatternSeverity:
        """Calculate severity based on multiple factors"""
        # Normalized scores
        freq_score = min(1.0, access_frequency / 20)
        cdr_score = cdr
        trauma_score = trauma_level
        
        # Combined severity score
        severity_score = (freq_score * 0.3 + cdr_score * 0.4 + trauma_score * 0.3)
        
        if severity_score >= 0.8:
            return AntiPatternSeverity.CRITICAL
        elif severity_score >= 0.6:
            return AntiPatternSeverity.HIGH
        elif severity_score >= 0.4:
            return AntiPatternSeverity.MEDIUM
        else:
            return AntiPatternSeverity.LOW
    
    def get_violation_count(self, severity: Optional[AntiPatternSeverity] = None) -> int:
        """Get count of violations, optionally filtered by severity"""
        if severity:
            return sum(1 for v in self.violations if v.severity == severity)
        return len(self.violations)


class TruthDenial:
    """
    Detects Truth Denial antipattern.
    
    This occurs when:
    - Legitimate researchers are denied access to complete historical records
    - Excessive filtering removes important historical context
    - Access restrictions are applied inappropriately
    """
    
    def __init__(self):
        """Initialize truth denial detector"""
        self.violations: List[AntiPatternViolation] = []
        
        # Thresholds for detection
        self.RESEARCHER_DENIAL_THRESHOLD = 3  # Denials in a session
        self.EXCESSIVE_FILTERING_THRESHOLD = 0.5  # 50% trauma reduction
    
    def detect_access_denial(self, user_role: str, denied_count: int,
                           access_reason: str, user_credentials_verified: bool) -> Optional[AntiPatternViolation]:
        """
        Detect truth denial through inappropriate access restrictions.
        
        Args:
            user_role: Role of user being denied
            denied_count: Number of recent denials
            access_reason: Reason for denial
            user_credentials_verified: Whether user has verified credentials
            
        Returns:
            AntiPatternViolation if detected, None otherwise
        """
        # Researchers with verified credentials should rarely be denied
        if user_role == 'researcher' and user_credentials_verified:
            if denied_count >= self.RESEARCHER_DENIAL_THRESHOLD:
                violation = AntiPatternViolation(
                    antipattern_type=AntiPatternType.TRUTH_DENIAL,
                    severity=AntiPatternSeverity.HIGH,
                    description=(
                        f"Truth denial detected: Verified researcher denied access "
                        f"{denied_count} times. This may inappropriately restrict access "
                        f"to complete historical records."
                    ),
                    context={
                        'user_role': user_role,
                        'denied_count': denied_count,
                        'access_reason': access_reason,
                        'credentials_verified': user_credentials_verified
                    },
                    recommendations=[
                        'Review access control logic for researchers',
                        'Consider granting time-limited elevated access',
                        'Verify researcher credentials are properly recognized',
                        'Review TDR filter thresholds for verified researchers',
                        'Provide path for researcher to appeal denial'
                    ]
                )
                
                self.violations.append(violation)
                return violation
        
        # Check for systematic denial patterns that might hide truth
        if denied_count >= 5 and 'immutable' in access_reason.lower():
            violation = AntiPatternViolation(
                antipattern_type=AntiPatternType.TRUTH_DENIAL,
                severity=AntiPatternSeverity.MEDIUM,
                description=(
                    f"Potential truth denial: User repeatedly denied access to "
                    f"immutable archive. May indicate overly restrictive policies."
                ),
                context={
                    'user_role': user_role,
                    'denied_count': denied_count,
                    'access_reason': access_reason
                },
                recommendations=[
                    'Review if access policies are too restrictive',
                    'Provide clear path for legitimate access requests',
                    'Ensure educational alternatives are adequate'
                ]
            )
            
            self.violations.append(violation)
            return violation
        
        return None
    
    def detect_excessive_filtering(self, original_trauma: float, filtered_trauma: float,
                                  important_context_removed: bool) -> Optional[AntiPatternViolation]:
        """
        Detect truth denial through excessive content filtering.
        
        Args:
            original_trauma: Original content trauma level
            filtered_trauma: Filtered content trauma level
            important_context_removed: Whether filtering removed important context
            
        Returns:
            AntiPatternViolation if detected, None otherwise
        """
        trauma_reduction = original_trauma - filtered_trauma
        reduction_ratio = trauma_reduction / original_trauma if original_trauma > 0 else 0
        
        # Check if filtering was excessive
        if reduction_ratio > self.EXCESSIVE_FILTERING_THRESHOLD and important_context_removed:
            violation = AntiPatternViolation(
                antipattern_type=AntiPatternType.TRUTH_DENIAL,
                severity=AntiPatternSeverity.HIGH,
                description=(
                    f"Truth denial through excessive filtering: {reduction_ratio:.1%} "
                    f"trauma reduction removed important historical context."
                ),
                context={
                    'original_trauma': original_trauma,
                    'filtered_trauma': filtered_trauma,
                    'reduction_ratio': reduction_ratio,
                    'context_removed': important_context_removed
                },
                recommendations=[
                    'Review filtering algorithm parameters',
                    'Preserve essential historical facts even if traumatic',
                    'Add contextual notes instead of removing content',
                    'Ensure Educational Archive maintains historical accuracy',
                    'Make unfiltered version available to appropriate users'
                ]
            )
            
            self.violations.append(violation)
            return violation
        
        return None
    
    def get_violation_count(self, severity: Optional[AntiPatternSeverity] = None) -> int:
        """Get count of violations, optionally filtered by severity"""
        if severity:
            return sum(1 for v in self.violations if v.severity == severity)
        return len(self.violations)


class AntiPatternEngine:
    """
    Central engine for detecting and managing ethical antipatterns.
    Integrates with existing Red Code system.
    """
    
    def __init__(self):
        """Initialize antipattern engine"""
        self.trauma_perpetuation = TraumaPerpetuation()
        self.truth_denial = TruthDenial()
        self.all_violations: List[AntiPatternViolation] = []
    
    def check_trauma_perpetuation(self, user_access_pattern: Dict, user_cdr: float,
                                  recent_trauma_exposure: List[float]) -> Optional[AntiPatternViolation]:
        """Check for trauma perpetuation antipattern"""
        violation = self.trauma_perpetuation.detect(
            user_access_pattern, user_cdr, recent_trauma_exposure
        )
        if violation:
            self.all_violations.append(violation)
        return violation
    
    def check_truth_denial_access(self, user_role: str, denied_count: int,
                                  access_reason: str, user_credentials_verified: bool) -> Optional[AntiPatternViolation]:
        """Check for truth denial through access restrictions"""
        violation = self.truth_denial.detect_access_denial(
            user_role, denied_count, access_reason, user_credentials_verified
        )
        if violation:
            self.all_violations.append(violation)
        return violation
    
    def check_truth_denial_filtering(self, original_trauma: float, filtered_trauma: float,
                                    important_context_removed: bool) -> Optional[AntiPatternViolation]:
        """Check for truth denial through excessive filtering"""
        violation = self.truth_denial.detect_excessive_filtering(
            original_trauma, filtered_trauma, important_context_removed
        )
        if violation:
            self.all_violations.append(violation)
        return violation
    
    def get_all_violations(self, antipattern_type: Optional[AntiPatternType] = None,
                          severity: Optional[AntiPatternSeverity] = None) -> List[AntiPatternViolation]:
        """
        Get all violations, optionally filtered by type and severity.
        
        Args:
            antipattern_type: Filter by antipattern type
            severity: Filter by severity level
            
        Returns:
            List of AntiPatternViolation objects
        """
        violations = self.all_violations
        
        if antipattern_type:
            violations = [v for v in violations if v.antipattern_type == antipattern_type]
        
        if severity:
            violations = [v for v in violations if v.severity == severity]
        
        return violations
    
    def get_violation_statistics(self) -> Dict:
        """Get statistics about detected violations"""
        return {
            'total_violations': len(self.all_violations),
            'trauma_perpetuation': self.trauma_perpetuation.get_violation_count(),
            'truth_denial': self.truth_denial.get_violation_count(),
            'by_severity': {
                'critical': len([v for v in self.all_violations if v.severity == AntiPatternSeverity.CRITICAL]),
                'high': len([v for v in self.all_violations if v.severity == AntiPatternSeverity.HIGH]),
                'medium': len([v for v in self.all_violations if v.severity == AntiPatternSeverity.MEDIUM]),
                'low': len([v for v in self.all_violations if v.severity == AntiPatternSeverity.LOW])
            },
            'recent_violations_hour': len([
                v for v in self.all_violations
                if (datetime.utcnow() - datetime.fromisoformat(v.timestamp)).total_seconds() < 3600
            ])
        }
    
    def generate_report(self) -> str:
        """Generate human-readable report of violations"""
        stats = self.get_violation_statistics()
        
        report = "=== PDM AntiPattern Engine Report ===\n\n"
        report += f"Total Violations Detected: {stats['total_violations']}\n"
        report += f"  - Trauma Perpetuation: {stats['trauma_perpetuation']}\n"
        report += f"  - Truth Denial: {stats['truth_denial']}\n\n"
        
        report += "Severity Breakdown:\n"
        report += f"  - Critical: {stats['by_severity']['critical']}\n"
        report += f"  - High: {stats['by_severity']['high']}\n"
        report += f"  - Medium: {stats['by_severity']['medium']}\n"
        report += f"  - Low: {stats['by_severity']['low']}\n\n"
        
        # Add critical violations details
        critical = self.get_all_violations(severity=AntiPatternSeverity.CRITICAL)
        if critical:
            report += "CRITICAL VIOLATIONS:\n"
            for v in critical:
                report += f"  - [{v.antipattern_type.value}] {v.description}\n"
        
        return report
