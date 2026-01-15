"""
Messaging Layer - Transparent Communication System

Provides traceable communication channels for reporting AIC compliance,
decisions, and status to the Sovereign Collective.

NRE Principles: 004, 009, 013, 017
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class MessageType(Enum):
    """Types of messages sent to Sovereign Collective"""
    COMPLIANCE_REPORT = "compliance_report"
    DECISION_NOTIFICATION = "decision_notification"
    VIOLATION_ALERT = "violation_alert"
    STATE_CHANGE = "state_change"
    ROLLBACK_NOTIFICATION = "rollback_notification"
    SYSTEM_STATUS = "system_status"


class MessagePriority(Enum):
    """Priority levels for messages"""
    INFO = "info"
    NOTICE = "notice"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class Message:
    """Represents a single message to the Sovereign Collective"""
    
    def __init__(self, message_type: MessageType, priority: MessagePriority,
                 content: Dict, nre_principles: List[str] = None):
        self.message_id = self._generate_id()
        self.timestamp = datetime.utcnow().isoformat()
        self.message_type = message_type
        self.priority = priority
        self.content = content
        self.nre_principles = nre_principles or []
        self.signature = self._generate_signature()
        
    def _generate_id(self) -> str:
        """Generate unique message ID"""
        timestamp = datetime.utcnow().isoformat()
        return hashlib.sha256(f"{timestamp}:{id(self)}".encode()).hexdigest()[:16]
    
    def _generate_signature(self) -> str:
        """Generate cryptographic signature for message integrity"""
        message_data = {
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "type": self.message_type.value,
            "content": self.content
        }
        data_str = json.dumps(message_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        """Export message as dictionary"""
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "type": self.message_type.value,
            "priority": self.priority.value,
            "content": self.content,
            "nre_principles": self.nre_principles,
            "signature": self.signature
        }
    
    def to_human_readable(self) -> str:
        """Generate human-readable summary (NRE-004)"""
        summary_parts = [
            f"[{self.priority.value.upper()}] {self.message_type.value}",
            f"Time: {self.timestamp}",
            f"Message ID: {self.message_id}"
        ]
        
        if self.nre_principles:
            summary_parts.append(f"NRE Principles: {', '.join(self.nre_principles)}")
        
        # Add content summary based on type
        if self.message_type == MessageType.VIOLATION_ALERT:
            violations = self.content.get("violations", [])
            summary_parts.append(f"Violations Detected: {', '.join(violations)}")
        elif self.message_type == MessageType.DECISION_NOTIFICATION:
            decision_type = self.content.get("decision_type", "unknown")
            summary_parts.append(f"Decision: {decision_type}")
        
        return "\n".join(summary_parts)


class AuditTrail:
    """
    Immutable audit trail for all significant AIC actions.
    
    Implements NRE-017 (Eternal Witness).
    """
    
    def __init__(self):
        self.entries = []
        self.trail_hash = self._initialize_hash()
        
    def _initialize_hash(self) -> str:
        """Initialize genesis hash for the trail"""
        return hashlib.sha256("EUYSTACIO_AUDIT_TRAIL_GENESIS".encode()).hexdigest()
    
    def add_entry(self, event_type: str, data: Dict, 
                  nre_principles: List[str] = None) -> str:
        """
        Add entry to immutable audit trail.
        
        Returns:
            entry_id
        """
        entry = {
            "entry_id": self._generate_entry_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data,
            "nre_principles": nre_principles or [],
            "previous_hash": self.trail_hash
        }
        
        # Update chain hash
        self.trail_hash = self._hash_entry(entry)
        entry["entry_hash"] = self.trail_hash
        
        self.entries.append(entry)
        return entry["entry_id"]
    
    def _generate_entry_id(self) -> str:
        """Generate unique entry ID"""
        timestamp = datetime.utcnow().isoformat()
        return hashlib.sha256(f"{timestamp}:{len(self.entries)}".encode()).hexdigest()[:16]
    
    def _hash_entry(self, entry: Dict) -> str:
        """Generate hash of entry for chain integrity"""
        entry_str = json.dumps({
            k: v for k, v in entry.items() if k != "entry_hash"
        }, sort_keys=True)
        return hashlib.sha256(entry_str.encode()).hexdigest()
    
    def verify_integrity(self) -> bool:
        """Verify audit trail hasn't been tampered with"""
        current_hash = self._initialize_hash()
        
        for entry in self.entries:
            # Verify chain linkage
            if entry.get("previous_hash") != current_hash:
                return False
            
            # Verify entry hash
            computed_hash = self._hash_entry(entry)
            if entry.get("entry_hash") != computed_hash:
                return False
            
            current_hash = entry["entry_hash"]
        
        return current_hash == self.trail_hash
    
    def search(self, event_type: Optional[str] = None, 
              nre_principle: Optional[str] = None,
              limit: int = 100) -> List[Dict]:
        """Search audit trail with filters"""
        results = self.entries
        
        if event_type:
            results = [e for e in results if e["event_type"] == event_type]
        
        if nre_principle:
            results = [e for e in results if nre_principle in e.get("nre_principles", [])]
        
        # Return most recent first
        return list(reversed(results[-limit:]))


