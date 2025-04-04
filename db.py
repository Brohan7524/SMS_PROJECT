import psycopg2
import os  # Fixed: Use environment variables

def connect_db():
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "student_management_system"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "admin@1234")
              # Replace with env variable in production
        )
        print("connection successful")
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None
