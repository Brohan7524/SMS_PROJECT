import customtkinter as ctk
from tkinter import messagebox
from core.helpers import create_form_ui, submit_form
from core.display import display_records


class CoursesForm(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db = db_manager
        self.entries = {}

        create_form_ui(
            frame=self,
            title="Manage Courses",
            fields={
                "Course Name": "Course Name",
                "Course Code": "Course Code",
                "Credits": "Credits",
                "Department ID": "Department ID",
                "Teacher ID": "Teacher ID"
            },
            submit_callback=self.add_course,
            display_callback=lambda: display_records("Courses", self.db, self),
            entries_dict=self.entries
        )

    def add_course(self):
        query = """
            INSERT INTO Courses 
            (course_name, course_code, credits, department_id, teacher_id) 
            VALUES (%s, %s, %s, %s, %s)
        """
        submit_form(self.db, query, self.entries, "Course added successfully!")
