"""
student_module.py
BrightMind Tuition Centre Management and Data Analysis System
"""

SUBJECT_FEES = {
    "Mathematics": 80,
    "English": 70,
    "Science": 85,
    "Computer Science": 90,
    "Bahasa Melayu": 65,
}

def register_student(name, age, student_id, marks=0, subjects=None):
    """Create and return a Student object (default parameters allow flexible calls)."""
    return Student(name, age, student_id, marks, subjects or [])

def calculate_fee(selected_subjects, discount=0, registration_fee=0):
    """
    Calculate subject fees with optional discount and registration fee.
    Default parameters demonstrate function overloading-style behaviour in Python.
    """
    subtotal = sum(SUBJECT_FEES.get(subject, 0) for subject in selected_subjects)
    discount_amount = subtotal * discount / 100
    return max(0, subtotal - discount_amount + registration_fee)

def display_student_info(student):
    """Return formatted information for display in the Streamlit interface."""
    subjects = ", ".join(student.subjects) if student.subjects else "No subjects selected"
    return (
        f"Student ID: {student.student_id}\n"
        f"Name: {student.name}\n"
        f"Age: {student.age}\n"
        f"Type: {student.student_type}\n"
        f"Marks: {student.marks:.1f}\n"
        f"Subjects: {subjects}"
    )

class Student:
    """Represent a student registered at the tuition centre."""

    def __init__(self, name, age, student_id, marks=0, subjects=None):
        self.name = str(name).strip()
        self.age = int(age)
        self.student_id = str(student_id).strip()
        self.marks = float(marks)
        self.subjects = list(subjects) if subjects else []
        self.student_type = "Regular Student"

    def __str__(self):
        return f"{self.name} ({self.student_id}) - {self.student_type}"

    def __add__(self, other):
        """Operator overloading: add marks of two Student objects."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.marks + other.marks

class PremiumStudent(Student):
    """Premium student inherits Student and receives a 10% subject-fee discount."""

    def __init__(self, name, age, student_id, marks=0, subjects=None, discount=10):
        super().__init__(name, age, student_id, marks, subjects)
        self.discount = float(discount)
        self.student_type = "Premium Student"

    def __str__(self):
        return f"{self.name} ({self.student_id}) - {self.student_type}, {self.discount:.0f}% discount"
