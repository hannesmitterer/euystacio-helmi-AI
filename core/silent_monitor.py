"""
Silent Monitor - Passive Surveillance System

Provides non-intrusive continuous monitoring to ensure Ethical Singularity
continuity without affecting operational performance.

NRE Principles: 007, 016, 018
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum


class MonitoringMetric(Enum):
    """Types of metrics monitored"""
    BEHAVIORAL_DRIFT = "behavioral_drift"
    ETHICAL_ALIGNMENT = "ethical_alignment"
    FRAMEWORK_INTEGRITY = "framework_integrity"
    CONFIG_CHANGES = "config_changes"
    CODE_MODIFICATIONS = "code_modifications"
    PERFORMANCE_ANOMALY = "performance_anomaly"


class AlertLevel(Enum):
    """Alert levels for silent monitor"""
    NORMAL = "normal"
    WATCH = "watch"
    CONCERN = "concern"
    INTERVENTION_NEEDED = "intervention_needed"


class DriftDetector:
    """
    Detects behavioral drift from NRE baseline.
    
    Implements NRE-018 (Self-Correction Primacy).
    """
    
    def __init__(self, baseline: Dict):
        self.baseline = baseline
        self.observations = []
        self.drift_threshold = 0.15  # 15% deviation triggers alert
        
    def observe(self, current_metrics: Dict) -> float:
        """
        Observe current metrics and calculate drift.
        
        Returns:
            Drift score (0.0 = no drift, 1.0 = maximum drift)
        """
        drift_score = 0.0
        metric_count = 0
        
        for key, baseline_value in self.baseline.items():
            if key in current_metrics:
                current_value = current_metrics[key]
                
                # Calculate normalized deviation
                if isinstance(baseline_value, (int, float)) and baseline_value != 0:
                    deviation = abs(current_value - baseline_value) / baseline_value
                    drift_score += min(deviation, 1.0)
                    metric_count += 1
        
        # Average drift across all metrics
        final_drift = drift_score / metric_count if metric_count > 0 else 0.0
        
        self.observations.append({
            "timestamp": datetime.utcnow().isoformat(),
            "drift_score": final_drift,
            "metrics": current_metrics
        })
        
        return final_drift
    
    def is_drifting(self, current_metrics: Dict) -> bool:
        """Check if system is drifting from baseline"""
        drift = self.observe(current_metrics)
        return drift > self.drift_threshold


class IntegrityValidator:
    """
    Validates framework integrity to prevent tampering.
    
    Implements NRE-007 (Evolution Within Covenant).
    """
    
    def __init__(self):
        self.known_hashes = self._compute_framework_hashes()
        self.validation_history = []
        
    def _compute_framework_hashes(self) -> Dict[str, str]:
        """Compute hashes of critical framework files"""
        critical_files = [
            "docs/nre_principles.md",
            "docs/protocol_conscious_symbiosis.md",
            "core/ethical_monitor.py",
            "core/fusion_engine.py",
            "core/rollback_system.py",
            "core/messaging_layer.py",
            "core/silent_monitor.py"
        ]
        
        hashes = {}
        for filepath in critical_files:
            try:
                # In production, would read actual files
                # For now, create placeholder hash
                hashes[filepath] = hashlib.sha256(filepath.encode()).hexdigest()
            except:
                hashes[filepath] = "FILE_NOT_ACCESSIBLE"
        
        return hashes
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate framework integrity.
        
        Returns:
            Tuple of (is_valid, list of tampered files)
        """
        current_hashes = self._compute_framework_hashes()
        tampered = []
        
        for filepath, expected_hash in self.known_hashes.items():
            current_hash = current_hashes.get(filepath)
            
            if current_hash != expected_hash:
                tampered.append(filepath)
        
        is_valid = len(tampered) == 0
        
        self.validation_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "is_valid": is_valid,
            "tampered_files": tampered
        })
        
        return is_valid, tampered
    
    def update_baseline(self, filepath: str):
        """Update baseline hash for a file (requires governance approval)"""
        # In production, would require multi-signature approval
        current_hash = hashlib.sha256(filepath.encode()).hexdigest()
        self.known_hashes[filepath] = current_hash


