from db import connect_db  # Fixed import

def create_tables():
    conn = connect_db()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Teachers (
            teacher_id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Departments (
            department_id SERIAL PRIMARY KEY,
            department_name TEXT UNIQUE NOT NULL,
            head_of_department_id INT UNIQUE REFERENCES Teachers(teacher_id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS Students (
            student_id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob DATE NOT NULL,
            gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT UNIQUE NOT NULL,
            address TEXT,
            admission_date DATE DEFAULT CURRENT_DATE,
            department_id INT REFERENCES Departments(department_id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS Courses (
            course_id SERIAL PRIMARY KEY,
            course_name TEXT NOT NULL,
            course_code TEXT UNIQUE NOT NULL,
            credits INT NOT NULL CHECK (credits > 0),
            department_id INT REFERENCES Departments(department_id) ON DELETE CASCADE,
            teacher_id INT REFERENCES Teachers(teacher_id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS Enrollments (
            enrollment_id SERIAL PRIMARY KEY,
            student_id INT REFERENCES Students(student_id) ON DELETE CASCADE,
            course_id INT REFERENCES Courses(course_id) ON DELETE CASCADE,
            enrollment_date DATE DEFAULT CURRENT_DATE,
            grade TEXT CHECK (grade IN ('A', 'B', 'C', 'D', 'F', NULL)),
            UNIQUE (student_id, course_id)
        );

        CREATE TABLE IF NOT EXISTS Attendance (
            attendance_id SERIAL PRIMARY KEY,
            student_id INT REFERENCES Students(student_id) ON DELETE CASCADE,
            course_id INT REFERENCES Courses(course_id) ON DELETE CASCADE,
            date DATE NOT NULL,
            status TEXT CHECK (status IN ('Present', 'Absent', 'Late')),
            UNIQUE (student_id, course_id, date)
        );
        ''')

        conn.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
    finally:
        conn.close()
