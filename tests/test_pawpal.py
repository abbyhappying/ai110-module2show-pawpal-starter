from pawpal_system import Pet, Task, TaskType


def test_task_completion_marks_task_complete():
    task = Task(name="Feed Luna", task_type=TaskType.FEEDING, priority=2)

    task.mark_complete()

    assert task.completed is True


def test_adding_task_to_pet_increases_task_count():
    pet = Pet(name="Luna", species="Dog", age=3, breed="Labrador")
    task = Task(name="Morning walk", task_type=TaskType.WALK, priority=3)

    pet.add_task(task)

    assert len(pet.tasks) == 1


from pawpal_system import Scheduler, Task, TaskType


def test_generate_daily_plan_prioritizes_high_priority_tasks():
    scheduler = Scheduler()

    low_priority = Task(name="Low priority task", task_type=TaskType.FEEDING, priority=1, duration_minutes=15, time_of_day="09:00")
    high_priority = Task(name="High priority task", task_type=TaskType.WALK, priority=3, duration_minutes=20, time_of_day="08:00")

    scheduler.add_task(low_priority)
    scheduler.add_task(high_priority)

    plan = scheduler.generate_daily_plan()

    assert [task.id for task in plan[:2]] == [high_priority.id, low_priority.id]


def test_generate_daily_plan_respects_available_time_limit():
    scheduler = Scheduler()

    short_task = Task(name="Short task", task_type=TaskType.FEEDING, priority=2, duration_minutes=15, time_of_day="07:00")
    long_task = Task(name="Long task", task_type=TaskType.MEDICATION, priority=2, duration_minutes=30, time_of_day="08:00")

    scheduler.add_task(short_task)
    scheduler.add_task(long_task)

    plan = scheduler.generate_daily_plan(total_minutes=30)

    assert [task.id for task in plan] == [short_task.id]


from datetime import date, timedelta

from pawpal_system import Pet, Scheduler, Task, TaskType


def test_sort_by_time_orders_tasks_chronologically():
    scheduler = Scheduler()
    late_task = Task(name="Late task", task_type=TaskType.FEEDING, time_of_day="19:00")
    early_task = Task(name="Early task", task_type=TaskType.WALK, time_of_day="07:00")
    middle_task = Task(name="Middle task", task_type=TaskType.MEDICATION, time_of_day="12:30")

    scheduler.add_task(late_task)
    scheduler.add_task(early_task)
    scheduler.add_task(middle_task)

    scheduler.sort_by_time()

    assert [task.name for task in scheduler.scheduled_tasks] == [
        "Early task",
        "Middle task",
        "Late task",
    ]


def test_mark_complete_creates_next_occurrence_for_daily_task():
    task = Task(name="Daily meds", task_type=TaskType.MEDICATION, frequency="daily", due_date=date.today())

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.frequency == "daily"
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_get_conflict_warning_reports_overlapping_tasks():
    scheduler = Scheduler()
    first = Task(name="Noon walk", task_type=TaskType.WALK, time_of_day="12:30")
    second = Task(name="Midday check", task_type=TaskType.FEEDING, time_of_day="12:30")
    scheduler.add_task(first)
    scheduler.add_task(second)

    warning = scheduler.get_conflict_warning()

    assert warning is not None
    assert "12:30" in warning
    assert "Noon walk" in warning


def test_empty_scheduler_returns_no_tasks_and_no_conflicts():
    scheduler = Scheduler()

    assert scheduler.scheduled_tasks == []
    assert scheduler.generate_daily_plan() == []
    assert scheduler.get_conflict_warning() is None


def test_filter_by_pet_returns_only_tasks_for_selected_pet():
    scheduler = Scheduler()
    luna = Pet(name="Luna", species="Dog")
    max_pet = Pet(name="Max", species="Cat")

    first_task = Task(name="Morning walk", task_type=TaskType.WALK, time_of_day="08:00")
    second_task = Task(name="Evening meds", task_type=TaskType.MEDICATION, time_of_day="20:00")

    luna.add_task(first_task)
    max_pet.add_task(second_task)

    scheduler.add_task(first_task)
    scheduler.add_task(second_task)

    luna_tasks = scheduler.filter_by_pet(luna.id)

    assert len(luna_tasks) == 1
    assert luna_tasks[0].name == "Morning walk"
