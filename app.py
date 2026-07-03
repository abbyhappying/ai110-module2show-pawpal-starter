import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task, TaskType

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.write("Plan your pet care tasks with simple scheduling rules based on time and priority.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

with st.sidebar:
    st.header("Owner details")
    owner_name = st.text_input("Owner name", value="Jordan")
    owner_email = st.text_input("Owner email", value="jordan@example.com")

    st.header("Pet details")
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"], index=0)
    age = st.number_input("Age", min_value=0, max_value=30, value=2)
    breed = st.text_input("Breed", value="Mixed")

    st.header("Schedule constraints")
    available_minutes = st.number_input("Available minutes today", min_value=30, max_value=480, value=180)
    preference = st.selectbox("Priority style", ["time", "priority"], index=0)

st.subheader("Add or edit tasks")
st.caption("Each task should include a duration and priority so the scheduler can make a plan.")

if st.session_state.tasks:
    selected_task_index = st.selectbox(
        "Edit an existing task",
        options=range(len(st.session_state.tasks)),
        format_func=lambda i: st.session_state.tasks[i]["title"],
    )
else:
    selected_task_index = None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.slider("Priority", min_value=1, max_value=5, value=3)

time_of_day = st.text_input("Suggested time", value="08:00")
task_type = st.selectbox("Task type", [task_type.value for task_type in TaskType], index=0)

if st.button("Add task"):
    st.session_state.tasks.append(
        {
            "title": task_title,
            "duration_minutes": int(duration),
            "priority": int(priority),
            "time_of_day": time_of_day,
            "task_type": task_type,
        }
    )
    st.success(f"Added {task_title}.")

if st.session_state.tasks and selected_task_index is not None:
    st.write("Selected task")
    task_to_edit = st.session_state.tasks[selected_task_index]
    task_to_edit["title"] = st.text_input("Edit title", value=task_to_edit["title"])
    task_to_edit["duration_minutes"] = int(
        st.number_input("Edit duration", min_value=1, max_value=240, value=task_to_edit["duration_minutes"])
    )
    task_to_edit["priority"] = int(
        st.slider("Edit priority", min_value=1, max_value=5, value=task_to_edit["priority"])
    )
    task_to_edit["time_of_day"] = st.text_input("Edit time", value=task_to_edit["time_of_day"])
    task_to_edit["task_type"] = st.selectbox(
        "Edit task type",
        [task_type.value for task_type in TaskType],
        index=[task_type.value for task_type in TaskType].index(task_to_edit["task_type"]),
    )

    if st.button("Remove selected task"):
        st.session_state.tasks.pop(selected_task_index)
        st.rerun()

if st.session_state.tasks:
    st.write("Current tasks")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Generate schedule")
if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        owner = Owner(name=owner_name, email=owner_email)
        pet = Pet(name=pet_name, species=species, age=int(age), breed=breed)
        owner.add_pet(pet)

        for task_data in st.session_state.tasks:
            task = Task(
                name=task_data["title"],
                task_type=TaskType(task_data["task_type"]),
                priority=task_data["priority"],
                duration_minutes=task_data["duration_minutes"],
                time_of_day=task_data["time_of_day"],
                frequency="daily",
            )
            pet.add_task(task)

        scheduler = Scheduler()
        for task in pet.tasks:
            scheduler.add_task(task)

        plan = scheduler.generate_daily_plan(total_minutes=int(available_minutes), preference=preference)
        st.success(f"Created a plan for {pet.name} with {len(plan)} task(s).")

        for task in plan:
            st.write(f"{task.time_of_day or 'unscheduled'} — {task.name} ({task.task_type.value})")

        skipped = [task.name for task in pet.tasks if task not in plan]
        if skipped:
            st.caption(f"Skipped due to time limits: {', '.join(skipped)}")

        st.info(
            "Reasoning: tasks are arranged by the selected preference and only the ones that fit into the available time are included."
        )
