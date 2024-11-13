# time_management_app.py
import streamlit as st
import pandas as pd
import datetime

# App Title
st.title("Time Management App")
st.subheader("Developed by Mansoor Sarookh")

# Sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Today's Tasks", "Calendar", "Analytics", "Goals"])

# Placeholder Data
tasks_data = pd.DataFrame({
    "Task": ["Meeting", "Coding Session", "Review Project"],
    "Time": ["10:00 AM", "1:00 PM", "3:00 PM"]
})

# Today's Tasks Section
if selection == "Today's Tasks":
    st.header("Today's Tasks")
    st.table(tasks_data)
    
    # Focus Timer Section
    st.subheader("Focus Timer")
    if st.button("Start Focus Session"):
        st.write("Focus session started...")

# Placeholder for Analytics and Goals sections
elif selection == "Analytics":
    st.header("Productivity Insights")
    st.write("Analytics coming soon...")
    
elif selection == "Goals":
    st.header("Goals")
    st.write("Goals section coming soon...")
# Add task input in 'Today's Tasks' section
if selection == "Today's Tasks":
    st.header("Today's Tasks")
    
    # Input form for new tasks
    with st.form("task_form"):
        task_name = st.text_input("Task Name")
        task_time = st.time_input("Time")
        submit_task = st.form_submit_button("Add Task")
        
    # Append new tasks
    if submit_task:
        new_task = pd.DataFrame({"Task": [task_name], "Time": [task_time.strftime("%I:%M %p")]})
        tasks_data = pd.concat([tasks_data, new_task], ignore_index=True)
        st.success(f"Task '{task_name}' added for {task_time.strftime('%I:%M %p')}")
        
    st.table(tasks_data)
import time

# Focus Timer Section
if selection == "Today's Tasks":
    st.subheader("Focus Timer")
    
    # Customizable session duration
    focus_duration = st.slider("Set Focus Duration (minutes)", min_value=5, max_value=60, step=5)
    if st.button("Start Focus Session"):
        st.write(f"Focus session started for {focus_duration} minutes...")
        with st.spinner("Focusing..."):
            time.sleep(focus_duration * 60)  # Replace with actual countdown timer functionality
        st.success("Focus session completed!")
import matplotlib.pyplot as plt

# Analytics section
elif selection == "Analytics":
    st.header("Productivity Insights")
    
    # Dummy data for demonstration
    productivity_data = {"Category": ["Work", "Study", "Exercise", "Leisure"], "Hours": [20, 15, 5, 10]}
    df_productivity = pd.DataFrame(productivity_data)
    
    # Bar chart for productivity
    fig, ax = plt.subplots()
    ax.bar(df_productivity["Category"], df_productivity["Hours"], color='skyblue')
    ax.set_title("Weekly Productivity Breakdown")
    st.pyplot(fig)
# AI Suggestions (Simplified example)
def get_suggestions():
    return "Try focusing on high-priority tasks in the morning when you're most productive."

# Display suggestions in the Analytics section
if selection == "Analytics":
    st.subheader("AI Suggestions")
    st.write(get_suggestions())
# Placeholder function for peak productivity (e.g., based on mock data)
st.subheader("Peak Productivity Hours")
peak_hours = [9, 10, 11, 14, 15]
st.write(f"Your peak productivity hours: {', '.join([str(hour) + ':00' for hour in peak_hours])}")