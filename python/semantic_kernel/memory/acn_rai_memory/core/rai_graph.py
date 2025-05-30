"""
Core RAI Graph Implementation
Provides the main graph-based memory structure for agent memory management
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import uuid

@dataclass
class MemoryNode:
    """Represents a node in the RAI memory graph"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = ""  # learning, newData, update, action, observation, decision
    label: str = ""
    content: Any = None
    status: str = "active"  # active, evolving, stable, pending
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Initialize default metadata if not provided"""
        if not self.metadata:
            self.metadata = {
                "confidence": 0.5,
                "contextual_score": 0.5,
                "evolution_stage": 0,
                "iterations": 0,
                "creation_cycle": 0,
                "last_evolution_cycle": 0
            }

@dataclass 
class MemoryRelationship:
    """Represents a relationship between memory nodes"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str = ""
    target_id: str = ""
    type: str = ""  # translates, reinforces, adapts, extends, contradicts
    weight: float = 0.5
    confidence: float = 0.5
    label: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

class RAIMemoryGraph:
    """
    Core RAI Memory Graph implementation
    Manages the dynamic neural graph structure for agent memory
    """
    
    def __init__(self):
        self.nodes: Dict[str, MemoryNode] = {}
        self.relationships: Dict[str, MemoryRelationship] = {}
        self.learning_cycle_count = 0
        self._event_subscribers = []
        
    async def create_memory_node(
        self,
        node_type: str,
        label: str,
        content: Any,
        status: str = "active",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new memory node"""
        node = MemoryNode(
            type=node_type,
            label=label,
            content=content,
            status=status,
            metadata=metadata or {}
        )
        
        self.nodes[node.id] = node
        await self._notify_subscribers("create", node)
        return node.id
        
    async def update_memory_node(self, node_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing memory node"""
        if node_id not in self.nodes:
            return False
            
        node = self.nodes[node_id]
        
        for key, value in updates.items():
            if hasattr(node, key):
                setattr(node, key, value)
                
        node.updated_at = datetime.now()
        await self._notify_subscribers("update", node)
        return True
        
    async def create_relationship(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        weight: float = 0.5,
        confidence: float = 0.5,
        label: str = ""
    ) -> Optional[str]:
        """Create a relationship between nodes"""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None
            
        relationship = MemoryRelationship(
            source_id=source_id,
            target_id=target_id,
            type=rel_type,
            weight=weight,
            confidence=confidence,
            label=label
        )
        
        self.relationships[relationship.id] = relationship
        return relationship.id
        
    def get_memory_by_type(self, node_type: str) -> List[MemoryNode]:
        """Get all memory nodes of a specific type"""
        return [node for node in self.nodes.values() if node.type == node_type]
        
    def get_memory_by_id(self, node_id: str) -> Optional[MemoryNode]:
        """Get a specific memory node by ID"""
        return self.nodes.get(node_id)
        
    def get_all_memory(self) -> List[MemoryNode]:
        """Get all memory nodes"""
        return list(self.nodes.values())
        
    def get_all_relationships(self) -> List[MemoryRelationship]:
        """Get all relationships"""
        return list(self.relationships.values())
        
    async def run_learning_cycle(self):
        """Execute a learning cycle to evolve memory"""
        self.learning_cycle_count += 1
        
        # Knowledge Evolution
        await self._evolve_knowledge()
        
        # Relationship Refinement  
        await self._refine_relationships()
        
        # Consensus Mechanism
        await self._consensus_mechanism()
        
        # Notify subscribers
        for node in self.nodes.values():
            await self._notify_subscribers("evolve", node)
    
    async def _evolve_knowledge(self):
        """Update learning nodes with increased confidence"""
        for node in self.get_memory_by_type("learning"):
            if node.metadata.get("confidence", 0) < 0.95:
                node.metadata["confidence"] = min(0.95, node.metadata["confidence"] + 0.05)
                node.metadata["evolution_stage"] = node.metadata.get("evolution_stage", 0) + 1
                node.metadata["last_evolution_cycle"] = self.learning_cycle_count
                
    async def _refine_relationships(self):
        """Update relationship weights and confidence"""
        for rel in self.relationships.values():
            # Strengthen frequently used relationships
            if rel.weight < 0.9:
                rel.weight = min(0.9, rel.weight + 0.02)
                
    async def _consensus_mechanism(self):
        """Consolidate similar concepts when confidence is high"""
        # Implementation for consensus mechanism would go here
        pass
        
    def subscribe(self, callback):
        """Subscribe to memory events"""
        self._event_subscribers.append(callback)
        
        def unsubscribe():
            if callback in self._event_subscribers:
                self._event_subscribers.remove(callback)
        
        return unsubscribe
        
    async def _notify_subscribers(self, event: str, record: MemoryNode):
        """Notify all subscribers of memory events"""
        for callback in self._event_subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event, record)
                else:
                    callback(event, record)
            except Exception as e:
                print(f"Error notifying subscriber: {e}")
