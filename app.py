import streamlit as st
import sqlite3
from datetime import date


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Healthcare Management System",
    page_icon="🏥",
    layout="wide"
)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    return sqlite3.connect(
        "data/healthcare.db",
        check_same_thread=False
    )


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT,
            phone TEXT,
            email TEXT,
            blood_group TEXT,
            medical_history TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            reason TEXT,
            status TEXT
        )
    """)

    connection.commit()
    connection.close()


create_tables()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🏥 Healthcare System")

st.sidebar.write("Navigation")

menu = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Patient Registration",
        "Patient Records",
        "Appointments",
        "Health Assessment",
        "AI Health Assistant",
        "About"
    ]
)


# ==========================================
# DASHBOARD
# ==========================================

if menu == "Dashboard":

    st.title("🏥 AI Healthcare Management System")

    st.subheader("Welcome!")

    st.write(
        "This system helps manage patient information, "
        "appointments and basic health assessments."
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM patients"
    )

    patient_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM appointments"
    )

    appointment_count = cursor.fetchone()[0]

    connection.close()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Patients",
            patient_count
        )

    with col2:

        st.metric(
            "Total Appointments",
            appointment_count
        )

    with col3:

        st.metric(
            "System Status",
            "Active"
        )

    st.divider()

    st.info(
        "Select a module from the sidebar to use the system."
    )


# ==========================================
# PATIENT REGISTRATION
# ==========================================

elif menu == "Patient Registration":

    st.title("👤 Patient Registration")

    st.write(
        "Enter the patient's basic information below."
    )

    with st.form("patient_registration_form"):

        name = st.text_input(
            "Patient Name"
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=18
        )

        gender = st.selectbox(
            "Gender",
            [
                "Female",
                "Male",
                "Other"
            ]
        )

        phone = st.text_input(
            "Phone Number"
        )

        email = st.text_input(
            "Email"
        )

        blood_group = st.selectbox(
            "Blood Group",
            [
                "Unknown",
                "A+",
                "A-",
                "B+",
                "B-",
                "AB+",
                "AB-",
                "O+",
                "O-"
            ]
        )

        medical_history = st.text_area(
            "Medical History"
        )

        submit = st.form_submit_button(
            "Register Patient"
        )

        if submit:

            if name.strip() == "":

                st.error(
                    "Please enter the patient's name."
                )

            else:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO patients
                    (
                        name,
                        age,
                        gender,
                        phone,
                        email,
                        blood_group,
                        medical_history
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        age,
                        gender,
                        phone,
                        email,
                        blood_group,
                        medical_history
                    )
                )

                connection.commit()
                connection.close()

                st.success(
                    "Patient registered successfully! ✅"
                )


# ==========================================
# PATIENT RECORDS
# ==========================================

elif menu == "Patient Records":

    st.title("📋 Patient Records")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            patient_id,
            name,
            age,
            gender,
            phone,
            email,
            blood_group,
            medical_history
        FROM patients
        ORDER BY patient_id DESC
        """
    )

    patients = cursor.fetchall()

    connection.close()

    if len(patients) == 0:

        st.info(
            "No patient records found."
        )

    else:

        st.write(
            f"Total registered patients: {len(patients)}"
        )

        for patient in patients:

            with st.expander(
                f"Patient #{patient[0]} — {patient[1]}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Age:** {patient[2]}"
                    )

                    st.write(
                        f"**Gender:** {patient[3]}"
                    )

                    st.write(
                        f"**Phone:** {patient[4]}"
                    )

                    st.write(
                        f"**Email:** {patient[5]}"
                    )

                with col2:

                    st.write(
                        f"**Blood Group:** {patient[6]}"
                    )

                    st.write(
                        f"**Medical History:** "
                        f"{patient[7]}"
                    )


# ==========================================
# APPOINTMENTS
# ==========================================

