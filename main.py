import psycopg2
import customtkinter as ctk
from tkinter import messagebox

from tables import create_tables
from db_manager import DatabaseManager
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


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
        self.nav_frame = ctk.CTkFrame(self, height=0)
        self.nav_frame.pack(side="top", fill="x", pady=5)

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
                width=150,
            )
            button.pack(side="left", padx=25, pady=15)

        # Logout button on the right
        logout_button = ctk.CTkButton(
            self.nav_frame,
            text="Logout",
            command=self.logout,
            width=100,
        )
        logout_button.pack(side="right", padx=20, pady=10)

    def setup_frames(self):
        for name in self.nav_buttons.values():
            self.frames[name] = ctk.CTkFrame(self)
            self.frames[name].place(x=0, y=60, relwidth=1, relheight=0.9)
            home_frame = self.frames["home_frame"]
        self.create_dashboard()
        self.create_student_form()
        self.create_course_form()
        self.create_department_form()

    def show_frame(self, frame_key):
        if frame_key in self.frames:
            self.frames[frame_key].tkraise()

    def logout(self):
        self.destroy()  # Close the current application window
        import landing  # Importing the landing.py file
        landing.main() 

    def create_dashboard(self):
        frame = self.frames["home_frame"]
        ctk.CTkLabel(frame, text="College Dashboard", font=("Arial", 46)).pack(pady=40)
        ctk.CTkLabel(frame, text="Select an option from the menu above", font=("Arial", 22)).pack(pady=10)
        stats_frame = ctk.CTkFrame(frame)
        stats_frame.pack(pady=50)

        # Retrieve data counts
        student_count = self.get_count("Students")
        course_count = self.get_count("Courses")
        department_count = self.get_count("Departments")

        dashboard_items = {
            "Total Students": student_count,
            "Total Courses": course_count,
            "Total Departments": department_count,
        }

        for i, (label, count) in enumerate(dashboard_items.items()):
            item_frame = ctk.CTkFrame(stats_frame, width=300, height=250)
            item_frame.grid(row=0, column=i, padx=30, pady=20)

            ctk.CTkLabel(item_frame, text=label, font=("Arial", 20)).pack(pady=15,padx=10)
            ctk.CTkLabel(item_frame, text=str(count), font=("Arial", 32)).pack()

    def get_count(self, table_name):
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.db_manager.fetch_records(query)
        return result[0][0] if result else 0

    def create_student_form(self):
        frame = self.frames["students_frame"]
        ctk.CTkLabel(frame, text="Manage Students", font=("Arial", 24)).pack(pady=20)

        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(pady=30, anchor="center")

        self.student_entries = {
            "First Name": ctk.CTkEntry(form_frame, placeholder_text="Enter first name", justify="center"),
            "Last Name": ctk.CTkEntry(form_frame, placeholder_text="Enter last name", justify="center"),
            "DOB": ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", justify="center"),
            "Gender": ctk.CTkEntry(form_frame, placeholder_text="Male/Female/Other", justify="center"),
            "Email": ctk.CTkEntry(form_frame, placeholder_text="Enter email", justify="center"),
            "Phone": ctk.CTkEntry(form_frame, placeholder_text="Enter phone number", justify="center"),
            "Address": ctk.CTkEntry(form_frame, placeholder_text="Enter address", justify="center"),
            "Admission Date": ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", justify="center"),
            "Department ID": ctk.CTkEntry(form_frame, placeholder_text="Enter department ID", justify="center")
        }

        for row, (label, entry) in enumerate(self.student_entries.items()):
            ctk.CTkLabel(form_frame, text=f"{label} :", font=("Arial", 14), width=20, anchor="w").grid(row=row, column=0, pady=5, padx=10, sticky="w")
            entry.grid(row=row, column=1, pady=5, padx=10, sticky="ew")

        ctk.CTkButton(form_frame, text="Add Student", command=self.add_student).grid(row=len(self.student_entries), column=0, columnspan=2, pady=15)



    def add_student(self):
        values = [entry.get() for entry in self.student_entries.values()]
        query = (
            "INSERT INTO Students (first_name, last_name, dob, gender, email, phone_number, address, admission_date, department_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        self.db_manager.execute_query(query, values)
        messagebox.showinfo("Success", "Student added successfully!")

    def create_course_form(self):
        frame = self.frames["courses_frame"]
        ctk.CTkLabel(frame, text="Manage Courses", font=("Arial", 24)).pack(pady=20)

        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(pady=30, anchor="center")

        self.course_entries = {
            "Course Name": ctk.CTkEntry(form_frame, placeholder_text="Enter course name", justify="center"),
            "Course Code": ctk.CTkEntry(form_frame, placeholder_text="Enter course code", justify="center"),
            "Credits": ctk.CTkEntry(form_frame, placeholder_text="Enter credits", justify="center"),
            "Department ID": ctk.CTkEntry(form_frame, placeholder_text="Enter department ID", justify="center"),
            "Teacher ID": ctk.CTkEntry(form_frame, placeholder_text="Enter teacher ID", justify="center")
        }

        for row, (label, entry) in enumerate(self.course_entries.items()):
            ctk.CTkLabel(form_frame, text=f"{label} :", font=("Arial", 14), width=20, anchor="w").grid(row=row, column=0, pady=5, padx=10, sticky="w")
            entry.grid(row=row, column=1, pady=5, padx=10, sticky="ew")

        ctk.CTkButton(form_frame, text="Add Course", command=self.add_course).grid(row=len(self.course_entries), column=0, columnspan=2, pady=15)


    def add_course(self):
        values = [entry.get() for entry in self.course_entries.values()]
        query = "INSERT INTO Courses (course_name, course_code, credits, department_id, teacher_id) VALUES (%s, %s, %s, %s, %s)"
        self.db_manager.execute_query(query, values)
        messagebox.showinfo("Success", "Course added successfully!")

    def create_department_form(self):
        frame = self.frames["departments_frame"]
        ctk.CTkLabel(frame, text="Manage Departments", font=("Arial", 24)).pack(pady=20)

        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(pady=30, anchor="center")

        self.department_entries = {
            "Department Name": ctk.CTkEntry(form_frame, placeholder_text="Enter department name", justify="center"),
            "Head of Department ID": ctk.CTkEntry(form_frame, placeholder_text="Enter head of department ID", justify="center")
        }

        for row, (label, entry) in enumerate(self.department_entries.items()):
            ctk.CTkLabel(form_frame, text=f"{label} :", font=("Arial", 14), width=20, anchor="w").grid(row=row, column=0, pady=5, padx=10, sticky="w")
            entry.grid(row=row, column=1, pady=5, padx=10, sticky="ew")

        ctk.CTkButton(form_frame, text="Add Department", command=self.add_department).grid(row=len(self.department_entries), column=0, columnspan=2, pady=15)
        ctk.CTkButton(form_frame, text="Display Departments", command=lambda: self.display_records("Departments")).grid(row=len(self.department_entries) + 1, column=0, columnspan=2, pady=5)


    def add_department(self):
        try:
            values = [entry.get() for entry in self.department_entries.values()]
            query = "INSERT INTO Departments (department_name, head_of_department_id) VALUES (%s, %s)"
            self.db_manager.execute_query(query, values)
            messagebox.showinfo("Success", "Department added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add department: {str(e)}")



def main():
    create_tables()
    app = StudentManagementSystem()
    app.mainloop()


if __name__ == "__main__":
    main()
