"""
PDM (Protocollo di Depurazione della Memoria) - Memory Purification Protocol
Implementation of NRE-002 Rule for stratified memory management.

This module provides ethical memory archiving with three-tier access control:
- Immutable Archive (AI): Absolute truth, cryptographically verified
- Educational Archive (AD): Public-facing, trauma-filtered version
- Dynamic Archive (ADi): Optimized for collective wellbeing
"""

__version__ = "1.0.0"
__author__ = "Euystacio-Helmi AI Collective"

from .archive_manager import ArchiveManager, ArchiveType
from .access_control import AccessController, UserRole
from .filters import TemporalDecayFilter, TraumaFilter
from .antipatterns import TraumaPerpetuation, TruthDenial

__all__ = [
    'ArchiveManager',
    'ArchiveType', 
    'AccessController',
    'UserRole',
    'TemporalDecayFilter',
    'TraumaFilter',
    'TraumaPerpetuation',
    'TruthDenial'
]
