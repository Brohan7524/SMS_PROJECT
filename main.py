import customtkinter as ctk
from tables import create_tables
from db_manager import DatabaseManager
from gui.navigation import NavigationPanel
from gui.dashboard_frame import DashboardFrame
from gui.students_forms import StudentsForm
from gui.courses_forms import CoursesForm
from gui.departments_forms import DepartmentsForm
from core.display import display_records

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class StudentManagementSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1200x800")

        self.db_manager = DatabaseManager()
        self.frames = {}

        # Navigation
        self.nav_frame = NavigationPanel(self, self.show_frame)
        self.nav_frame.pack(side="left", fill="y")

        self.body_frame = ctk.CTkFrame(self)
        self.body_frame.pack(side="right", fill="both", expand=True)

        self.setup_frames()
        self.show_frame("dashboard")

    def setup_frames(self):
        self.frames["dashboard"] = DashboardFrame(self.body_frame, self.db_manager)
        self.frames["students_frame"] = StudentsForm(self.body_frame, self.db_manager)
        self.frames["courses_frame"] = CoursesForm(self.body_frame, self.db_manager)
        self.frames["departments_frame"] = DepartmentsForm(self.body_frame, self.db_manager)

        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_frame(self, key):
        if key in self.frames:
            self.frames[key].tkraise()


if __name__ == "__main__":
    create_tables()
    app = StudentManagementSystem()
    app.mainloop()
