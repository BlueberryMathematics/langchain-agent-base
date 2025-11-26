"""Main entry point for Task Manager CLI."""

from task_manager import TaskManager, Storage


def main():
    """Run the task manager CLI."""
    print("=" * 60)
    print("TASK MANAGER")
    print("=" * 60)
    
    # Initialize
    storage = Storage("tasks.json")
    manager = TaskManager(storage)
    
    # Show existing tasks
    tasks = manager.list_tasks()
    print(f"\nLoaded {len(tasks)} task(s)")
    
    # Demo: Create some tasks
    if not tasks:
        print("\nCreating demo tasks...")
        manager.create_task("Buy groceries", "Milk, eggs, bread")
        manager.create_task("Write report", "Q4 financial report")
        manager.create_task("Call dentist", "Schedule checkup")
    
    # List tasks
    print("\nCurrent Tasks:")
    print("-" * 60)
    for task in manager.list_tasks():
        status = "[X]" if task.completed else "[ ]"
        print(f"{status} [{task.id}] {task.title}")
        if task.description:
            print(f"    {task.description}")
    print("-" * 60)
    
    print("\nTask Manager is ready!")
    print("   - Add tasks with: manager.create_task(title, description)")
    print("   - Complete tasks with: manager.complete_task(task_id)")
    print("   - Delete tasks with: manager.delete_task(task_id)")


if __name__ == "__main__":
    main()
