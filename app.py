import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task, TaskType

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.write("Plan your pet care tasks with simple scheduling rules based on time and priority.")

if "owner" not in st.session_state or st.session_state.owner is None:
    st.session_state.owner = Owner(name="Jordan", email="jordan@example.com")

if "scheduler" not in st.session_state or st.session_state.scheduler is None:
    st.session_state.scheduler = Scheduler()

if "selected_pet_id" not in st.session_state:
    st.session_state.selected_pet_id = None

owner = st.session_state.owner
scheduler = st.session_state.scheduler

with st.sidebar:
    st.header("Owner details")
    owner_name = st.text_input("Owner name", value=owner.name)
    owner_email = st.text_input("Owner email", value=owner.email)

    if st.button("Save owner"):
        owner.name = owner_name
        owner.email = owner_email
        st.success("Owner saved.")
        st.rerun()

    st.header("Add a pet")
    with st.form("pet_form"):
        pet_name = st.text_input("Pet name", value="Mochi")
        species = st.selectbox("Species", ["dog", "cat", "other"], index=0)
        age = st.number_input("Age", min_value=0, max_value=30, value=2)
        breed = st.text_input("Breed", value="Mixed")
        submitted = st.form_submit_button("Add pet")

        if submitted:
            pet = Pet(name=pet_name, species=species, age=int(age), breed=breed)
            owner.add_pet(pet)
            st.session_state.selected_pet_id = pet.id
            st.success(f"Added {pet.name} to your pet list.")
            st.rerun()

    st.header("Schedule constraints")
    available_minutes = st.number_input("Available minutes today", min_value=30, max_value=480, value=180)
    preference = st.selectbox("Priority style", ["time", "priority"], index=0)

st.subheader("Current pets")
if owner.pets:
    pet_ids = [pet.id for pet in owner.pets]
    if st.session_state.selected_pet_id not in pet_ids:
        st.session_state.selected_pet_id = pet_ids[0]

    selected_pet_id = st.selectbox(
        "Choose a pet",
        options=pet_ids,
        format_func=lambda pet_id: owner.get_pet(pet_id).name,
        index=pet_ids.index(st.session_state.selected_pet_id),
    )
    st.session_state.selected_pet_id = selected_pet_id
    selected_pet = owner.get_pet(selected_pet_id)
    st.write(f"Selected pet: {selected_pet.name} ({selected_pet.species})")
else:
    st.info("No pets yet. Add one from the sidebar.")
    selected_pet = None

st.divider()

st.subheader("Schedule a task")
if selected_pet is not None:
    with st.form("task_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.slider("Priority", min_value=1, max_value=5, value=3)

        time_of_day = st.text_input("Suggested time", value="08:00")
        task_type = st.selectbox("Task type", [task_type.value for task_type in TaskType], index=0)
        submitted_task = st.form_submit_button("Schedule task")

        if submitted_task:
            task = Task(
                name=task_title,
                task_type=TaskType(task_type),
                priority=int(priority),
                duration_minutes=int(duration),
                time_of_day=time_of_day,
                frequency="daily",
            )
            selected_pet.add_task(task)
            scheduler.add_task(task)
            st.success(f"Scheduled {task.name} for {selected_pet.name}.")
            st.rerun()

    if selected_pet.tasks:
        pet_tasks = sorted(selected_pet.tasks, key=lambda task: task.time_of_day or "00:00")
        st.write("Tasks for this pet")
        st.table(
            [
                {
                    "title": task.name,
                    "time": task.time_of_day,
                    "priority": task.priority,
                    "duration": task.duration_minutes,
                    "type": task.task_type.value,
                }
                for task in pet_tasks
            ]
        )

        conflict_warning = scheduler.get_conflict_warning()
        if conflict_warning:
            st.warning(conflict_warning)
    else:
        st.info("No tasks scheduled yet for this pet.")
else:
    st.info("Add a pet before scheduling tasks.")

st.divider()

st.subheader("Generate schedule")
if st.button("Generate schedule"):
    if not scheduler.scheduled_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        pet_tasks = [task for task in scheduler.scheduled_tasks if task.pet_id == selected_pet.id] if selected_pet is not None else scheduler.scheduled_tasks
        plan = sorted(
            pet_tasks,
            key=lambda task: (task.time_of_day or "00:00", -task.priority),
        )
        st.success(f"Created a plan with {len(plan)} task(s) for {selected_pet.name if selected_pet else 'all pets'}.")

        for task in plan:
            pet_name = selected_pet.name if selected_pet is not None else owner.get_pet(task.pet_id).name if task.pet_id else "Unknown pet"
            st.write(f"{task.time_of_day or 'unscheduled'} — {pet_name}: {task.name} ({task.task_type.value})")

        skipped = [task.name for task in pet_tasks if task not in plan]
        if skipped:
            st.caption(f"Skipped due to time limits: {', '.join(skipped)}")

        st.info(
            "Reasoning: tasks are sorted by time and shown for the selected pet when available."
        )
