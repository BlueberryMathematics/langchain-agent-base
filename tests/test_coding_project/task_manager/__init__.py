"""Task Manager - A simple CLI task management system."""

from .task import Task
from .manager import TaskManager
from .storage import Storage

__version__ = "1.0.0"
__all__ = ["Task", "TaskManager", "Storage"]
