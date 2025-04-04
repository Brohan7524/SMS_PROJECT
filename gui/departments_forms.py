import customtkinter as ctk
from tkinter import messagebox
from core.helpers import create_form_ui, submit_form
from core.display import display_records


class DepartmentsForm(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db = db_manager
        self.entries = {}

        create_form_ui(
            frame=self,
            title="Manage Departments",
            fields={
                "Department Name": "Department Name",
                "Head of Department ID": "Head of Department ID"
            },
            submit_callback=self.add_department,
            display_callback=lambda: display_records("Departments", self.db, self),
            entries_dict=self.entries
        )

    def add_department(self):
        query = """
            INSERT INTO Departments 
            (department_name, head_of_department_id) 
            VALUES (%s, %s)
        """
        submit_form(self.db, query, self.entries, "Department added successfully!")
