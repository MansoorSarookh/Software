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
    name = st.text_input("Project Name")
    description = st.text_area("Project Description")
    start_date = st.date_input("Start Date", date.today())
    end_date = st.date_input("End Date")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    budget = st.number_input("Budget", min_value=0.0)
    tags = st.text_input("Tags (comma-separated)")
    
    if st.button("Create Project"):
        if name and description:
            new_project = pd.DataFrame({
                "Project Name": [name],
                "Description": [description],
                "Start Date": [start_date],
                "End Date": [end_date],
                "Priority": [priority],
                "Status": ["Uncompleted"],
                "Progress": [0],
                "Budget": [budget],
                "Tags": [tags]
            })
            df = load_projects()
            df = pd.concat([df, new_project], ignore_index=True)
            save_projects(df)
            st.success(f"Project '{name}' has been added!")
        else:
            st.error("Please fill in all fields")

# Other functions such as edit_project, delete_project, manage_tasks, view_high_priority, manage_team...

# Sidebar with functional buttons and custom colors
st.sidebar.markdown("<h3>Menu</h3>", unsafe_allow_html=True)

# Set the selected option based on button clicks
selected_option = None

# Define a helper to create colored buttons in sidebar
def colored_button(label, color):
    return st.sidebar.markdown(
        f"""
        <style>
            .button {{
                background-color: {color};
                color: white;
                padding: 8px;
                border-radius: 5px;
                width: 100%;
                text-align: center;
                margin: 2px 0;
                cursor: pointer;
                font-weight: bold;
            }}
            .button:hover {{
                opacity: 0.9;
            }}
        </style>
        <div class="button" onclick="window.location.href='#{label.replace(' ', '').lower()}'">{label}</div>
        """,
        unsafe_allow_html=True
    )

# Display sidebar buttons
if st.sidebar.button("Add Project"):
    selected_option = "Add Project"
elif st.sidebar.button("Edit Project"):
    selected_option = "Edit Project"
elif st.sidebar.button("Delete Project"):
    selected_option = "Delete Project"
elif st.sidebar.button("Task Management"):
    selected_option = "Task Management"
elif st.sidebar.button("High Priority & Deadlines"):
    selected_option = "High Priority & Deadlines"
elif st.sidebar.button("Team Management"):
    selected_option = "Team Management"

# Execute the selected function
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
