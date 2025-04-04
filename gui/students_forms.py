import customtkinter as ctk
from tkinter import messagebox
from core.helpers import create_form_ui, submit_form
from core.display import display_records


class StudentsForm(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db = db_manager
        self.entries = {}

        create_form_ui(
            self, 
            title="Manage Students",
            fields={
                "First Name": "First Name",
                "Last Name": "Last Name",
                "DOB": "YYYY-MM-DD",
                "Gender": "Male/Female/Other",
                "Email": "Email",
                "Phone": "Phone",
                "Address": "Address",
                "Admission Date": "YYYY-MM-DD",
                "Department ID": "Department ID",
            },
            submit_callback=self.add_student,
            display_callback=lambda: display_records("Students", self.db, self),
            entries_dict=self.entries
        )

    def add_student(self):
        query = """
        INSERT INTO Students 
        (first_name, last_name, dob, gender, email, phone_number, address, admission_date, department_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        submit_form(self.db, query, self.entries, "Student added successfully!")
