
import heapq
from datetime import datetime

class Task:
    def __init__(self, description, priority, dependencies, assignee=None):
        self.description = description
        self.priority = priority
        self.dependencies = dependencies  # List of task descriptions that this task depends on
        self.assignee = assignee  # Person assigned to the task
        self.completed = False
        self.start_date = None
        self.end_date = None

    def __lt__(self, other):
        return self.priority < other.priority

    def start(self):
        self.start_date = datetime.now()

    def end(self):
        self.completed = True
        self.end_date = datetime.now()

class ProjectManager:
    def __init__(self):
        self.tasks = []
        self.completed_tasks = []
        self.resource_pool = {}  # Dictionary to hold resources and their assigned tasks

    def add_task(self, task):
        heapq.heappush(self.tasks, task)

    def complete_task(self, task):
        print(f"Completing task: {task.description}")
        task.end()
        self.completed_tasks.append(task)
        self.tasks.remove(task)
        heapq.heapify(self.tasks)
        if task.assignee in self.resource_pool:
            self.resource_pool[task.assignee].remove(task.description)

    def get_next_task(self):
        for task in self.tasks:
            if all(dep in [t.description for t in self.completed_tasks] for dep in task.dependencies):
                return task
        return None

    def assign_task(self, task, assignee):
        task.assignee = assignee
        if assignee not in self.resource_pool:
            self.resource_pool[assignee] = []
        self.resource_pool[assignee].append(task.description)
        task.start()

    def update_task_priority(self, task_description, new_priority):
        for task in self.tasks:
            if task.description == task_description:
                task.priority = new_priority
                break
        heapq.heapify(self.tasks)

    def task_status_report(self):
        print("Task Status Report:")
        for task in self.tasks + self.completed_tasks:
            status = "Completed" if task.completed else "In Progress"
            print(f"{task.description}: {status}, Assigned to: {task.assignee}, Start Date: {task.start_date}, End Date: {task.end_date}")

# Example usage
project_manager = ProjectManager()
project_manager.add_task(Task("Implement NLP module", 1, []))
project_manager.add_task(Task("Write unit tests", 2, ["Implement NLP module"]))
project_manager.add_task(Task("Create project documentation", 3, ["Write unit tests"]))

# Assign tasks
project_manager.assign_task(project_manager.get_next_task(), "Alice")
project_manager.assign_task(project_manager.get_next_task(), "Bob")

# Complete a task and update priorities as needed
next_task = project_manager.get_next_task()
if next_task:
    project_manager.complete_task(next_task)
    project_manager.update_task_priority("Create project documentation", 1)

# Print out a status report
project_manager.task_status_report()
