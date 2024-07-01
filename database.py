import sqlite3
import os


class GradebookDB:
    def __init__(self, db_name="gradebook.db"):
        self.db_name = os.path.join(os.getenv("LOCALAPPDATA"), "Gradebook", db_name)
        self.conn = None
        self.cursor = None
        self.initialize()

    def initialize(self):
        if not os.path.exists(self.db_name):
            self.create_database()
        else:
            self.connect()

    def create_database(self):
        try:
            os.makedirs(os.path.dirname(self.db_name), exist_ok=True)
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.init_db()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def init_db(self):
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT,
                    subjects TEXT,
                    average_score REAL
                )
                """
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")

    def fetch_all_students(self):
        try:
            self.cursor.execute("SELECT * FROM students")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching students: {e}")
            return []

    def insert_or_update_student(self, student_id, name, subjects, average_score):
        try:
            self.cursor.execute(
                "SELECT * FROM students WHERE student_id = ?", (student_id,)
            )
            result = self.cursor.fetchone()

            if result:
                # Update existing record
                existing_subjects = result[2]
                if existing_subjects:
                    existing_subjects += ", " + subjects
                else:
                    existing_subjects = subjects
                updated_average_score = (result[3] + average_score) / 2
                self.cursor.execute(
                    "UPDATE students SET name = ?, subjects = ?, average_score = ? WHERE student_id = ?",
                    (name, existing_subjects, updated_average_score, student_id),
                )
            else:
                # Insert new record
                self.cursor.execute(
                    "INSERT INTO students (student_id, name, subjects, average_score) VALUES (?, ?, ?, ?)",
                    (student_id, name, subjects, average_score),
                )

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting/updating student: {e}")

    def get_total_students(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM students")
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Error counting students: {e}")
            return 0

    def delete_student(self, student_id):
        try:
            self.cursor.execute(
                "DELETE FROM students WHERE student_id = ?", (student_id,)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting student: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
