import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation
from tkinter import *
from tkinter import filedialog
import csv
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from PIL import Image, ImageTk
import os
import sys

base_dir = getattr(sys, "_MEIPASS", os.getcwd())

logo_path = os.path.join(base_dir, "logos", "logo1.png")


class GradebookGUI(ttk.Frame):
    def __init__(self, master, db):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        self.db = db
        self.name = ttk.StringVar(value="")
        self.student_id = ttk.StringVar(value="")
        self.subjects = []  # List to hold subjects and their grades
        self.data = []
        self.colors = master.style.colors

        # Load and resize the logo image
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
        self.logo = ImageTk.PhotoImage(logo_image)

        # Create a label to display the logo
        self.logo_label = ttk.Label(self, image=self.logo)
        self.logo_label.pack(anchor=NW, padx=10, pady=10)

        instruction_text = "Students Gradebook Dashboard "
        instruction = ttk.Label(
            self, text=instruction_text, width=50, font=("Helvetica", 18)
        )
        instruction.pack(fill=X, pady=10)

        self.name_frame = ttk.Frame(self)
        self.name_frame.pack(fill=X, pady=15)
        self.create_form_entry()  # Create entry for student name and ID

        self.subject_frame = ttk.Frame(self)
        self.subject_frame.pack(fill=X, pady=15)
        self.create_subject_entry()  # Create entry for subjects and grades

        self.create_meters()  # Create meters for average score and total students
        self.create_buttonbox()  # Create buttons for exporting, importing, graphing, and printing report

        self.table = self.create_table()  # Create table to display student data
        self.load_data_from_db()  # Load data from database
        self.update_meters_from_db()  # Update meters with data from database

    def create_form_entry(self):
        self.name = ttk.StringVar(value="")
        self.student_id = ttk.StringVar(value="")

        name_container = ttk.Frame(self.name_frame)
        name_container.pack(fill=X, expand=YES, pady=15)

        student_name_label = ttk.Label(
            master=name_container,
            text="Student Name: ",
            width=15,
            font=("Helvetica", 12, "bold"),
        )
        student_name_label.pack(side=LEFT, padx=12)
        student_name_input = ttk.Entry(master=name_container, textvariable=self.name)
        student_name_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

        student_id_label = ttk.Label(
            master=name_container,
            text="Student ID: ",
            width=15,
            font=("Helvetica", 12, "bold"),
        )
        student_id_label.pack(side=LEFT, padx=12)
        student_id_input = ttk.Entry(
            master=name_container, textvariable=self.student_id
        )
        student_id_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_subject_entry(self):
        self.subject_name = ttk.StringVar(value="")
        self.subject_grade = ttk.DoubleVar(value=0)

        subject_container = ttk.Frame(self.subject_frame)
        subject_container.pack(fill=X, expand=YES, pady=15)

        subject_name_label = ttk.Label(
            master=subject_container,
            text="Subject: ",
            width=17,
            font=("Helvetica", 12, "bold"),
        )
        subject_name_label.pack(side=LEFT, padx=12)
        subject_name_input = ttk.Entry(
            master=subject_container, textvariable=self.subject_name
        )
        subject_name_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

        subject_grade_label = ttk.Label(
            master=subject_container,
            text="Grade: ",
            width=17,
            font=("Helvetica", 12, "bold"),
        )
        subject_grade_label.pack(side=LEFT, padx=12)
        subject_grade_input = ttk.Entry(
            master=subject_container, textvariable=self.subject_grade
        )
        subject_grade_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

        add_subject_btn = ttk.Button(
            master=subject_container,
            text="Add Subject",
            command=self.add_subject,
            bootstyle=PRIMARY,
        )
        add_subject_btn.pack(side=LEFT, padx=5)

    def add_subject(self):
        subject = self.subject_name.get()
        grade = self.subject_grade.get()
        if subject and grade:
            self.subjects.append((subject, grade))
            self.subject_name.set("")
            self.subject_grade.set(0)
            self.update_average_score()

    def update_average_score(self):
        if self.subjects:
            average_score = sum(grade for _, grade in self.subjects) / len(
                self.subjects
            )
            self.final_score.set(average_score)
            self.update_meters()

    def create_buttonbox(self):
        button_container = ttk.Frame(self)
        button_container.pack(fill=X, expand=YES, pady=(15, 10))

        export_btn = ttk.Button(
            master=button_container,
            text="Export Data",
            command=self.export_to_csv,
            bootstyle=INFO,
            width=10,
        )
        export_btn.pack(side=LEFT, padx=5)

        import_btn = ttk.Button(
            master=button_container,
            text="Import Data",
            command=self.import_from_csv,
            bootstyle=INFO,
            width=10,
        )
        import_btn.pack(side=LEFT, padx=5)

        graph_btn = ttk.Button(
            master=button_container,
            text="Graphical Analysis",
            command=self.show_grade_distribution,
            bootstyle=INFO,
            width=15,
        )
        graph_btn.pack(side=LEFT, padx=5)

        print_report_btn = ttk.Button(
            master=button_container,
            text="Print Report",
            command=self.print_student_report,
            bootstyle=INFO,
            width=12,
        )
        print_report_btn.pack(side=LEFT, padx=5)

        cancel_btn = ttk.Button(
            master=button_container,
            text="Cancel",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=6,
        )

        cancel_btn.pack(side=RIGHT, padx=5)

        submit_btn = ttk.Button(
            master=button_container,
            text="Submit",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )

        submit_btn.pack(side=RIGHT, padx=5)

    def create_meters(self):
        # Meter for average score
        self.meter_avg = ttk.Meter(
            master=self,
            metersize=150,
            padding=5,
            amounttotal=100,
            amountused=0,
            metertype="full",
            subtext="Average Score",
            interactive=False,
            subtextfont=("Helvetica", 13),
        )
        self.meter_avg.pack(side=LEFT, padx=10)

        self.final_score = self.meter_avg.amountusedvar

        # Meter for total number of students
        self.meter_total_students = ttk.Meter(
            master=self,
            metersize=150,
            padding=5,
            amounttotal=200,  # This can be any maximum value you prefer
            amountused=0,
            metertype="full",
            subtext="Total Students",
            interactive=False,
            subtextfont=("Helvetica", 13),
        )
        self.meter_total_students.pack(side=LEFT, padx=10)

        self.total_students_count = self.meter_total_students.amountusedvar

    def update_meters(self):
        self.meter_avg.amountusedvar.set(self.final_score.get())
        self.meter_total_students.amountusedvar.set(self.total_students_count.get())

    def update_meters_from_db(self):
        # Update average score meter
        rows = self.db.fetch_all_students()
        if rows:
            average_score = sum(row[3] for row in rows) / len(rows)
            self.final_score.set(average_score)
        else:
            self.final_score.set(0)

        # Update total students meter
        total_students = self.db.get_total_students()
        self.total_students_count.set(total_students)

        self.update_meters()

    def create_table(self):
        coldata = [
            {"text": "Name", "stretch": True},
            {"text": "Student ID", "stretch": True},
            {"text": "Subjects", "stretch": True},
            {"text": "Average Score", "stretch": True},
        ]

        table = Tableview(
            master=self,
            coldata=coldata,
            rowdata=self.data,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            stripecolor=(self.colors.light, None),
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        return table

    def load_data_from_db(self):
        self.data = []
        rows = self.db.fetch_all_students()
        for row in rows:
            self.data.append((row[1], row[0], row[2], row[3]))
        self.refresh_table()

    def refresh_table(self):
        self.table.destroy()  # Destroy the old table
        self.table = self.create_table()  # Create a new table with updated data

    def on_submit(self):
        """Print the contents to console and return the values."""
        name = self.name.get()
        student_id = self.student_id.get()
        subjects = ", ".join(f"{subject} ({grade})" for subject, grade in self.subjects)
        average_score = self.final_score.get()

        print("Name:", name)
        print("Student ID: ", student_id)
        print("Subjects:", subjects)
        print("Average Score:", average_score)

        toast = ToastNotification(
            title="Submission successful!",
            message="Your data has been successfully submitted.",
            duration=3000,
        )

        toast.show_toast()

        # Insert or update student record in database
        self.db.insert_or_update_student(student_id, name, subjects, average_score)

        # Refresh GUI
        self.subjects = []  # Clear the subjects for the next input
        self.load_data_from_db()
        self.update_meters_from_db()

    def on_cancel(self):
        """Cancel and close the application."""
        self.db.close()
        self.quit()

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Student ID", "Name", "Subjects", "Average Score"])
                for student in self.db.fetch_all_students():
                    writer.writerow(student)
            toast = ToastNotification(
                title="Export successful!",
                message="Data has been successfully exported to CSV.",
                duration=3000,
            )
            toast.show_toast()

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    student_id, name, subjects, average_score = row
                    self.db.insert_or_update_student(
                        student_id, name, subjects, float(average_score)
                    )
            self.load_data_from_db()
            self.update_meters_from_db()
            toast = ToastNotification(
                title="Import successful!",
                message="Data has been successfully imported from CSV.",
                duration=3000,
            )
            toast.show_toast()

    def show_grade_distribution(self):
        rows = self.db.fetch_all_students()
        if rows:
            grades = [float(row[3]) for row in rows]
            plt.figure(figsize=(8, 6))
            plt.hist(grades, bins=10, edgecolor="black")
            plt.xlabel("Average Score")
            plt.ylabel("Frequency")
            plt.title("Grade Distribution")
            plt.grid(True)
            plt.show()
        else:
            toast = ToastNotification(
                title="No Data",
                message="No student data available to visualize.",
                duration=3000,
            )
            toast.show_toast()

    def print_student_report(self):
        # Fetch all students from the database
        students = self.db.fetch_all_students()

        # Generate PDF report
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            c = canvas.Canvas(file_path, pagesize=letter)

            # Title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 750, "Student Report")

            # Divider line
            c.setFont("Helvetica", 12)
            c.drawString(100, 730, "-" * 50)

            y_position = 700
            best_student = None
            highest_average_score = 0
            total_students = len(students)

            # Print total number of students
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, y_position, f"Total Students: {total_students}")

            # Find the best performing student
            for student in students:
                if student[3] > highest_average_score:
                    highest_average_score = student[3]
                    best_student = student

            # Print the best performing student details
            if best_student:
                y_position -= (
                    20  # Adjust for the next section to avoid overlapping text
                )
                c.drawString(100, y_position, "Best Performing Student:")
                c.setFont("Helvetica", 12)
                c.drawString(100, y_position - 20, f"Name: {best_student[1]}")
                c.drawString(100, y_position - 40, f"Student ID: {best_student[0]}")
                c.drawString(100, y_position - 60, f"Average Score: {best_student[3]}")
                c.drawString(100, y_position - 80, "-" * 50)

            y_position -= 100  # Adjust for next section

            # Print each student's details
            for student in students:
                c.drawString(100, y_position, f"Name: {student[1]}")
                c.drawString(100, y_position - 20, f"Student ID: {student[0]}")
                c.drawString(100, y_position - 40, f"Subjects: {student[2]}")
                c.drawString(100, y_position - 60, f"Average Score: {student[3]}")
                c.drawString(100, y_position - 80, "-" * 50)
                y_position -= 100

            c.save()

            toast = ToastNotification(
                title="Print Report",
                message="Student report has been successfully generated and saved as PDF.",
                duration=3000,
            )
            toast.show_toast()
