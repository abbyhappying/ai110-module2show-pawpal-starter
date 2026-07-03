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
