import streamlit as st
import pandas as pd
from datetime import date

# File to store project data
PROJECT_DATA_FILE = 'projects.csv'
TASK_DATA_FILE = 'tasks.csv'
TEAM_DATA_FILE = 'team_members.csv'

# Set up the page title and sidebar menu
st.set_page_config(page_title="Project Management Tool", layout="wide")
st.sidebar.title("Project Management Tool")
st.sidebar.title("Developed By Mansoor Sarookh, CS Student at GPGC Swabi")

# Define menu options
menu_options = [
    "Add Project", 
    "Edit Project", 
    "Delete Project", 
    "Task Management", 
    "High Priority & Deadlines", 
    "Team Management"
]
selected_menu = st.sidebar.radio("Navigation", menu_options)

# Load and save data functions
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

# Functionality: Add new project
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

# Functionality: Edit project
def edit_project():
    st.header("Edit Project")
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

# Functionality: Delete project
def delete_project():
    st.header("Delete Project")
    df = load_projects()
    if df.empty:
        st.info("No projects to delete.")
        return
    
    project = st.selectbox("Select Project to Delete", df["Project Name"])
    if st.button("Delete Project"):
        df = df[df["Project Name"] != project]
        save_projects(df)
        st.success(f"Project '{project}' has been deleted.")

# Functionality: Task management within each project
def manage_tasks():
    st.header("Task Management")
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

    if not tasks_df.empty:
        st.subheader("Existing Tasks")
        project_tasks = tasks_df[tasks_df["Project Name"] == project]
        for i, task in project_tasks.iterrows():
            st.text(f"Task: {task['Task Name']} | Deadline: {task['Deadline']} | Status: {task['Status']} | Assigned To: {task['Assigned To']}")
            if task["Status"] == "Uncompleted" and st.button(f"Mark '{task['Task Name']}' as Completed", key=f"task_complete_{i}"):
                tasks_df.at[i, "Status"] = "Completed"
                save_tasks(tasks_df)
                st.success(f"'{task['Task Name']}' marked as completed.")

# Functionality: View project deadlines and high-priority projects
def view_high_priority():
    st.header("Upcoming Deadlines & High Priority Projects")
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

# Functionality: Team collaboration and management
def manage_team():
    st.header("Team Management")
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

    if not df.empty:
        st.subheader("Team Members")
        for i, member in df.iterrows():
            st.text(f"Member: {member['Member Name']} | Role: {member['Role']} | Project: {member['Project Name']}")

# Display selected functionality based on sidebar choice
if selected_menu == "Add Project":
    add_project()
elif selected_menu == "Edit Project":
    edit_project()
elif selected_menu == "Delete Project":
    delete_project()
elif selected_menu == "Task Management":
    manage_tasks()
elif selected_menu == "High Priority & Deadlines":
    view_high_priority()
elif selected_menu == "Team Management":
    manage_team()


