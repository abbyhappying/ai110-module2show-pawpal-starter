from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task, TaskType


def main() -> None:
    owner = Owner(name="Alex", email="alex@example.com")

    luna = Pet(name="Luna", species="Dog", age=3, breed="Labrador")
    max_pet = Pet(name="Max", species="Cat", age=2, breed="Siamese")
    owner.add_pet(luna)
    owner.add_pet(max_pet)

    tasks = [
        Task(name="Evening medication", task_type=TaskType.MEDICATION, priority=3, duration_minutes=10, time_of_day="19:00", frequency="daily", due_date=date.today()),
        Task(name="Morning feeding", task_type=TaskType.FEEDING, priority=2, duration_minutes=15, time_of_day="07:00", frequency="daily", due_date=date.today()),
        Task(name="Noon walk", task_type=TaskType.WALK, priority=1, duration_minutes=30, time_of_day="12:30", frequency="weekly", due_date=date.today()),
        Task(name="Midday check", task_type=TaskType.FEEDING, priority=2, duration_minutes=10, time_of_day="12:30", frequency="daily", due_date=date.today()),
    ]

    for task in tasks:
        if task.name.startswith("Evening"):
            max_pet.add_task(task)
        else:
            luna.add_task(task)

    scheduler = Scheduler()
    for pet in owner.pets:
        for task in pet.tasks:
            scheduler.add_task(task)

    print("Today's Schedule")
    print("-" * 24)
    for task in scheduler.generate_daily_plan():
        pet_name = luna.name if task.pet_id == luna.id else max_pet.name
        print(f"{task.time_of_day} - {pet_name}: {task.name} [{task.task_type.value}]")

    print("\nSorted by time")
    scheduler.sort_by_time()
    for task in scheduler.scheduled_tasks:
        print(f"{task.time_of_day} - {task.name}")

    print("\nTasks for Luna")
    for task in scheduler.filter_by_pet(luna.id):
        print(f"- {task.name}")

    print("\nConflicts")
    conflict_warning = scheduler.get_conflict_warning()
    if conflict_warning:
        print(f"WARNING: {conflict_warning}")
    else:
        print("- No conflicts detected.")

    print("\nRecurring task demo")
    recurring_task = Task(name="Daily meds", task_type=TaskType.MEDICATION, priority=3, duration_minutes=5, time_of_day="08:00", frequency="daily", due_date=date.today())
    luna.add_task(recurring_task)
    scheduler.add_task(recurring_task)
    next_task = recurring_task.mark_complete()
    if next_task is not None:
        print(f"Next occurrence due: {next_task.due_date}")


if __name__ == "__main__":
    main()
