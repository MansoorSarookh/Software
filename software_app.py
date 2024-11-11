import streamlit as st
import pandas as pd
from datetime import date

# File paths for data storage
PROJECT_DATA_FILE = 'projects.csv'
TASK_DATA_FILE = 'tasks.csv'
TEAM_DATA_FILE = 'team_members.csv'

# Load project data
def load_projects():
    try:
        return pd.read_csv(PROJECT_DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Project Name", "Description", "Start Date", "End Date", "Priority", "Status", "Progress", "Budget", "Tags"])

# Save project data
def save_projects(df):
    df.to_csv(PROJECT_DATA_FILE, index=False)

# Sidebar
st.sidebar.title("Menu")
menu_options = {
    "Add Project": "primary",
    "Edit Project": "success",
    "Delete Project": "danger",
    "Task Management": "info",
    "High Priority & Deadlines": "warning",
    "Team Management": "secondary"
}

# Display each menu item as a button with a different color
selected_menu = None
for option, color in menu_options.items():
    if st.sidebar.button(option, key=option, help=option, type=color):
        selected_menu = option

# Main UI Title
st.title("Software Management Tool")
st.write("Developed By Mansoor Sarookh, CS Student at GPGC Swabi")

# Main Body Functionality
if selected_menu == "Add Project":
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

elif selected_menu == "Edit Project":
    st.header("Edit Project")
    df = load_projects()
    if df.empty:
        st.info("No projects to edit.")
    else:
        project = st.selectbox("Select Project", df["Project Name"])
        if project:
            row = df[df["Project Name"] == project].iloc[0]
            new_name = st.text_input("Project Name", row["Project Name"])
            description = st.text_area("Project Description", row["Description"])
            start_date = st.date_input("Start Date", row["Start Date"])
            end_date = st.date_input("End Date", row["End Date"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(row["Priority"]))
            budget = st.number_input("Budget", min_value=0.0, value=row["Budget"])
            tags = st.text_input("Tags", row["Tags"])
            
            if st.button("Update Project"):
                df.loc[df["Project Name"] == project, ["Project Name", "Description", "Start Date", "End Date", "Priority", "Budget", "Tags"]] = new_name, description, start_date, end_date, priority, budget, tags
                save_projects(df)
                st.success(f"Project '{new_name}' has been updated.")

elif selected_menu == "Delete Project":
    st.header("Delete Project")
    df = load_projects()
    if df.empty:
        st.info("No projects to delete.")
    else:
        project = st.selectbox("Select Project to Delete", df["Project Name"])
        if st.button("Delete Project"):
            df = df[df["Project Name"] != project]
            save_projects(df)
            st.success(f"Project '{project}' has been deleted.")

elif selected_menu == "Task Management":
    st.header("Task Management")
    # Additional task management code here

elif selected_menu == "High Priority & Deadlines":
    st.header("Upcoming Deadlines & High Priority Projects")
    # Additional deadline view code here

elif selected_menu == "Team Management":
    st.header("Team Management")
    # Additional team management code here