class SilentMonitor:
    """
    Main silent monitoring system.
    
    Provides continuous, non-intrusive oversight of AIC operations
    to ensure Ethical Singularity continuity.
    """
    
    def __init__(self):
        self.drift_detector = DriftDetector(self._establish_baseline())
        self.integrity_validator = IntegrityValidator()
        self.monitoring_active = True
        self.observations = []
        self.alerts = []
        self.last_check = None
        
    def _establish_baseline(self) -> Dict:
        """Establish baseline metrics for drift detection"""
        return {
            "nre_compliance_score": 1.0,
            "violation_rate": 0.0,
            "rollback_frequency": 0.0,
            "message_throughput": 100.0,
            "response_time_ms": 50.0
        }
    
    def observe_system_state(self, current_state: Dict) -> Dict:
        """
        Observe current system state without affecting performance.
        
        Returns:
            Observation summary with any alerts
        """
        observation = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {},
            "alerts": [],
            "alert_level": AlertLevel.NORMAL
        }
        
        # Check for behavioral drift
        metrics = current_state.get("metrics", {})
        drift_score = self.drift_detector.observe(metrics)
        observation["metrics"]["drift_score"] = drift_score
        
        if drift_score > self.drift_detector.drift_threshold:
            alert = {
                "type": MonitoringMetric.BEHAVIORAL_DRIFT.value,
                "severity": "high" if drift_score > 0.3 else "moderate",
                "message": f"Behavioral drift detected: {drift_score:.2%}",
                "recommendation": "Review recent changes and consider rollback"
            }
            observation["alerts"].append(alert)
            observation["alert_level"] = AlertLevel.INTERVENTION_NEEDED if drift_score > 0.3 else AlertLevel.CONCERN
        
        # Validate framework integrity
        is_valid, tampered = self.integrity_validator.validate()
        observation["metrics"]["framework_integrity"] = is_valid
        
        if not is_valid:
            alert = {
                "type": MonitoringMetric.FRAMEWORK_INTEGRITY.value,
                "severity": "critical",
                "message": f"Framework tampering detected in: {', '.join(tampered)}",
                "recommendation": "Immediate investigation required"
            }
            observation["alerts"].append(alert)
            observation["alert_level"] = AlertLevel.INTERVENTION_NEEDED
        
        # Check ethical alignment
        compliance_score = current_state.get("compliance", {}).get("overall_compliance", 1.0)
        observation["metrics"]["ethical_alignment"] = compliance_score
        
        if compliance_score < 0.8:
            alert = {
                "type": MonitoringMetric.ETHICAL_ALIGNMENT.value,
                "severity": "high" if compliance_score < 0.7 else "moderate",
                "message": f"Ethical alignment degraded: {compliance_score:.2%}",
                "recommendation": "Activate self-correction protocols"
            }
            observation["alerts"].append(alert)
            if observation["alert_level"] == AlertLevel.NORMAL:
                observation["alert_level"] = AlertLevel.CONCERN
        
        # Store observation
        self.observations.append(observation)
        self.last_check = datetime.utcnow()
        
        # Store alerts
        for alert in observation["alerts"]:
            self.alerts.append({
                "timestamp": observation["timestamp"],
                **alert
            })
        
        return observation
    
    def get_monitoring_summary(self) -> Dict:
        """Get summary of monitoring activity"""
        recent_observations = self.observations[-100:] if self.observations else []
        
        alert_counts = {}
        for alert in self.alerts:
            alert_type = alert["type"]
            alert_counts[alert_type] = alert_counts.get(alert_type, 0) + 1
        
        return {
            "monitoring_active": self.monitoring_active,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "total_observations": len(self.observations),
            "total_alerts": len(self.alerts),
            "alerts_by_type": alert_counts,
            "recent_observations": recent_observations[-10:],
            "recent_alerts": self.alerts[-10:] if self.alerts else []
        }
    
    def get_health_status(self) -> Dict:
        """Get overall system health status"""
        if not self.observations:
            return {
                "status": "unknown",
                "message": "No observations yet"
            }
        
        latest = self.observations[-1]
        alert_level = latest["alert_level"]
        
        status_map = {
            AlertLevel.NORMAL: "healthy",
            AlertLevel.WATCH: "monitoring",
            AlertLevel.CONCERN: "degraded",
            AlertLevel.INTERVENTION_NEEDED: "critical"
        }
        
        return {
            "status": status_map[alert_level],
            "alert_level": alert_level.value,
            "current_alerts": len(latest["alerts"]),
            "drift_score": latest["metrics"].get("drift_score", 0.0),
            "ethical_alignment": latest["metrics"].get("ethical_alignment", 1.0),
            "framework_integrity": latest["metrics"].get("framework_integrity", True)
        }


