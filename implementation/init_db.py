import sqlite3

from db import DB_PATH


def init_db() -> None:
    """Initialize the SQLite database with schema and demo data."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS enrollments;")
    cursor.execute("DROP TABLE IF EXISTS courses;")
    cursor.execute("DROP TABLE IF EXISTS students;")

    cursor.execute(
        """
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cohort TEXT NOT NULL,
            score REAL NOT NULL DEFAULT 0.0
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            credits INTEGER NOT NULL,
            department TEXT NOT NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            grade TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        );
        """
    )

    students_data = [
        ("Alice Smith", "A1", 85.5),
        ("Bob Johnson", "A1", 78.0),
        ("Charlie Brown", "A2", 92.0),
        ("David Wilson", "A2", 65.5),
        ("Eva Davis", "B1", 88.0),
        ("Frank Miller", "B1", 72.5),
        ("Grace Lee", "B2", 95.0),
        ("Henry Ford", "B2", 81.0),
        ("Ivy Chen", "C1", 89.5),
        ("Jack Ma", "C1", 77.0),
        ("Kelly Nguyen", "C2", 91.0),
        ("Liam Tran", "C2", 83.0),
    ]
    cursor.executemany(
        "INSERT INTO students (name, cohort, score) VALUES (?, ?, ?);",
        students_data,
    )

    courses_data = [
        ("Mathematics 101", 4, "Math"),
        ("Computer Science 50", 5, "CS"),
        ("World History", 3, "History"),
        ("Data Structures", 4, "CS"),
        ("Statistics", 4, "Math"),
        ("English Composition", 3, "English"),
        ("Physics I", 4, "Science"),
        ("Intro to Economics", 3, "Business"),
        ("Database Systems", 4, "CS"),
        ("Public Speaking", 2, "Communication"),
    ]
    cursor.executemany(
        "INSERT INTO courses (title, credits, department) VALUES (?, ?, ?);",
        courses_data,
    )

    enrollments_data = [
        (1, 1, "A"),
        (1, 2, "B"),
        (2, 1, "C"),
        (3, 2, "A"),
        (4, 3, "B"),
        (5, 1, "A"),
        (6, 4, "B"),
        (7, 5, "A"),
        (8, 6, "B"),
        (9, 7, "A"),
        (10, 8, "C"),
        (11, 9, "A"),
        (12, 10, "B"),
    ]
    cursor.executemany(
        "INSERT INTO enrollments (student_id, course_id, grade) VALUES (?, ?, ?);",
        enrollments_data,
    )

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at: {DB_PATH}")


if __name__ == "__main__":
    init_db()
