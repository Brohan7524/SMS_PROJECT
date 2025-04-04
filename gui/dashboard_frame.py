# gui/dashboard_frame.py

import customtkinter as ctk

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        self.columnconfigure((0, 1, 2), weight=1)  # responsive grid
        self.rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Get counts from DB
        total_students = self.db_manager.count_records("Students")
        total_courses = self.db_manager.count_records("Courses")
        total_departments = self.db_manager.count_records("Departments")

        # Create cards
        self.create_card("📚 Students", total_students, 0)
        self.create_card("🧑‍🏫 Courses", total_courses, 1)
        self.create_card("🏢 Departments", total_departments, 2)

    def create_card(self, title, count, column):
        card = ctk.CTkFrame(self, corner_radius=15)
        card.grid(row=0, column=column, padx=20, pady=30, sticky="nsew")

        title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(20, 5))

        count_label = ctk.CTkLabel(card, text=str(count), font=ctk.CTkFont(size=36, weight="bold"))
        count_label.pack(pady=(5, 20))
