from pawpal_system import Owner, Pet, Task, TaskType, Scheduler


def main() -> None:
    owner = Owner(name="Alex", email="alex@example.com")

    luna = Pet(name="Luna", species="Dog", age=3, breed="Labrador")
    max_pet = Pet(name="Max", species="Cat", age=2, breed="Siamese")

    owner.add_pet(luna)
    owner.add_pet(max_pet)

    morning_feed = Task(name="Morning feeding", task_type=TaskType.FEEDING, priority=2, duration_minutes=15, time_of_day="07:00", frequency="daily")
    noon_walk = Task(name="Noon walk", task_type=TaskType.WALK, priority=1, duration_minutes=30, time_of_day="12:30", frequency="daily")
    evening_medication = Task(name="Evening medication", task_type=TaskType.MEDICATION, priority=3, duration_minutes=10, time_of_day="19:00", frequency="daily")

    luna.add_task(morning_feed)
    luna.add_task(noon_walk)
    max_pet.add_task(evening_medication)

    scheduler = Scheduler()
    for pet in owner.pets:
        for task in pet.tasks:
            scheduler.add_task(task)

    print("Today's Schedule")
    print("-" * 20)
    for task in scheduler.generate_daily_plan():
        pet_name = luna.name if task.pet_id == luna.id else max_pet.name
        print(f"{task.time_of_day} - {pet_name}: {task.name} [{task.task_type.value}]")


if __name__ == "__main__":
    main()