class MessagingLayer:
    """
    Central communication hub for AIC transparency.
    
    Manages all outbound communication to the Sovereign Collective,
    ensuring traceability and compliance with NRE principles.
    """
    
    def __init__(self):
        self.messages = []
        self.audit_trail = AuditTrail()
        self.subscribers = []
        
    def send_compliance_report(self, compliance_data: Dict) -> str:
        """
        Send NRE compliance report to Sovereign Collective.
        
        Implements NRE-004 (Transparency) and NRE-009 (Participatory Governance).
        """
        message = Message(
            message_type=MessageType.COMPLIANCE_REPORT,
            priority=MessagePriority.INFO,
            content=compliance_data,
            nre_principles=["NRE-004", "NRE-009", "NRE-017"]
        )
        
        self._dispatch_message(message)
        self.audit_trail.add_entry("compliance_report", compliance_data, message.nre_principles)
        
        return message.message_id
    
    def send_decision_notification(self, decision: Dict, 
                                   stakeholders_notified: List[str]) -> str:
        """
        Notify stakeholders of significant decisions.
        
        Implements NRE-009 (Participatory Governance) and NRE-013 (Truth in Communication).
        """
        content = {
            "decision": decision,
            "stakeholders_notified": stakeholders_notified,
            "notification_time": datetime.utcnow().isoformat()
        }
        
        message = Message(
            message_type=MessageType.DECISION_NOTIFICATION,
            priority=MessagePriority.NOTICE,
            content=content,
            nre_principles=["NRE-009", "NRE-013", "NRE-017"]
        )
        
        self._dispatch_message(message)
        self.audit_trail.add_entry("decision_notification", content, message.nre_principles)
        
        return message.message_id
    
    def send_violation_alert(self, violations: List[str], 
                           context: Dict, action_taken: str) -> str:
        """
        Alert Sovereign Collective of NRE violations.
        
        Implements NRE-016 (Intervention Threshold).
        """
        content = {
            "violations": violations,
            "context": context,
            "action_taken": action_taken,
            "severity": self._assess_violation_severity(violations)
        }
        
        priority = MessagePriority.CRITICAL if len(violations) > 1 else MessagePriority.WARNING
        
        message = Message(
            message_type=MessageType.VIOLATION_ALERT,
            priority=priority,
            content=content,
            nre_principles=violations + ["NRE-016", "NRE-017"]
        )
        
        self._dispatch_message(message)
        self.audit_trail.add_entry("violation_alert", content, message.nre_principles)
        
        return message.message_id
    
    def send_rollback_notification(self, rollback_event: Dict) -> str:
        """
        Notify of system rollback event.
        
        Implements NRE-016 (Intervention) and NRE-018 (Self-Correction).
        """
        message = Message(
            message_type=MessageType.ROLLBACK_NOTIFICATION,
            priority=MessagePriority.CRITICAL,
            content=rollback_event,
            nre_principles=["NRE-016", "NRE-017", "NRE-018"]
        )
        
        self._dispatch_message(message)
        self.audit_trail.add_entry("rollback_notification", rollback_event, message.nre_principles)
        
        return message.message_id
    
    def send_state_change(self, old_state: str, new_state: str, 
                         reason: str) -> str:
        """
        Announce system state changes.
        
        Implements NRE-004 (Transparency).
        """
        content = {
            "old_state": old_state,
            "new_state": new_state,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        message = Message(
            message_type=MessageType.STATE_CHANGE,
            priority=MessagePriority.NOTICE,
            content=content,
            nre_principles=["NRE-004", "NRE-017"]
        )
        
        self._dispatch_message(message)
        self.audit_trail.add_entry("state_change", content, message.nre_principles)
        
        return message.message_id
    
    def _dispatch_message(self, message: Message):
        """Dispatch message to all subscribers"""
        self.messages.append(message)
        
        # Notify subscribers
        for subscriber in self.subscribers:
            subscriber.receive_message(message)
    
    def _assess_violation_severity(self, violations: List[str]) -> str:
        """Assess overall severity of violations"""
        critical_principles = ["NRE-001", "NRE-011", "NRE-015", "NRE-016"]
        
        if any(v in critical_principles for v in violations):
            return "critical"
        elif len(violations) > 2:
            return "high"
        else:
            return "moderate"
    
    def get_recent_messages(self, limit: int = 50, 
                           message_type: Optional[MessageType] = None) -> List[Dict]:
        """Retrieve recent messages"""
        messages = self.messages
        
        if message_type:
            messages = [m for m in messages if m.message_type == message_type]
        
        # Return most recent
        recent = list(reversed(messages[-limit:]))
        return [m.to_dict() for m in recent]
    
    def subscribe(self, subscriber):
        """
        Subscribe to message notifications.
        
        Args:
            subscriber: Object with a receive_message(message) method
        """
        # Validate subscriber has required method
        if not hasattr(subscriber, 'receive_message') or not callable(getattr(subscriber, 'receive_message')):
            raise TypeError("Subscriber must have a callable 'receive_message' method")
        
        self.subscribers.append(subscriber)
    
    def get_audit_trail_summary(self) -> Dict:
        """Get summary of audit trail"""
        return {
            "total_entries": len(self.audit_trail.entries),
            "trail_hash": self.audit_trail.trail_hash,
            "integrity_verified": self.audit_trail.verify_integrity(),
            "recent_entries": self.audit_trail.search(limit=10)
        }


# Singleton instance
_messaging_layer_instance = None

def get_messaging_layer() -> MessagingLayer:
    """Get global messaging layer instance"""
    global _messaging_layer_instance
    if _messaging_layer_instance is None:
        _messaging_layer_instance = MessagingLayer()
    return _messaging_layer_instance
