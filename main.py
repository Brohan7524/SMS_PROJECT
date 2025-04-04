import psycopg2
import customtkinter as ctk
from tkinter import messagebox

from tables import create_tables
from db_manager import DatabaseManager

ctk.set_appearance_mode("dark")  # Set to dark theme
ctk.set_default_color_theme("dark-blue")  # Use the dark-blue theme

#check for main.py updates
class StudentManagementSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1200x800")

        self.db_manager = DatabaseManager()
        self.frames = {}
        self.setup_navigation()
        self.setup_frames()
        self.show_frame("home_frame")

    def setup_navigation(self):
        self.nav_frame = ctk.CTkFrame(self, width=150)
        self.nav_frame.pack(side="left", fill="y")

        self.nav_buttons = {
            "Home": "home_frame",
            "Students": "students_frame",
            "Courses": "courses_frame",
            "Departments": "departments_frame",
        }

        for text, frame_key in self.nav_buttons.items():
            button = ctk.CTkButton(
                self.nav_frame,
                text=text,
                command=lambda key=frame_key: self.show_frame(key),
            )
            button.pack(pady=5, padx=10, fill="x")

    def setup_frames(self):
        for name in self.nav_buttons.values():
            self.frames[name] = ctk.CTkFrame(self)
            self.frames[name].place(x=150, y=0, relwidth=0.85, relheight=1)

        self.create_student_form()
        self.create_course_form()
        self.create_department_form()

    def show_frame(self, frame_key):
        if frame_key in self.frames:
            self.frames[frame_key].tkraise()

    def create_student_form(self):
        frame = self.frames["students_frame"]
        ctk.CTkLabel(frame, text="Manage Students", font=("Arial", 24)).pack(pady=20)

        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(pady=30, anchor="center")

        self.student_entries = {
            "First Name": ctk.CTkEntry(form_frame, placeholder_text="First Name", justify="center"),
            "Last Name": ctk.CTkEntry(form_frame, placeholder_text="Last Name", justify="center"),
            "DOB": ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", justify="center"),
            "Gender": ctk.CTkEntry(form_frame, placeholder_text="Male/Female/Other", justify="center"),
            "Email": ctk.CTkEntry(form_frame, placeholder_text="Email", justify="center"),
            "Phone": ctk.CTkEntry(form_frame, placeholder_text="Phone", justify="center"),
            "Address": ctk.CTkEntry(form_frame, placeholder_text="Address", justify="center"),
            "Admission Date": ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", justify="center"),
            "Department ID": ctk.CTkEntry(form_frame, placeholder_text="Department ID", justify="center")
        }

        for i, (label, entry) in enumerate(self.student_entries.items()):
            entry.grid(row=i, column=0, pady=5, padx=20, sticky="ew")

        ctk.CTkButton(form_frame, text="Add Student", command=self.add_student).grid(row=len(self.student_entries), column=0, pady=10)
        ctk.CTkButton(form_frame, text="Display Students", command=lambda: self.display_records("Students")).grid(row=len(self.student_entries) + 1, column=0, pady=5)

    def create_course_form(self):
        frame = self.frames["courses_frame"]
        ctk.CTkLabel(frame, text="Manage Courses", font=("Arial", 24)).pack(pady=20)

        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(pady=30, anchor="center")

        self.course_entries = {
            "Course Name": ctk.CTkEntry(form_frame, placeholder_text="Course Name", justify="center"),
            "Course Code": ctk.CTkEntry(form_frame, placeholder_text="Course Code", justify="center"),
            "Credits": ctk.CTkEntry(form_frame, placeholder_text="Credits", justify="center"),
            "Department ID": ctk.CTkEntry(form_frame, placeholder_text="Department ID", justify="center"),
            "Teacher ID": ctk.CTkEntry(form_frame, placeholder_text="Teacher ID", justify="center")
        }

        for i, (label, entry) in enumerate(self.course_entries.items()):
            entry.grid(row=i, column=0, pady=5, padx=20, sticky="ew")

        ctk.CTkButton(form_frame, text="Add Course", command=self.add_course).grid(row=len(self.course_entries), column=0, pady=10)
        ctk.CTkButton(form_frame, text="Display Courses", command=lambda: self.display_records("Courses")).grid(row=len(self.course_entries) + 1, column=0, pady=5)

    def create_department_form(self):
        frame = self.frames["departments_frame"]
        ctk.CTkLabel(frame, text="Manage Departments", font=("Arial", 24)).pack(pady=20)

        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(pady=30, anchor="center")

        self.department_entries = {
            "Department Name": ctk.CTkEntry(form_frame, placeholder_text="Department Name", justify="center"),
            "Head of Department ID": ctk.CTkEntry(form_frame, placeholder_text="Head of Department ID", justify="center")
        }

        for i, (label, entry) in enumerate(self.department_entries.items()):
            entry.grid(row=i, column=0, pady=5, padx=20, sticky="ew")

        ctk.CTkButton(form_frame, text="Add Department", command=self.add_department).grid(row=len(self.department_entries), column=0, pady=10)
        ctk.CTkButton(form_frame, text="Display Departments", command=lambda: self.display_records("Departments")).grid(row=len(self.department_entries) + 1, column=0, pady=5)

    def add_student(self):
        values = [entry.get() for entry in self.student_entries.values()]
        query = (
            "INSERT INTO Students (first_name, last_name, dob, gender, email, phone_number, address, admission_date, department_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        self.db_manager.execute_query(query, values)
        messagebox.showinfo("Success", "Student added successfully!")

    def add_course(self):
        values = [entry.get() for entry in self.course_entries.values()]
        query = "INSERT INTO Courses (course_name, course_code, credits, department_id, teacher_id) VALUES (%s, %s, %s, %s, %s)"
        self.db_manager.execute_query(query, values)
        messagebox.showinfo("Success", "Course added successfully!")

    def add_department(self):
        values = [entry.get() for entry in self.department_entries.values()]
        query = "INSERT INTO Departments (department_name, head_of_department_id) VALUES (%s, %s)"
        self.db_manager.execute_query(query, values)
        messagebox.showinfo("Success", "Department added successfully!")


def main():
    create_tables()
    app = StudentManagementSystem()
    app.mainloop()


if __name__ == "__main__":
    main()