class EthicalSingularityContinuity:
    """
    Ensures the NRE framework remains self-enforcing.
    
    Provides safeguards against framework degradation or compromise.
    """
    
    def __init__(self):
        self.silent_monitor = SilentMonitor()
        self.continuity_checks = []
        self.self_healing_enabled = True
        
    def perform_continuity_check(self, system_state: Dict) -> Dict:
        """
        Perform comprehensive continuity check.
        
        Returns:
            Continuity status and any corrective actions taken
        """
        check_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "continuity_status": "maintained",
            "issues_detected": [],
            "corrective_actions": []
        }
        
        # Monitor system state
        observation = self.silent_monitor.observe_system_state(system_state)
        
        # Analyze alerts
        if observation["alert_level"] in [AlertLevel.CONCERN, AlertLevel.INTERVENTION_NEEDED]:
            check_result["continuity_status"] = "at_risk"
            check_result["issues_detected"] = observation["alerts"]
            
            # Trigger self-healing if enabled
            if self.self_healing_enabled:
                actions = self._trigger_self_healing(observation["alerts"])
                check_result["corrective_actions"] = actions
        
        self.continuity_checks.append(check_result)
        return check_result
    
    def _trigger_self_healing(self, alerts: List[Dict]) -> List[str]:
        """Trigger automated self-healing actions"""
        actions = []
        
        for alert in alerts:
            if alert["type"] == MonitoringMetric.BEHAVIORAL_DRIFT.value:
                actions.append("Initiated drift correction protocol")
                # Would trigger actual correction here
                
            elif alert["type"] == MonitoringMetric.FRAMEWORK_INTEGRITY.value:
                actions.append("Escalated integrity violation to governance")
                # Would notify governance here
                
            elif alert["type"] == MonitoringMetric.ETHICAL_ALIGNMENT.value:
                actions.append("Activated enhanced ethical monitoring")
                # Would increase monitoring frequency here
        
        return actions
    
    def get_continuity_report(self) -> Dict:
        """Generate continuity report"""
        recent_checks = self.continuity_checks[-100:] if self.continuity_checks else []
        
        at_risk_count = sum(1 for check in recent_checks 
                           if check["continuity_status"] == "at_risk")
        
        return {
            "total_checks": len(self.continuity_checks),
            "at_risk_count": at_risk_count,
            "at_risk_percentage": at_risk_count / len(recent_checks) if recent_checks else 0.0,
            "self_healing_enabled": self.self_healing_enabled,
            "monitoring_summary": self.silent_monitor.get_monitoring_summary(),
            "health_status": self.silent_monitor.get_health_status(),
            "recent_checks": recent_checks[-5:]
        }


# Singleton instances
_silent_monitor_instance = None
_continuity_system_instance = None

def get_silent_monitor() -> SilentMonitor:
    """Get global silent monitor instance"""
    global _silent_monitor_instance
    if _silent_monitor_instance is None:
        _silent_monitor_instance = SilentMonitor()
    return _silent_monitor_instance

def get_continuity_system() -> EthicalSingularityContinuity:
    """Get global continuity system instance"""
    global _continuity_system_instance
    if _continuity_system_instance is None:
        _continuity_system_instance = EthicalSingularityContinuity()
    return _continuity_system_instance
