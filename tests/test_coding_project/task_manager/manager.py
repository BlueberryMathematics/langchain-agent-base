"""Task manager for CRUD operations."""

from typing import List, Optional
from .task import Task
from .storage import Storage


class TaskManager:
    """Manages tasks with CRUD operations."""
    
    def __init__(self, storage: Storage):
        """
        Initialize task manager.
        
        Args:
            storage: Storage backend for persistence
        """
        self.storage = storage
        self.tasks: List[Task] = self.storage.load_tasks()
        self.next_id = max([task.id for task in self.tasks], default=0) + 1
    
    def create_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task.
        
        Args:
            title: Task title
            description: Task description
        
        Returns:
            The created task
        """
        task = Task(id=self.next_id, title=title, description=description)
        self.tasks.append(task)
        self.next_id += 1
        self.storage.save_tasks(self.tasks)
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: Task ID
        
        Returns:
            Task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def list_tasks(self, show_completed: bool = True) -> List[Task]:
        """
        List all tasks.
        
        Args:
            show_completed: Include completed tasks
        
        Returns:
            List of tasks
        """
        if show_completed:
            return self.tasks.copy()
        return [task for task in self.tasks if not task.completed]
    
    def update_task(self, task_id: int, title: Optional[str] = None, 
                    description: Optional[str] = None) -> bool:
        """
        Update a task.
        
        Args:
            task_id: Task ID
            title: New title (optional)
            description: New description (optional)
        
        Returns:
            True if updated, False if not found
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        
        self.storage.save_tasks(self.tasks)
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: Task ID
        
        Returns:
            True if deleted, False if not found
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self.storage.save_tasks(self.tasks)
        return True
    
    def complete_task(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: Task ID
        
        Returns:
            True if completed, False if not found
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        task.mark_completed()
        self.storage.save_tasks(self.tasks)
        return True
