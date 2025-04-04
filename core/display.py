import customtkinter as ctk

def display_records(table_name, db_manager, parent_window):
    records = db_manager.fetch_all(f"SELECT * FROM {table_name}")
    win = ctk.CTkToplevel(parent_window)
    win.title(f"{table_name} Records")
    win.geometry("800x600")

    textbox = ctk.CTkTextbox(win, wrap="none", font=("Courier", 12))
    textbox.pack(expand=True, fill="both", padx=10, pady=10)

    if records:
        columns = [desc[0] for desc in db_manager.cursor.description]
        textbox.insert("end", "\t".join(columns) + "\n")
        textbox.insert("end", "-" * 100 + "\n")
        for row in records:
            textbox.insert("end", "\t".join(str(col) for col in row) + "\n")
    else:
        textbox.insert("end", f"No records found in {table_name}.")

    textbox.configure(state="disabled")
