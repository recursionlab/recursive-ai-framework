"""
Recursive Memory Engine
Persistent memory system for accumulating recursive intelligence across LLM conversations

This solves the fundamental problem: LLMs reset every session.
With this, they can start from φₙ instead of φ₀.
"""

from .core.collapse_detector import CollapseDetector, CollapseEvent, CollapseType
from .core.residue_extractor import ResidueExtractor, SemanticResidue
from .storage.memory_graph import RecursiveMemoryGraph
from .core.integration_generator import IntegrationPromptGenerator

__version__ = "1.0.0"
__all__ = [
    "CollapseDetector",
    "CollapseEvent",
    "CollapseType",
    "ResidueExtractor",
    "SemanticResidue",
    "RecursiveMemoryGraph",
    "IntegrationPromptGenerator"
]
