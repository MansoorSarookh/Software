# app.py
import streamlit as st
from datetime import datetime, timedelta

# Set up the page configuration
st.set_page_config(page_title="Time Management App", layout="wide")

# Title with your name
st.title("Time Management Tool Developed by Mansoor Sarookh")

# Sidebar for navigation
st.sidebar.header("Navigation")
sections = ["Today's Tasks", "Calendar", "Analytics", "Goals"]
choice = st.sidebar.radio("Go to", sections)

# Layout based on section choice
if choice == "Today's Tasks":
    st.subheader("Today's Tasks")
    # Placeholder for daily task display
    
elif choice == "Calendar":
    st.subheader("Calendar View")
    # Placeholder for calendar view
    
elif choice == "Analytics":
    st.subheader("Productivity Analytics")
    # Placeholder for productivity analytics
    
elif choice == "Goals":
    st.subheader("Goals and Habits")
    # Placeholder for goal tracking
if choice == "Today's Tasks":
    st.subheader("Today's Task List")

    # Task input form
    task = st.text_input("Add a new task", "")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])

    # Store tasks in a dictionary or external database (for demo purposes, use session state)
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    if st.button("Add Task"):
        st.session_state.tasks.append({"task": task, "priority": priority, "added": datetime.now()})
        st.success(f"Task '{task}' added successfully!")

    # Display tasks
    st.write("### Task List")
    for i, t in enumerate(st.session_state.tasks):
        st.write(f"**{t['task']}** - Priority: {t['priority']} (added on {t['added'].strftime('%Y-%m-%d %H:%M:%S')})")
if choice == "Calendar":
    st.subheader("Calendar View")

    # Simple date picker
    selected_date = st.date_input("Choose a date", datetime.now())
    st.write(f"Events for {selected_date.strftime('%Y-%m-%d')}:")

    # For a more advanced calendar, consider integrating a library such as `streamlit-calendar` if available
    # (Currently, placeholder content below)
    st.write("No events scheduled for this date.")
if choice == "Today's Tasks":
    st.write("### Focus Timer (Pomodoro)")
    focus_duration = st.slider("Focus Duration (minutes)", 15, 60, 25)
    break_duration = st.slider("Break Duration (minutes)", 5, 15, 5)
    if st.button("Start Focus Session"):
        st.success("Focus session started!")
        # Timer logic here can be added in an actual deployment (or using a JS-based timer in Streamlit)
if choice == "Analytics":
    st.write("### Productivity Insights")
    
    # Placeholder data (replace with actual data for full functionality)
    task_completion_data = {
        "Date": [datetime.now() - timedelta(days=i) for i in range(7)],
        "Tasks Completed": [3, 5, 2, 4, 6, 1, 4]
    }

    # Generate a line chart to show productivity over the past week
    st.line_chart(task_completion_data)
if choice == "Goals":
    st.write("### Goal Tracker")

    goal = st.text_input("Set a new goal", "e.g., 30 minutes reading daily")
    if st.button("Add Goal"):
        st.session_state.goals.append(goal)
        st.success(f"Goal '{goal}' added!")

    st.write("Your Goals:")
    for goal in st.session_state.goals:
        st.write(f"- {goal}")
