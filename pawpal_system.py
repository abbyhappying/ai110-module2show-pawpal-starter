# models.py
from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Optional
import uuid

class TaskType(Enum):
    FEEDING = "feeding"
    WALK = "walk"
    MEDICATION = "medication"

class Task:
    def __init__(self,
                 id: Optional[str] = None,
                 name: str = "",
                 task_type: TaskType = TaskType.FEEDING,
                 priority: int = 1,
                 duration_minutes: int = 15,
                 completed: bool = False,
                 pet_id: Optional[str] = None,
                 time_of_day: Optional[str] = None,
                 frequency: str = "daily",
                 due_date: Optional[date] = None):
        self.id = id if id is not None else str(uuid.uuid4())[:8]
        self.name = name
        self.task_type = task_type
        self.priority = priority
        self.duration_minutes = duration_minutes
        self.completed = completed
        self.pet_id = pet_id
        self.time_of_day = time_of_day or ""
        self.frequency = frequency
        self.due_date = due_date or date.today()

    def mark_complete(self) -> None:
        """Mark this task as complete and create the next occurrence if recurring."""
        self.completed = True

        if self.frequency.lower() == "daily":
            self.due_date = date.today() + timedelta(days=1)
            return Task(
                name=self.name,
                task_type=self.task_type,
                priority=self.priority,
                duration_minutes=self.duration_minutes,
                completed=False,
                pet_id=self.pet_id,
                time_of_day=self.time_of_day,
                frequency=self.frequency,
                due_date=self.due_date,
            )

        if self.frequency.lower() == "weekly":
            self.due_date = date.today() + timedelta(days=7)
            return Task(
                name=self.name,
                task_type=self.task_type,
                priority=self.priority,
                duration_minutes=self.duration_minutes,
                completed=False,
                pet_id=self.pet_id,
                time_of_day=self.time_of_day,
                frequency=self.frequency,
                due_date=self.due_date,
            )

        return None

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete"""
        self.completed = False

    def get_priority_score(self) -> float:
        """Calculate priority score based on priority level and other factors"""
        return (self.priority * 10) + (self.duration_minutes / 15)

    def as_feeding_task(self, food_type: str, amount: float) -> None:
        """Configure task as a feeding task with specific parameters"""
        self.task_type = TaskType.FEEDING
        self.name = f"{self.name} ({food_type}: {amount} cups)"

    def as_walk_task(self, distance_km: float, location: str) -> None:
        """Configure task as a walk task with specific parameters"""
        self.task_type = TaskType.WALK
        self.name = f"{self.name} ({distance_km} km at {location})"

    def as_medication_task(self, medication_name: str, dosage: str) -> None:
        """Configure task as a medication task with specific parameters"""
        self.task_type = TaskType.MEDICATION
        self.name = f"{self.name} ({medication_name}: {dosage})"

class Pet:
    def __init__(self,
                 id: Optional[str] = None,
                 name: str = "",
                 species: str = "",
                 age: int = 0,
                 breed: str = ""):
        self.id = id if id is not None else str(uuid.uuid4())[:8]
        self.name = name
        self.species = species
        self.age = age
        self.breed = breed
        self.tasks: List[Task] = []  # Tasks belong to this pet

    def add_task(self, task: Task) -> None:
        """Assign a task to this pet"""
        task.pet_id = self.id
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from this pet by ID"""
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def get_active_tasks(self) -> List[Task]:
        """Get all tasks that are not completed"""
        return [task for task in self.tasks if not task.completed]

class Owner:
    def __init__(self,
                 id: Optional[str] = None,
                 name: str = "",
                 email: str = ""):
        self.id = id if id is not None else str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.pets: List[Pet] = []  # Owner's collection of pets

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection"""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet by ID"""
        self.pets = [pet for pet in self.pets if pet.id != pet_id]

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """Get a pet by ID"""
        for pet in self.pets:
            if pet.id == pet_id:
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return all active tasks from all pets owned by this person"""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_active_tasks())
        return tasks

class Scheduler:
    def __init__(self):
        self.scheduled_tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule"""
        if task not in self.scheduled_tasks:
            self.scheduled_tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the schedule by ID"""
        self.scheduled_tasks = [task for task in self.scheduled_tasks if task.id != task_id]

    def get_tasks_by_pet(self, pet_id: str) -> List[Task]:
        """Get all tasks belonging to a specific pet"""
        return [task for task in self.scheduled_tasks if task.pet_id == pet_id]

    def generate_daily_plan(self, total_minutes: Optional[int] = None, preference: str = "time") -> List[Task]:
        """Generate a daily plan by sorting and filtering tasks."""
        active_tasks = [task for task in self.scheduled_tasks if not task.completed]
        preference = (preference or "time").lower()

        if preference == "priority":
            active_tasks.sort(key=lambda task: (-task.priority, task.time_of_day or ""))
        else:
            active_tasks.sort(key=lambda task: (task.time_of_day or "", -task.priority))

        if total_minutes is None:
            return active_tasks

        planned_tasks: List[Task] = []
        used_minutes = 0
        for task in active_tasks:
            if used_minutes + task.duration_minutes <= total_minutes:
                planned_tasks.append(task)
                used_minutes += task.duration_minutes
        return planned_tasks

    def sort_by_priority(self) -> None:
        """Sort tasks by priority (highest first)"""
        self.scheduled_tasks.sort(key=lambda task: task.priority, reverse=True)

    def sort_by_time(self) -> None:
        """Sort tasks by their time attribute using a HH:MM-compatible key."""
        self.scheduled_tasks.sort(key=lambda task: task.time_of_day or "00:00")

    def filter_by_pet(self, pet_id: str) -> List[Task]:
        """Return tasks belonging to a specific pet."""
        return [task for task in self.scheduled_tasks if task.pet_id == pet_id]

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return tasks matching the requested completion status."""
        return [task for task in self.scheduled_tasks if task.completed is completed]

    def detect_conflicts(self) -> List[tuple[Task, Task]]:
        """Detect tasks that share the same time slot."""
        conflicts: List[tuple[Task, Task]] = []
        seen = set()
        for index, task in enumerate(self.scheduled_tasks):
            for other in self.scheduled_tasks[index + 1:]:
                if task.time_of_day and task.time_of_day == other.time_of_day:
                    pair = tuple(sorted((task.id, other.id)))
                    if pair not in seen:
                        seen.add(pair)
                        conflicts.append((task, other))
        return conflicts

    def get_conflict_warning(self) -> Optional[str]:
        """Return a lightweight warning message if tasks overlap in time."""
        conflicts = self.detect_conflicts()
        if not conflicts:
            return None

        first, second = conflicts[0]
        return f"Warning: {first.name} and {second.name} both happen at {first.time_of_day}."

    def filter_by_available_time(self, total_minutes: int) -> List[Task]:
        """Filter tasks to fit within available time"""
        planned_tasks: List[Task] = []
        used_minutes = 0
        for task in self.scheduled_tasks:
            if used_minutes + task.duration_minutes <= total_minutes:
                planned_tasks.append(task)
                used_minutes += task.duration_minutes
        return planned_tasks
