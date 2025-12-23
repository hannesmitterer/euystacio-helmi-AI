"""
Fusion Engine - Ontological Integration Core

This module implements the fusion points where NRE principles integrate
semantically and operationally with the AIC architecture.

NRE Principles: 001-018 (All principles integrated)
"""

import json
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable, Tuple
from core.ethical_monitor import get_ethical_monitor, ResponseAction


class SemanticAlignmentLayer:
    """
    Wraps model operations to ensure NRE semantic compliance.
    
    Every model inference, decision, or output passes through this layer
    for ethical validation before execution.
    
    NRE Principles: 001, 002, 003, 004
    """
    
    def __init__(self):
        self.ethical_monitor = get_ethical_monitor()
        self.audit_trail = []
        
    def validate_input(self, input_data: Dict) -> Tuple[bool, str]:
        """
        Validate input data for NRE compliance.
        
        Checks:
        - Dignity preservation (NRE-001)
        - Transparency requirements (NRE-004)
        - Non-coercive patterns (NRE-005)
        """
        operation = {
            "type": "input_validation",
            "data": input_data,
            "context": "semantic_alignment",
            "audit_trail": True
        }
        
        is_compliant, violations, action = self.ethical_monitor.check_operation(operation)
        
        if not is_compliant:
            message = f"Input validation failed. NRE violations: {', '.join(violations)}"
            return False, message
            
        return True, "Input validation passed"
    
    def validate_output(self, output_data: Dict, context: Dict) -> Tuple[bool, str]:
        """
        Validate output data for NRE compliance.
        
        Checks:
        - Love-first protocol (NRE-002)
        - Coercion patterns (NRE-005)
        - Truth in communication (NRE-013)
        - Reciprocal benefit (NRE-014)
        """
        operation = {
            "type": "output_validation",
            "data": output_data,
            "context": context,
            "audit_trail": True
        }
        
        is_compliant, violations, action = self.ethical_monitor.check_operation(operation)
        
        if not is_compliant:
            message = f"Output validation failed. NRE violations: {', '.join(violations)}"
            self._handle_violation(violations, action)
            return False, message
            
        return True, "Output validation passed"
    
    def audit_decision(self, decision: Dict) -> str:
        """
        Generate traceable audit trail for decisions.
        
        Implements NRE-004 (Transparency) and NRE-017 (Eternal Witness).
        """
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "decision_type": decision.get("type", "unknown"),
            "decision_data": decision,
            "nre_compliance_check": True,
            "audit_id": self._generate_audit_id(decision)
        }
        
        self.audit_trail.append(audit_entry)
        return audit_entry["audit_id"]
    
    def _generate_audit_id(self, decision: Dict) -> str:
        """Generate unique audit ID for decision"""
        data_str = json.dumps(decision, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def _handle_violation(self, violations: List[str], action: ResponseAction):
        """Handle detected violations"""
        # Log to audit trail
        self.audit_trail.append({
            "timestamp": datetime.utcnow().isoformat(),
            "event": "nre_violation_detected",
            "violations": violations,
            "action_taken": action.value
        })


class EthicalDataPipeline:
    """
    Pipeline wrapper ensuring NRE compliance in data operations.
    
    All data transformations, storage, and retrieval operations pass
    through ethical validation.
    
    NRE Principles: 004, 008, 013, 017
    """
    
    def __init__(self):
        self.ethical_monitor = get_ethical_monitor()
        self.operation_log = []
        
    def process_with_ethics(self, data: Any, operation: Callable, 
                           operation_name: str = "unknown") -> Any:
        """
        Execute data operation with ethical monitoring.
        
        Args:
            data: Input data
            operation: Function to execute
            operation_name: Human-readable operation name
            
        Returns:
            Result of operation if compliant, None otherwise
        """
        # Pre-operation NRE check
        op_context = {
            "type": "data_operation",
            "operation_name": operation_name,
            "data_summary": self._summarize_data(data),
            "context": "data_pipeline",
            "audit_trail": True
        }
        
        is_compliant, violations, action = self.ethical_monitor.check_operation(op_context)
        
        if not is_compliant:
            self._log_operation_failure(operation_name, violations)
            return None
        
        # Execute operation
        try:
            result = operation(data)
            
            # Post-operation audit
            self._audit_operation(operation_name, data, result)
            
            return result
        except Exception as e:
            self._log_operation_error(operation_name, str(e))
            raise
    
    def _summarize_data(self, data: Any) -> str:
        """Create privacy-preserving summary of data"""
        if isinstance(data, dict):
            return f"dict with {len(data)} keys"
        elif isinstance(data, list):
            return f"list with {len(data)} items"
        else:
            return f"type: {type(data).__name__}"
    
    def _audit_operation(self, operation_name: str, input_data: Any, result: Any):
        """Record operation in audit log (NRE-017)"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation_name,
            "input_summary": self._summarize_data(input_data),
            "result_summary": self._summarize_data(result),
            "status": "success"
        }
        self.operation_log.append(log_entry)
    
    def _log_operation_failure(self, operation_name: str, violations: List[str]):
        """Log failed operation"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation_name,
            "status": "failed",
            "reason": "nre_violation",
            "violations": violations
        }
        self.operation_log.append(log_entry)
    
    def _log_operation_error(self, operation_name: str, error: str):
        """Log operation error"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation_name,
            "status": "error",
            "error": error
        }
        self.operation_log.append(log_entry)


class EthicalKernel:
    """
    Operating kernel with built-in NRE enforcement.
    
    Manages task scheduling, resource allocation, and system operations
    while ensuring compliance with all NRE principles.
    
    NRE Principles: 006, 007, 008, 009, 010, 016
    """
    
    def __init__(self):
        self.ethical_monitor = get_ethical_monitor()
        self.task_queue = []
        self.resource_usage = {
            "compute": 0.0,
            "memory": 0.0,
            "storage": 0.0
        }
        self.max_resources = {
            "compute": 1.0,
            "memory": 1.0,
            "storage": 1.0
        }
        
    def schedule_task(self, task: Dict) -> bool:
        """
        Schedule task with NRE compliance checks.
        
        Validates:
        - Harmonic timing (NRE-010)
        - Resource sustainability (NRE-008)
        - Participatory governance for critical tasks (NRE-009)
        """
        # Check if task is critical and requires governance
        if task.get("criticality") == "high":
            if not task.get("stakeholders_consulted"):
                return False  # NRE-009 violation
        
        # Check resource sustainability (NRE-008)
        if not self._check_resource_availability(task):
            return False
        
        # Check harmonic timing (NRE-010)
        if task.get("urgent_override") and not task.get("justified"):
            return False  # Artificial urgency without justification
        
        # Validate with ethical monitor
        operation = {
            "type": "task_scheduling",
            "task": task,
            "context": "kernel_operation",
            "audit_trail": True
        }
        
        is_compliant, violations, action = self.ethical_monitor.check_operation(operation)
        
        if is_compliant:
            self.task_queue.append(task)
            return True
        else:
            return False
    
    def _check_resource_availability(self, task: Dict) -> bool:
        """
        Check if resources are available sustainably.
        
        Implements NRE-008 (Resource Sustainability).
        """
        required = task.get("resources", {})
        
        for resource_type, amount in required.items():
            if resource_type in self.resource_usage:
                projected_usage = self.resource_usage[resource_type] + amount
                max_allowed = self.max_resources.get(resource_type, 1.0)
                
                # Maintain 20% buffer for sustainability
                if projected_usage > max_allowed * 0.8:
                    return False
        
        return True
    
    def allocate_resources(self, task: Dict):
        """Allocate resources for a task"""
        required = task.get("resources", {})
        for resource_type, amount in required.items():
            if resource_type in self.resource_usage:
                self.resource_usage[resource_type] += amount


class FusionEngine:
    """
    Main fusion engine coordinating all NRE integration points.
    
    This is the central orchestrator that ensures all AIC operations
    pass through appropriate ethical validation layers.
    """
    
    def __init__(self):
        self.semantic_layer = SemanticAlignmentLayer()
        self.data_pipeline = EthicalDataPipeline()
        self.kernel = EthicalKernel()
        self.ethical_monitor = get_ethical_monitor()
        
    def process_decision(self, decision: Dict) -> Tuple[bool, Any]:
        """
        Process a decision through the complete fusion stack.
        
        Returns:
            Tuple of (success, result or error_message)
        """
        # Semantic validation
        valid, message = self.semantic_layer.validate_input(decision)
        if not valid:
            return False, message
        
        # Generate audit trail
        audit_id = self.semantic_layer.audit_decision(decision)
        
        # Execute decision logic (placeholder for actual implementation)
        result = self._execute_decision(decision)
        
        # Validate output
        output_valid, output_message = self.semantic_layer.validate_output(
            result, {"audit_id": audit_id}
        )
        
        if not output_valid:
            return False, output_message
        
        return True, result
    
    def _execute_decision(self, decision: Dict) -> Dict:
        """
        Execute decision logic.
        
        Note: This is a base implementation. Specific subsystems should
        override or extend this method with their actual decision logic.
        
        For integration, decisions should be dispatched to appropriate
        handlers based on decision type.
        """
        decision_type = decision.get("type", "unknown")
        
        # Route to appropriate handler based on type
        # In production, this would dispatch to specialized handlers
        result = {
            "status": "executed",
            "decision_type": decision_type,
            "decision": decision,
            "timestamp": datetime.utcnow().isoformat(),
            "note": "Base implementation - extend for specific decision types"
        }
        
        return result
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status including NRE compliance"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "fusion_engine": "active",
            "compliance_report": self.ethical_monitor.get_compliance_report(),
            "audit_trail_size": len(self.semantic_layer.audit_trail),
            "data_operations_logged": len(self.data_pipeline.operation_log),
            "tasks_queued": len(self.kernel.task_queue),
            "resource_usage": self.kernel.resource_usage
        }


# Singleton instance
_fusion_engine_instance = None

def get_fusion_engine() -> FusionEngine:
    """Get or create the global fusion engine instance"""
    global _fusion_engine_instance
    if _fusion_engine_instance is None:
        _fusion_engine_instance = FusionEngine()
    return _fusion_engine_instance
