"""Storage backend for task persistence."""

import json
from pathlib import Path
from typing import List
from .task import Task


class Storage:
    """Handles task persistence using JSON."""
    
    def __init__(self, filepath: str = "tasks.json"):
        """
        Initialize storage.
        
        Args:
            filepath: Path to JSON file for storage
        """
        self.filepath = Path(filepath)
    
    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Save tasks to file.
        
        Args:
            tasks: List of tasks to save
        """
        data = [task.to_dict() for task in tasks]
        self.filepath.write_text(json.dumps(data, indent=2), encoding='utf-8')
    
    def load_tasks(self) -> List[Task]:
        """
        Load tasks from file.
        
        Returns:
            List of tasks
        """
        if not self.filepath.exists():
            return []
        
        try:
            data = json.loads(self.filepath.read_text(encoding='utf-8'))
            return [Task.from_dict(task_data) for task_data in data]
        except (json.JSONDecodeError, KeyError):
            return []
