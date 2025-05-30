"""
Observable Memory Component
Tracks and monitors agent behavior for transparency and analysis
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import asyncio

@dataclass
class BehaviorMarker:
    """Represents an observable behavior marker"""
    timestamp: datetime = field(default_factory=datetime.now)
    behavior_type: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DecisionContext:
    """Captures the context of an agent decision"""
    decision_id: str = ""
    input_context: Dict[str, Any] = field(default_factory=dict)
    processing_steps: List[str] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class ObservableBehavior:
    """
    Observable Behavior tracking system
    Monitors and records agent behavior patterns for analysis
    """
    
    def __init__(self):
        self.behavior_history: List[BehaviorMarker] = []
        self.decision_contexts: List[DecisionContext] = []
        self._observers = []
        
    async def capture_context(self, messages: Any) -> DecisionContext:
        """Capture the context for a decision"""
        context = DecisionContext(
            decision_id=str(len(self.decision_contexts)),
            input_context={"messages": str(messages)},
            processing_steps=[],
            confidence_scores={}
        )
        
        self.decision_contexts.append(context)
        return context
        
    def extract_behavior_markers(self, response: Any) -> List[BehaviorMarker]:
        """Extract behavior markers from agent response"""
        markers = []
        
        # Example behavior extraction logic
        if hasattr(response, 'content'):
            marker = BehaviorMarker(
                behavior_type="response_generation",
                context={"response_length": len(str(response.content))},
                confidence=0.8
            )
            markers.append(marker)
            
        return markers
        
    async def record_behavior(self, markers: List[BehaviorMarker]):
        """Record behavior markers"""
        self.behavior_history.extend(markers)
        
        # Notify observers
        for observer in self._observers:
            try:
                if asyncio.iscoroutinefunction(observer):
                    await observer("behavior_recorded", markers)
                else:
                    observer("behavior_recorded", markers)
            except Exception as e:
                print(f"Error notifying behavior observer: {e}")
                
    def get_behavior_patterns(self, 
                            behavior_type: Optional[str] = None,
                            time_window: Optional[int] = None) -> List[BehaviorMarker]:
        """Get behavior patterns with optional filtering"""
        patterns = self.behavior_history
        
        if behavior_type:
            patterns = [p for p in patterns if p.behavior_type == behavior_type]
            
        if time_window:
            cutoff = datetime.now().timestamp() - time_window
            patterns = [p for p in patterns if p.timestamp.timestamp() > cutoff]
            
        return patterns
        
    def add_observer(self, observer):
        """Add a behavior observer"""
        self._observers.append(observer)
        
    def remove_observer(self, observer):
        """Remove a behavior observer"""
        if observer in self._observers:
            self._observers.remove(observer)
