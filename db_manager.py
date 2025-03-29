from db import connect_db
import psycopg2
from tkinter import messagebox

class DatabaseManager:
    """Manages database queries and transactions."""

    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """Executes a given SQL query with optional parameters and fetch support."""
        conn = None
        try:
            conn = connect_db()
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                conn.commit()
                return True
        except psycopg2.Error as e:
            if conn:
                conn.rollback()  # Fixed: Rollback transaction on error
            messagebox.showerror("Database Error", str(e))
            return None
        finally:
            if conn:
                conn.close()

    def fetch_records(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return []