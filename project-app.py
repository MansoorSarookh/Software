import streamlit as st
import pandas as pd
from datetime import date, datetime

# File paths
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

# Load tasks
def load_tasks():
    try:
        return pd.read_csv(TASK_DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Project Name", "Task Name", "Deadline", "Status", "Assigned To"])

# Save tasks
def save_tasks(df):
    df.to_csv(TASK_DATA_FILE, index=False)

# Load team members
def load_team():
    try:
        return pd.read_csv(TEAM_DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Project Name", "Member Name", "Role"])

# Save team members
def save_team(df):
    df.to_csv(TEAM_DATA_FILE, index=False)

# Functions for each functionality
def add_project():
    st.subheader("Add New Project")
    # Collect project details
    name = st.text_input("Project Name")
    description = st.text_area("Project Description")
    start_date = st.date_input("Start Date", date.today())
    end_date = st.date_input("End Date")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    budget = st.number_input("Budget", min_value=0.0)
    tags = st.text_input("Tags (comma-separated)")
    
    # Save project
    if st.button("Create Project", key="create_project"):
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

def edit_project():
    st.subheader("Edit Project")
    df = load_projects()
    if df.empty:
        st.info("No projects to edit.")
        return
    
    project_names = df["Project Name"].tolist()
    project = st.selectbox("Select Project", project_names)
    
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

def delete_project():
    st.subheader("Delete Project")
    df = load_projects()
    if df.empty:
        st.info("No projects to delete.")
        return
    
    project = st.selectbox("Select Project to Delete", df["Project Name"])
    if st.button("Delete Project"):
        df = df[df["Project Name"] != project]
        save_projects(df)
        st.success(f"Project '{project}' has been deleted.")

def manage_tasks():
    st.subheader("Task Management")
    projects = load_projects()
    if projects.empty:
        st.info("No projects available.")
        return
    
    project = st.selectbox("Select Project", projects["Project Name"])
    tasks_df = load_tasks()
    task_name = st.text_input("Task Name")
    deadline = st.date_input("Deadline")
    assigned_to = st.text_input("Assigned To")
    
    if st.button("Add Task"):
        if project and task_name:
            new_task = pd.DataFrame({
                "Project Name": [project],
                "Task Name": [task_name],
                "Deadline": [deadline],
                "Status": ["Uncompleted"],
                "Assigned To": [assigned_to]
            })
            tasks_df = pd.concat([tasks_df, new_task], ignore_index=True)
            save_tasks(tasks_df)
            st.success(f"Task '{task_name}' has been added to project '{project}'.")

def view_high_priority():
    st.subheader("Upcoming Deadlines & High Priority Projects")
    df = load_projects()
    if df.empty:
        st.info("No projects available.")
        return
    
    today = date.today()
    upcoming_deadlines = df[df["End Date"] >= str(today)].sort_values("End Date")
    high_priority = upcoming_deadlines[upcoming_deadlines["Priority"] == "High"]

    if not high_priority.empty:
        st.subheader("High Priority Projects")
        for i, row in high_priority.iterrows():
            st.text(f"{row['Project Name']} - Deadline: {row['End Date']}")

    st.subheader("Upcoming Deadlines")
    for i, row in upcoming_deadlines.iterrows():
        st.text(f"{row['Project Name']} - Deadline: {row['End Date']}")

def manage_team():
    st.subheader("Team Management")
    df = load_team()
    project = st.selectbox("Assign Team Member to Project", load_projects()["Project Name"])
    member_name = st.text_input("Team Member Name")
    role = st.selectbox("Role", ["Project Manager", "Developer", "Designer", "QA"])

    if st.button("Add Member"):
        if project and member_name:
            new_member = pd.DataFrame({
                "Project Name": [project],
                "Member Name": [member_name],
                "Role": [role]
            })
            df = pd.concat([df, new_member], ignore_index=True)
            save_team(df)
            st.success(f"Team member '{member_name}' assigned to project '{project}'.")

# Main UI
st.title("Project Management Tool")
st.markdown("**Developed By Mansoor Sarookh, CS Student at GPGC Swabi**")

# Sidebar with buttons
if st.button("Add Project", key="add_proj"):
    add_project()
elif st.button("Edit Project", key="edit_proj"):
    edit_project()
elif st.button("Delete Project", key="del_proj"):
    delete_project()
elif st.button("Task Management", key="task_mgmt"):
    manage_tasks()
elif st.button("High Priority & Deadlines", key="high_prio"):
    view_high_priority()
elif st.button("Team Management", key="team_mgmt"):
    manage_team()