elif menu == "Appointments":

    st.title("📅 Appointment Management")

    st.subheader("Book New Appointment")

    with st.form("appointment_form"):

        patient_name = st.text_input(
            "Patient Name"
        )

        doctor = st.text_input(
            "Doctor Name"
        )

        appointment_date = st.date_input(
            "Appointment Date",
            value=date.today()
        )

        appointment_time = st.time_input(
            "Appointment Time"
        )

        reason = st.text_area(
            "Reason for Appointment"
        )

        status = st.selectbox(
            "Appointment Status",
            [
                "Scheduled",
                "Completed",
                "Cancelled"
            ]
        )

        submit = st.form_submit_button(
            "Book Appointment"
        )

        if submit:

            if (
                patient_name.strip() == ""
                or doctor.strip() == ""
            ):

                st.error(
                    "Please enter patient and doctor names."
                )

            else:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO appointments
                    (
                        patient_name,
                        doctor,
                        appointment_date,
                        appointment_time,
                        reason,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        patient_name,
                        doctor,
                        str(appointment_date),
                        str(appointment_time),
                        reason,
                        status
                    )
                )

                connection.commit()
                connection.close()

                st.success(
                    "Appointment booked successfully! ✅"
                )

    st.divider()

    st.subheader("Appointment List")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            appointment_id,
            patient_name,
            doctor,
            appointment_date,
            appointment_time,
            reason,
            status
        FROM appointments
        ORDER BY appointment_date
        """
    )

    appointments = cursor.fetchall()

    connection.close()

    if len(appointments) == 0:

        st.info(
            "No appointments available."
        )

    else:

        for appointment in appointments:

            st.write(
                f"### Appointment #{appointment[0]}"
            )

            st.write(
                f"**Patient:** {appointment[1]}"
            )

            st.write(
                f"**Doctor:** {appointment[2]}"
            )

            st.write(
                f"**Date:** {appointment[3]}"
            )

            st.write(
                f"**Time:** {appointment[4]}"
            )

            st.write(
                f"**Reason:** {appointment[5]}"
            )

            st.write(
                f"**Status:** {appointment[6]}"
            )

            st.divider()


# ==========================================
# HEALTH ASSESSMENT
# ==========================================

elif menu == "Health Assessment":

    st.title("🩺 Basic Health Assessment")

    st.warning(
        "This is an educational screening tool. "
        "It does not diagnose medical conditions."
    )

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=18
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=30.0,
        max_value=45.0,
        value=36.5
    )

    symptoms = st.multiselect(
        "Select symptoms",
        [
            "Fever",
            "Cough",
            "Headache",
            "Fatigue",
            "Sore throat",
            "Nausea",
            "Vomiting",
            "Breathing difficulty"
        ]
    )

    analyze = st.button(
        "Analyze Health Information"
    )

    if analyze:

        if "Breathing difficulty" in symptoms:

            st.error(
                "Breathing difficulty can be serious. "
                "Please seek appropriate medical attention."
            )

        elif temperature >= 38:

            st.warning(
                "The entered temperature is elevated. "
                "Consider contacting a healthcare professional "
                "if symptoms continue or become worse."
            )

        elif len(symptoms) >= 3:

            st.info(
                "Several symptoms were selected. "
                "This tool cannot determine the cause. "
                "Consider discussing your symptoms with "
                "a healthcare professional."
            )

        else:

            st.success(
                "No high-risk indicator was detected "
                "by this basic educational screening."
            )


# ==========================================
# AI HEALTH ASSISTANT
# ==========================================

elif menu == "AI Health Assistant":

    st.title("🤖 AI Health Assistant")

    st.write(
        "Ask general health-information questions."
    )

    st.warning(
        "The AI assistant will provide general educational "
        "information only. It is not a doctor and cannot "
        "provide a medical diagnosis."
    )

    question = st.text_area(
        "Enter your question"
    )

    if st.button("Ask AI"):

        if question.strip() == "":

            st.error(
                "Please enter a question."
            )

        else:

            st.info(
                "AI integration will be connected in the "
                "next development stage."
            )


# ==========================================
# ABOUT
# ==========================================

elif menu == "About":

    st.title("ℹ️ About the Project")

    st.write(
        """
        ## AI Healthcare Management System

        This project is developed using Python and Streamlit.

        ### Main Features

        • Patient Registration

        • Patient Records

        • Appointment Management

        • Basic Health Assessment

        • AI Health Assistant

        ### Purpose

        The system demonstrates how a healthcare management
        application can be developed using Python, databases,
        Streamlit and AI technologies.

        ### Disclaimer

        This application is created for educational purposes.
        It should not be used as a replacement for professional
        medical diagnosis, treatment or emergency services.
        """
    )