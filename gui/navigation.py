import customtkinter as ctk

class NavigationPanel(ctk.CTkFrame):
    def __init__(self, master, show_callback):
        super().__init__(master, width=150)
        self.show_callback = show_callback
        self.buttons = {
            "Home": "dashboard",
            "Students": "students_frame",
            "Courses": "courses_frame",
            "Departments": "departments_frame",
        }
        self.create_buttons()

    def create_buttons(self):
        for text, frame_key in self.buttons.items():
            ctk.CTkButton(self, text=text, command=lambda k=frame_key: self.show_callback(k)).pack(pady=5, padx=10, fill="x")
