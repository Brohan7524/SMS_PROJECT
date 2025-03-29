
import psycopg2
import customtkinter as ctk
from tkinter import ttk, messagebox

from tables import create_tables
from db_manager import DatabaseManager

import customtkinter as ctk
from tkinter import messagebox

class StudentManagementSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1200x800")
        self.configure(fg_color="white")

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
            ctk.CTkButton(
                self.nav_frame,
                text=text,
                command=lambda key=frame_key: self.show_frame(key)
            ).pack(pady=5, padx=10, fill="x")

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
        ctk.CTkLabel(frame, text="Manage Students", font=("Arial", 20)).pack(pady=10)

        self.student_entries = {
            "First Name": ctk.CTkEntry(frame, placeholder_text="First Name"),
            "Last Name": ctk.CTkEntry(frame, placeholder_text="Last Name"),
            "DOB": ctk.CTkEntry(frame, placeholder_text="YYYY-MM-DD"),
            "Gender": ctk.CTkEntry(frame, placeholder_text="Male/Female/Other"),
            "Email": ctk.CTkEntry(frame, placeholder_text="Email"),
            "Phone": ctk.CTkEntry(frame, placeholder_text="Phone"),
            "Address": ctk.CTkEntry(frame, placeholder_text="Address"),
            "Admission Date": ctk.CTkEntry(frame, placeholder_text="YYYY-MM-DD"),
            "Department ID": ctk.CTkEntry(frame, placeholder_text="Department ID")
        }

        for entry in self.student_entries.values():
            entry.pack(pady=5)

        ctk.CTkButton(frame, text="Add Student", command=self.add_student).pack(pady=5)
        ctk.CTkButton(frame, text="Display Students", command=lambda: self.display_records("Students")).pack(pady=5)

        self.student_display = ctk.CTkTextbox(frame, height=200)
        self.student_display.pack(pady=5, fill="both", expand=True)

    def create_course_form(self):
        frame = self.frames["courses_frame"]
        ctk.CTkLabel(frame, text="Manage Courses", font=("Arial", 20)).pack(pady=10)

        self.course_entries = {
            "Course Name": ctk.CTkEntry(frame, placeholder_text="Course Name"),
            "Course Code": ctk.CTkEntry(frame, placeholder_text="Course Code"),
            "Credits": ctk.CTkEntry(frame, placeholder_text="Credits"),
            "Department ID": ctk.CTkEntry(frame, placeholder_text="Department ID"),
            "Teacher ID": ctk.CTkEntry(frame, placeholder_text="Teacher ID")
        }

        for entry in self.course_entries.values():
            entry.pack(pady=5)

        ctk.CTkButton(frame, text="Add Course", command=self.add_course).pack(pady=5)
        ctk.CTkButton(frame, text="Display Courses", command=lambda: self.display_records("Courses")).pack(pady=5)

        self.course_display = ctk.CTkTextbox(frame, height=200)
        self.course_display.pack(pady=5, fill="both", expand=True)

    def create_department_form(self):
        frame = self.frames["departments_frame"]
        ctk.CTkLabel(frame, text="Manage Departments", font=("Arial", 20)).pack(pady=10)

        self.department_entries = {
            "Department Name": ctk.CTkEntry(frame, placeholder_text="Department Name"),
            "Head of Department ID": ctk.CTkEntry(frame, placeholder_text="Head of Department ID")
        }

        for entry in self.department_entries.values():
            entry.pack(pady=5)

        ctk.CTkButton(frame, text="Add Department", command=self.add_department).pack(pady=5)
        ctk.CTkButton(frame, text="Display Departments", command=lambda: self.display_records("Departments")).pack(pady=5)

        self.department_display = ctk.CTkTextbox(frame, height=200)
        self.department_display.pack(pady=5, fill="both", expand=True)

    def add_student(self):
        values = [entry.get() for entry in self.student_entries.values()]
        query = (
            "INSERT INTO Students (first_name, last_name, dob, gender, email, phone_number, "
            "address, admission_date, department_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        self.db_manager.execute_query(query, values)
        messagebox.showinfo("Success", "Student added successfully!")

    def add_course(self):
        values = [entry.get() for entry in self.course_entries.values()]
        query = (
            "INSERT INTO Courses (course_name, course_code, credits, department_id, teacher_id) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        self.db_manager.execute_query(query, values)
        messagebox.showinfo("Success", "Course added successfully!")

    def add_department(self):
        values = [entry.get() for entry in self.department_entries.values()]
        query = "INSERT INTO Departments (department_name, head_of_department_id) VALUES (%s, %s)"
        self.db_manager.execute_query(query, values)
        messagebox.showinfo("Success", "Department added successfully!")

    def display_records(self, table_name):
        query = f"SELECT * FROM {table_name}"
        records = self.db_manager.fetch_records(query)

        display_box = {
            "Students": self.student_display,
            "Courses": self.course_display,
            "Departments": self.department_display
        }.get(table_name, None)

        if display_box:
            display_box.delete("1.0", "end")
            if records:
                for record in records:
                    display_box.insert("end", f"{record}\n")
            else:
                display_box.insert("end", "No records found.\n")

def main():
    create_tables()
    app = StudentManagementSystem()
    app.mainloop()

if __name__ == "__main__":
    main()
