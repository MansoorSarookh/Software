import streamlit as st
import pandas as pd
import os
from datetime import date

# File paths
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
STUDENT_FILE = os.path.join(DATA_DIR, "students.csv")
FEES_FILE = os.path.join(DATA_DIR, "fees.csv")
RESULTS_FILE = os.path.join(DATA_DIR, "results.csv")
LEAVING_CERT_FILE = os.path.join(DATA_DIR, "leaving_certificates.csv")
TEACHERS_FILE = os.path.join(DATA_DIR, "teachers.csv")
FINANCIAL_LOG_FILE = os.path.join(DATA_DIR, "financial_log.csv")

# Initialize CSVs
for file in [STUDENT_FILE, FEES_FILE, RESULTS_FILE, LEAVING_CERT_FILE, TEACHERS_FILE, FINANCIAL_LOG_FILE]:
    if not os.path.exists(file):
        pd.DataFrame().to_csv(file, index=False)


# Helper functions
def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()


def save_data(data, file_path):
    data.to_csv(file_path, index=False)


def app_title():
    st.title("School Management System")
    st.markdown("**Developed by Mansoor Sarookh**")


# Main App
app_title()

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Student Admission Management",
        "Fees Management",
        "Student Fee Overview",
        "Award List and Results",
        "Leaving Certificate Management",
        "Teacher Records",
        "Daily Financial Management (Roznamcha)"
    ]
)

# Student Admission Management
if menu == "Student Admission Management":
    st.header("Student Admission Management")

    # Admission Form
    with st.form("admission_form"):
        name = st.text_input("Student Name")
        father_name = st.text_input("Father's Name")
        student_class = st.text_input("Class")
        address = st.text_area("Address")
        transport = st.checkbox("Transport Required?")
        fees = st.number_input("Class Fees", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Submit")

    # Save Data
    if submitted:
        students = load_data(STUDENT_FILE)
        new_student = pd.DataFrame([{
            "Name": name,
            "Father's Name": father_name,
            "Class": student_class,
            "Address": address,
            "Transport": transport,
            "Fees": fees
        }])
        updated_students = pd.concat([students, new_student], ignore_index=True)
        save_data(updated_students, STUDENT_FILE)
        st.success("Student added successfully!")

    # View and Download Data
    students = load_data(STUDENT_FILE)
    st.dataframe(students)
    if not students.empty:
        csv = students.to_csv(index=False).encode('utf-8')
        st.download_button("Download Admission Data", csv, "students.csv")

# Fees Management
elif menu == "Fees Management":
    st.header("Fees Management")
    students = load_data(STUDENT_FILE)

    if not students.empty:
        student_name = st.selectbox("Select Student", students["Name"])
        month = st.selectbox("Select Month", [f"{i:02d}" for i in range(1, 13)])
        transport_fees = st.checkbox("Include Transport Fee")
        submitted = st.button("Log Payment")

        if submitted:
            fees_data = load_data(FEES_FILE)
            new_payment = pd.DataFrame([{
                "Name": student_name,
                "Month": month,
                "Transport Fee": transport_fees,
                "Date": date.today()
            }])
            updated_fees = pd.concat([fees_data, new_payment], ignore_index=True)
            save_data(updated_fees, FEES_FILE)
            st.success("Payment logged successfully!")

    fees_data = load_data(FEES_FILE)
    st.dataframe(fees_data)
    if not fees_data.empty:
        csv = fees_data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Fees Data", csv, "fees.csv")

# Student Fee Overview
elif menu == "Student Fee Overview":
    st.header("Student Fee Overview")
    fees_data = load_data(FEES_FILE)

    if not fees_data.empty:
        st.dataframe(fees_data)
        csv = fees_data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Fees Overview", csv, "fees_overview.csv")

# Award List and Results
elif menu == "Award List and Results":
    st.header("Award List and Results")

    # Input Form
    with st.form("result_form"):
        student_name = st.text_input("Student Name")
        rank = st.selectbox("Rank", ["First", "Second", "Third", "None"])
        total_marks = st.number_input("Total Marks", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Save Result")

    if submitted:
        results = load_data(RESULTS_FILE)
        new_result = pd.DataFrame([{
            "Name": student_name,
            "Rank": rank,
            "Total Marks": total_marks
        }])
        updated_results = pd.concat([results, new_result], ignore_index=True)
        save_data(updated_results, RESULTS_FILE)
        st.success("Result saved successfully!")

    results = load_data(RESULTS_FILE)
    st.dataframe(results)
    if not results.empty:
        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results", csv, "results.csv")

# Leaving Certificate Management
elif menu == "Leaving Certificate Management":
    st.header("Leaving Certificate Management")

    # Input Form
    with st.form("leaving_form"):
        student_name = st.text_input("Student Name")
        leaving_date = st.date_input("Leaving Date")
        reason = st.text_area("Reason")
        submitted = st.form_submit_button("Generate Certificate")

    if submitted:
        cert_data = load_data(LEAVING_CERT_FILE)
        new_cert = pd.DataFrame([{
            "Name": student_name,
            "Leaving Date": leaving_date,
            "Reason": reason
        }])
        updated_cert_data = pd.concat([cert_data, new_cert], ignore_index=True)
        save_data(updated_cert_data, LEAVING_CERT_FILE)
        st.success("Certificate generated successfully!")

    cert_data = load_data(LEAVING_CERT_FILE)
    st.dataframe(cert_data)

# Teacher Records
elif menu == "Teacher Records":
    st.header("Teacher Records")

    # Input Form
    with st.form("teacher_form"):
        name = st.text_input("Teacher Name")
        join_date = st.date_input("Joining Date")
        education = st.text_input("Highest Education")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        employment_type = st.selectbox("Employment Type", ["Contract", "Permanent"])
        submitted = st.form_submit_button("Save Record")

    if submitted:
        teachers = load_data(TEACHERS_FILE)
        new_teacher = pd.DataFrame([{
            "Name": name,
            "Joining Date": join_date,
            "Education": education,
            "Gender": gender,
            "Employment Type": employment_type
        }])
        updated_teachers = pd.concat([teachers, new_teacher], ignore_index=True)
        save_data(updated_teachers, TEACHERS_FILE)
        st.success("Teacher record saved successfully!")

    teachers = load_data(TEACHERS_FILE)
    st.dataframe(teachers)

# Daily Financial Management
elif menu == "Daily Financial Management (Roznamcha)":
    st.header("Daily Financial Management")

    # Input Form
    with st.form("financial_form"):
        date_entry = st.date_input("Date")
        fees_collected = st.number_input("Fees Collected", min_value=0, value=0, step=1)
        salaries_paid = st.number_input("Salaries Paid", min_value=0, value=0, step=1)
        other_expenses = st.number_input("Other Expenses", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Log Entry")

    if submitted:
        finance_log = load_data(FINANCIAL_LOG_FILE)
        new_entry = pd.DataFrame([{
            "Date": date_entry,
            "Fees Collected": fees_collected,
            "Salaries Paid": salaries_paid,
            "Other Expenses": other_expenses
        }])
        updated_finance_log = pd.concat([finance_log, new_entry], ignore_index=True)
        save_data(updated_finance_log, FINANCIAL_LOG_FILE)
        st.success("Financial entry logged successfully!")

    finance_log = load_data(FINANCIAL_LOG_FILE)
    st.dataframe(finance_log)
