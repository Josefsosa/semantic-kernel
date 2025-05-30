"""
ACN RAI Memory Module for Semantic Kernel
A comprehensive memory management system providing observable behavior tracking,
human-understandable decision explanations, and advanced graph-based memory organization.
"""

from .core.rai_graph import RAIMemoryGraph
from .core.observable_memory import ObservableBehavior
from .core.behavioral_analysis import BehavioralAnalyzer
from .core.human_understanding import HumanUnderstandingModule

__version__ = "0.1.0"
__author__ = "ACN RAI Team"

__all__ = [
    "RAIMemoryGraph",
    "ObservableBehavior", 
    "BehavioralAnalyzer",
    "HumanUnderstandingModule"
]
