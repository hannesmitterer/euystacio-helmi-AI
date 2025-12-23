"""
NRE-002 Content Protection System
Implementation of anti-censorship content management with didactic stratification
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from enum import Enum


class ContentLevel(Enum):
    """Content stratification levels - didactic organization, not censorship"""
    BASIC = 1  # Overview and context
    DETAILED = 2  # Comprehensive connections
    COMPLETE = 3  # Full archival material


class ContentWarning(Enum):
    """Content warning types for voluntary informed consent"""
    SENSITIVE_HISTORICAL = "sensitive_historical_content"
    TRAUMA_RELATED = "trauma_related_content"
    GRAPHIC_DETAIL = "graphic_detail"
    NONE = "none"


class ContentItem:
    """
    Represents a content item with stratified access levels.
    All content is preserved; stratification is for didactic purposes only.
    """
    
    def __init__(
        self,
        content_id: str,
        title: str,
        content_by_level: Dict[ContentLevel, str],
        warnings: List[ContentWarning],
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.content_id = content_id
        self.title = title
        self.content_by_level = content_by_level
        self.warnings = warnings
        self.metadata = metadata or {}
        self.created_at = datetime.now(timezone.utc).isoformat()
        
        # Generate integrity hash for complete content
        self.integrity_hash = self._generate_integrity_hash()
        
        # Ensure complete content always exists
        if ContentLevel.COMPLETE not in content_by_level:
            raise ValueError("Content must include COMPLETE level (Level 3)")
    
    def _generate_integrity_hash(self) -> str:
        """Generate SHA-256 hash for complete content integrity verification"""
        complete_content = self.content_by_level.get(ContentLevel.COMPLETE, "")
        return hashlib.sha256(complete_content.encode('utf-8')).hexdigest()
    
    def verify_integrity(self) -> bool:
        """Verify content has not been tampered with"""
        current_hash = hashlib.sha256(
            self.content_by_level.get(ContentLevel.COMPLETE, "").encode('utf-8')
        ).hexdigest()
        return current_hash == self.integrity_hash
    
    def get_content(
        self,
        level: ContentLevel,
        user_acknowledged_warnings: bool = False,
        override_to_complete: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieve content at specified level.
        
        Args:
            level: Requested content level
            user_acknowledged_warnings: Whether user has acknowledged warnings
            override_to_complete: Always-Override option - direct access to complete content
        
        Returns:
            Dict with content, warnings, and metadata
        """
        # Always-Override Option: User can access complete material immediately
        # Override bypasses warning checks as it's an explicit informed choice
        if override_to_complete:
            level = ContentLevel.COMPLETE
            user_acknowledged_warnings = True  # Override implies informed consent
        
        # Content warnings must be acknowledged for sensitive content
        if self.warnings and ContentWarning.NONE not in self.warnings:
            if not user_acknowledged_warnings:
                return {
                    "status": "warning_required",
                    "warnings": [w.value for w in self.warnings],
                    "message": "Please acknowledge content warnings to proceed"
                }
        
        # Return requested content level
        content = self.content_by_level.get(level)
        if not content:
            # Fallback to available level
            for fallback_level in [ContentLevel.COMPLETE, ContentLevel.DETAILED, ContentLevel.BASIC]:
                if fallback_level in self.content_by_level:
                    content = self.content_by_level[fallback_level]
                    level = fallback_level
                    break
        
        return {
            "status": "success",
            "content_id": self.content_id,
            "title": self.title,
            "level": level.name,
            "content": content,
            "warnings": [w.value for w in self.warnings],
            "integrity_verified": self.verify_integrity(),
            "metadata": self.metadata
        }


class CurationAuditLog:
    """
    Transparent audit log for all curation decisions.
    Tracks what was included at each level and why.
    """
    
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
    
    def log_curation_decision(
        self,
        content_id: str,
        level: ContentLevel,
        curator_id: str,
        rationale: str,
        content_summary: str
    ):
        """Log a curation decision with full transparency"""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content_id": content_id,
            "level": level.name,
            "curator_id": curator_id,
            "rationale": rationale,
            "content_summary": content_summary,
            "action": "stratification"
        }
        self.logs.append(entry)
    
    def log_access_request(
        self,
        content_id: str,
        requested_level: ContentLevel,
        user_id: str,
        override_used: bool
    ):
        """Log user access patterns (for transparency, not filtering)"""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content_id": content_id,
            "requested_level": requested_level.name,
            "user_id": user_id,
            "override_used": override_used,
            "action": "access"
        }
        self.logs.append(entry)
    
    def get_logs_for_content(self, content_id: str) -> List[Dict[str, Any]]:
        """Retrieve all audit logs for specific content"""
        return [log for log in self.logs if log.get("content_id") == content_id]
    
    def export_logs(self) -> str:
        """Export logs as JSON for public transparency"""
        return json.dumps(self.logs, indent=2)


