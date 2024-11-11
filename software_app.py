import streamlit as st
import pandas as pd
from datetime import date

# File to store project data
PROJECT_DATA_FILE = 'projects.csv'
TASK_DATA_FILE = 'tasks.csv'
TEAM_DATA_FILE = 'team_members.csv'

# Main title in the main body
st.title("Software Management Tool")
st.write("Developed By Mansoor Sarookh, CS Student at GPGC Swabi")

# Load and save functions for projects, tasks, and team members
def load_projects():
    try:
        return pd.read_csv(PROJECT_DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Project Name", "Description", "Start Date", "End Date", "Priority", "Status", "Progress", "Budget", "Tags"])

def save_projects(df):
    df.to_csv(PROJECT_DATA_FILE, index=False)

def load_tasks():
    try:
        return pd.read_csv(TASK_DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Project Name", "Task Name", "Deadline", "Status", "Assigned To"])

def save_tasks(df):
    df.to_csv(TASK_DATA_FILE, index=False)

def load_team():
    try:
        return pd.read_csv(TEAM_DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Project Name", "Member Name", "Role"])

def save_team(df):
    df.to_csv(TEAM_DATA_FILE, index=False)

# Functions for each main feature
def add_project():
    st.header("Add New Project")
    # project addition logic here

def edit_project():
    st.header("Edit Project")
    # project editing logic here

def delete_project():
    st.header("Delete Project")
    # project deletion logic here

def manage_tasks():
    st.header("Task Management")
    # task management logic here

def view_high_priority():
    st.header("Upcoming Deadlines & High Priority Projects")
    # view deadlines and high-priority projects logic here

def manage_team():
    st.header("Team Management")
    # team management logic here

# Sidebar with custom buttons for each functionality
st.sidebar.markdown("<h3>Menu</h3>", unsafe_allow_html=True)

# Custom button styles
button_styles = {
    "Add Project": "background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;",
    "Edit Project": "background-color: #2196F3; color: white; padding: 10px; border-radius: 5px;",
    "Delete Project": "background-color: #f44336; color: white; padding: 10px; border-radius: 5px;",
    "Task Management": "background-color: #FF9800; color: white; padding: 10px; border-radius: 5px;",
    "High Priority & Deadlines": "background-color: #9C27B0; color: white; padding: 10px; border-radius: 5px;",
    "Team Management": "background-color: #3E4551; color: white; padding: 10px; border-radius: 5px;"
}

# Display each button with its custom style
for option, style in button_styles.items():
    if st.sidebar.markdown(f"<button style='{style}'>{option}</button>", unsafe_allow_html=True):
        selected_option = option
        break
else:
    selected_option = "Add Project"  # default

# Execute the corresponding function based on the selected option
if selected_option == "Add Project":
    add_project()
elif selected_option == "Edit Project":
    edit_project()
elif selected_option == "Delete Project":
    delete_project()
elif selected_option == "Task Management":
    manage_tasks()
elif selected_option == "High Priority & Deadlines":
    view_high_priority()
elif selected_option == "Team Management":
    manage_team()
