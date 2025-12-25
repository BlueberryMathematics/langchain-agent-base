"""Task model for the task manager."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Task:
    """Represents a single task."""
    
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.completed = True
        self.completed_at = datetime.now()
    
    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False
        self.completed_at = None
    
    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create task from dictionary."""
        created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        completed_at = datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None
        
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            created_at=created_at,
            completed_at=completed_at,
        )