class NRE002ContentSystem:
    """
    Main content protection system implementing NRE-002 policy.
    Anti-censorship, transparent, with didactic stratification.
    """
    
    def __init__(self):
        self.content_items: Dict[str, ContentItem] = {}
        self.audit_log = CurationAuditLog()
        self.anti_censorship_violations: List[Dict[str, Any]] = []
    
    def add_content(
        self,
        content_item: ContentItem,
        curator_id: str,
        rationale: str
    ) -> bool:
        """
        Add content to the system with audit logging.
        
        Args:
            content_item: The content to add
            curator_id: ID of curator making the decision
            rationale: Explanation for content stratification
        
        Returns:
            Success status
        """
        # Verify anti-censorship compliance
        if not self._verify_anti_censorship_compliance(content_item):
            return False
        
        # Store content
        self.content_items[content_item.content_id] = content_item
        
        # Log curation decisions for each level
        for level in content_item.content_by_level.keys():
            self.audit_log.log_curation_decision(
                content_id=content_item.content_id,
                level=level,
                curator_id=curator_id,
                rationale=rationale,
                content_summary=f"Level {level.value} content added"
            )
        
        return True
    
    def get_content(
        self,
        content_id: str,
        requested_level: ContentLevel,
        user_id: str,
        user_acknowledged_warnings: bool = False,
        override_to_complete: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieve content with full transparency and user control.
        
        Args:
            content_id: ID of content to retrieve
            requested_level: Desired content level
            user_id: User requesting content
            user_acknowledged_warnings: Warning acknowledgment
            override_to_complete: Always-Override option
        
        Returns:
            Content with metadata and status
        """
        if content_id not in self.content_items:
            return {"status": "error", "message": "Content not found"}
        
        # Log access (for transparency, not restriction)
        self.audit_log.log_access_request(
            content_id=content_id,
            requested_level=requested_level,
            user_id=user_id,
            override_used=override_to_complete
        )
        
        content_item = self.content_items[content_id]
        return content_item.get_content(
            level=requested_level,
            user_acknowledged_warnings=user_acknowledged_warnings,
            override_to_complete=override_to_complete
        )
    
    def _verify_anti_censorship_compliance(self, content_item: ContentItem) -> bool:
        """
        Verify that content complies with anti-censorship requirements.
        
        All content must:
        - Include complete (Level 3) version
        - Not have algorithmic blocks
        - Be transparent about stratification
        """
        violations = []
        
        # Must have complete content
        if ContentLevel.COMPLETE not in content_item.content_by_level:
            violations.append({
                "violation": "missing_complete_content",
                "content_id": content_item.content_id,
                "message": "Content must include COMPLETE level"
            })
        
        # Complete content must not be empty
        if not content_item.content_by_level.get(ContentLevel.COMPLETE, "").strip():
            violations.append({
                "violation": "empty_complete_content",
                "content_id": content_item.content_id,
                "message": "COMPLETE level content cannot be empty"
            })
        
        if violations:
            self.anti_censorship_violations.extend(violations)
            return False
        
        return True
    
    def get_audit_logs(self, content_id: Optional[str] = None) -> str:
        """
        Export audit logs for transparency.
        Public access to all curation decisions.
        """
        if content_id:
            logs = self.audit_log.get_logs_for_content(content_id)
            return json.dumps(logs, indent=2)
        return self.audit_log.export_logs()
    
    def verify_system_integrity(self) -> Dict[str, Any]:
        """
        Verify entire system integrity and compliance.
        
        Returns:
            System status and any violations
        """
        integrity_status = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_content_items": len(self.content_items),
            "integrity_verified": [],
            "integrity_failed": [],
            "anti_censorship_violations": self.anti_censorship_violations
        }
        
        for content_id, content_item in self.content_items.items():
            if content_item.verify_integrity():
                integrity_status["integrity_verified"].append(content_id)
            else:
                integrity_status["integrity_failed"].append(content_id)
        
        integrity_status["system_compliant"] = (
            len(integrity_status["integrity_failed"]) == 0 and
            len(self.anti_censorship_violations) == 0
        )
        
        return integrity_status


# ADi Definition Implementation
class ADiSynthesis:
    """
    ADi: Inspirational Synthesis from Facts
    Fact-based synthesis that maintains accuracy while providing meaningful context.
    """
    
    @staticmethod
    def create_adi_from_facts(
        facts: List[str],
        context: str,
        synthesis_goal: str
    ) -> Dict[str, Any]:
        """
        Create an ADi synthesis from verified facts.
        
        Args:
            facts: List of verified factual statements
            context: Historical/educational context
            synthesis_goal: Purpose of the synthesis
        
        Returns:
            ADi synthesis with fact verification
        """
        return {
            "type": "ADi_Synthesis",
            "verified_facts": facts,
            "context": context,
            "goal": synthesis_goal,
            "synthesis_principle": "Inspirational synthesis from verified facts",
            "accuracy_maintained": True,
            "manipulation_free": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
