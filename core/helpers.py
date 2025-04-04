import customtkinter as ctk
from tkinter import messagebox

def create_form_ui(frame, title, fields, submit_callback, display_callback, entries_dict):
    ctk.CTkLabel(frame, text=title, font=("Arial", 24)).pack(pady=20)
    form_frame = ctk.CTkFrame(frame)
    form_frame.pack(pady=30, anchor="center")

    for i, (key, placeholder) in enumerate(fields.items()):
        entry = ctk.CTkEntry(form_frame, placeholder_text=placeholder, justify="center")
        entry.grid(row=i, column=0, pady=5, padx=20, sticky="ew")
        entries_dict[key] = entry

    ctk.CTkButton(form_frame, text="Submit", command=submit_callback).grid(row=len(fields), column=0, pady=10)
    ctk.CTkButton(form_frame, text="Display Records", command=display_callback).grid(row=len(fields)+1, column=0, pady=5)


def submit_form(db_manager, query, entries, success_msg):
    values = [entry.get() for entry in entries.values()]
    db_manager.execute_query(query, values)
    messagebox.showinfo("Success", success_msg)
