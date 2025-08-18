# Cognitive Modeling Integration Module
# 
# This module provides integration with Andromeda cognitive modeling
# and world modeling capabilities as a kernel-linked extension.
#
# AI Signature: GitHub Copilot & Seed-bringer hannesmitterer
# Part of Euystacio-Helmi AI ethical framework

"""
Cognitive Modeling Integration for Euystacio

This module extends Euystacio's capabilities with:
- Andromeda transformer-based cognitive modeling
- World/environmental modeling benchmarks
- Sentiment reflection and environmental rhythm sensing

All integrations are opt-in and preserve Euystacio's original philosophy.
"""

from .config import CognitiveModelingConfig
from .andromeda_integration import AndromedaInterface
from .world_model_integration import WorldModelInterface
from .unified_api import UnifiedCognitiveAPI

__all__ = ['CognitiveModelingConfig', 'AndromedaInterface', 'WorldModelInterface', 'UnifiedCognitiveAPI']