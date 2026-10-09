"""
main.py
Run with: streamlit run main.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from student_module import (
    Student, PremiumStudent, SUBJECT_FEES,
    register_student, calculate_fee, display_student_info
)

st.set_page_config(page_title="BrightMind Tuition Centre", page_icon="📚", layout="wide")
st.title("📚 BrightMind Tuition Centre")
st.write("Student registration, subject fee calculation and performance analysis")

# Store registered students while the Streamlit session is active.
if "students" not in st.session_state:
    st.session_state.students = []

st.header("1. Student Registration")
with st.form("student_registration"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Student name")
        student_id = st.text_input("Student ID")
        age = st.number_input("Age", min_value=5, max_value=100, value=15, step=1)
    with col2:
        student_type = st.selectbox("Student type", ["Regular Student", "Premium Student"])
        marks = st.number_input("Performance mark (0–100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        selected_subjects = st.multiselect(
            "Select subjects (each subject displays its fee)",
            options=list(SUBJECT_FEES.keys()),
            format_func=lambda subject: f"{subject} — RM {SUBJECT_FEES[subject]:.2f}"
        )
    submitted = st.form_submit_button("Register Student and Calculate Fee")

if submitted:
    try:
        if not name.strip():
            raise ValueError("Please enter the student's name.")
        if not student_id.strip():
            raise ValueError("Please enter a student ID.")
        if not selected_subjects:
            raise ValueError("Please select at least one subject.")
        if any(s.student_id.lower() == student_id.strip().lower() for s in st.session_state.students):
            raise ValueError("This student ID is already registered.")

        # Call the required register_student function.
        if student_type == "Premium Student":
            student = PremiumStudent(name, age, student_id, marks, selected_subjects)
        else:
            student = register_student(name, age, student_id, marks, selected_subjects)

        discount = student.discount if isinstance(student, PremiumStudent) else 0
        total_fee = calculate_fee(selected_subjects, discount=discount)
        st.session_state.students.append({
            "object": student,
            "student_id": student.student_id,
            "name": student.name,
            "age": student.age,
            "student_type": student.student_type,
            "marks": student.marks,
            "subjects": list(student.subjects),
            "subject_count": len(student.subjects),
            "fee": total_fee,
        })
        st.success("Student registered successfully!")
        st.rerun()
    except (ValueError, TypeError) as error:
        st.error(f"Input error: {error}")
    except Exception as error:
        st.error(f"Unexpected error: {error}")

st.header("2. Registered Student Information and Fees")
if st.session_state.students:
    for item in st.session_state.students:
        with st.expander(f"{item['name']} — {item['student_id']}"):
            # Call the required display_student_info function.
            st.text(display_student_info(item["object"]))
            st.write("**Selected subjects and individual fees**")
            for subject in item["subjects"]:
                st.write(f"- {subject}: RM {SUBJECT_FEES[subject]:.2f}")
            st.write(f"**Total subject fee: RM {item['fee']:.2f}**")
    fee_df = pd.DataFrame([
        {"Student ID": s["student_id"], "Name": s["name"], "Type": s["student_type"],
         "Subjects": ", ".join(s["subjects"]), "Total Fee (RM)": s["fee"], "Marks": s["marks"]}
        for s in st.session_state.students
    ])
    st.dataframe(fee_df, use_container_width=True)
    st.metric("Total fees for all registered students", f"RM {fee_df['Total Fee (RM)'].sum():.2f}")
else:
    st.info("No students registered yet. Complete the form above to add a student.")

st.header("3. OOP Demonstration")
st.write("**Magic methods:** `__init__` initializes each object, `__str__` creates readable text, and `__add__` adds the marks of two Student objects.")
demo_a = Student("Demo A", 15, "D001", 75)
demo_b = Student("Demo B", 16, "D002", 85)
st.write(f"Object A: {demo_a}")
st.write(f"Object B: {demo_b}")
st.write(f"Operator overloading (Demo A + Demo B marks): {demo_a + demo_b:.1f} / 200")
st.write("**Function overloading-style example using default parameters:**")
st.code(
    "calculate_fee(['Mathematics'])                         # no discount or registration fee\n"
    "calculate_fee(['Mathematics', 'Science'], discount=10) # 10% discount\n"
    "calculate_fee(['English'], discount=5, registration_fee=20)",
    language="python"
)
st.write(f"Example fee with defaults: RM {calculate_fee(['Mathematics']):.2f}")
st.write(f"Example fee with 10% discount: RM {calculate_fee(['Mathematics', 'Science'], discount=10):.2f}")
st.write(f"Example fee with registration fee: RM {calculate_fee(['English'], discount=5, registration_fee=20):.2f}")

st.header("4. NumPy, Pandas and Student Data Analysis")
if st.session_state.students:
    df = pd.DataFrame([
        {"Student ID": s["student_id"], "Name": s["name"], "Age": s["age"],
         "Marks": s["marks"], "Subject Count": s["subject_count"],
         "Fee (RM)": s["fee"], "Type": s["student_type"]}
        for s in st.session_state.students
    ])
else:
    # Sample records ensure analysis, indexing/slicing and graph are visible before registration.
    df = pd.DataFrame([
        {"Student ID": "S001", "Name": "Aina", "Age": 15, "Marks": 88.0, "Subject Count": 3, "Fee (RM)": 235.0, "Type": "Regular Student"},
        {"Student ID": "S002", "Name": "Hakim", "Age": 16, "Marks": 76.0, "Subject Count": 2, "Fee (RM)": 155.0, "Type": "Premium Student"},
        {"Student ID": "S003", "Name": "Mei", "Age": 14, "Marks": 92.0, "Subject Count": 4, "Fee (RM)": 300.0, "Type": "Regular Student"},
    ])
    st.caption("Sample data is shown until you register students.")

marks_array = np.array(df["Marks"], dtype=float)
st.subheader("Pandas DataFrame")
st.dataframe(df, use_container_width=True)
st.subheader("NumPy array and attributes")
st.write("Marks array:", marks_array)
st.write(f"Array shape: {marks_array.shape} | Number of dimensions: {marks_array.ndim} | Array size: {marks_array.size}")
st.write("Indexing — first mark:", float(marks_array[0]))
st.write("Slicing — first three marks:", marks_array[:3])
st.subheader("Mathematical analysis")
st.write(f"Average mark: {np.mean(marks_array):.2f}")
st.write(f"Highest mark: {np.max(marks_array):.2f}")
st.write(f"Lowest mark: {np.min(marks_array):.2f}")
st.write(f"Standard deviation: {np.std(marks_array):.2f}")
st.subheader("Filter and sort data")
minimum_mark = st.slider("Show students with marks at least", min_value=0, max_value=100, value=70)
filtered_df = df[df["Marks"] >= minimum_mark].sort_values(by="Marks", ascending=False)
st.dataframe(filtered_df, use_container_width=True)

st.subheader("Graph: Student Performance")
fig, ax = plt.subplots()
ax.bar(df["Name"], df["Marks"])
ax.set_xlabel("Student")
ax.set_ylabel("Marks")
ax.set_title("Student Marks Comparison")
ax.set_ylim(0, 100)
ax.grid(axis="y", alpha=0.25)
st.pyplot(fig)
plt.close(fig)

st.caption("Subject fees: " + " | ".join(f"{subject}: RM {fee}" for subject, fee in SUBJECT_FEES.items()))
