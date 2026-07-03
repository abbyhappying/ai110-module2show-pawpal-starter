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
