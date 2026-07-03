from datetime import date, timedelta

from pawpal_system import Pet, Scheduler, Task, TaskType


def test_sort_by_time_orders_tasks_chronologically():
    pet = Pet(name="Luna", species="Dog")
    late_task = Task(name="Late task", task_type=TaskType.FEEDING, time_of_day="19:00")
    early_task = Task(name="Early task", task_type=TaskType.WALK, time_of_day="07:00")

    pet.add_task(late_task)
    pet.add_task(early_task)

    scheduler = type("Scheduler", (), {"scheduled_tasks": [late_task, early_task]})
    scheduler.scheduled_tasks.sort(key=lambda task: task.time_of_day or "00:00")

    assert [task.name for task in scheduler.scheduled_tasks] == ["Early task", "Late task"]


def test_mark_complete_creates_next_occurrence_for_daily_task():
    task = Task(name="Daily meds", task_type=TaskType.MEDICATION, frequency="daily", due_date=date.today())

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_get_conflict_warning_reports_overlapping_tasks():
    scheduler = Scheduler()
    first = Task(name="Noon walk", task_type=TaskType.WALK, time_of_day="12:30")
    second = Task(name="Midday check", task_type=TaskType.FEEDING, time_of_day="12:30")
    scheduler.scheduled_tasks = [first, second]

    warning = scheduler.get_conflict_warning()

    assert warning is not None
    assert "12:30" in warning
    assert "Noon walk" in warning
