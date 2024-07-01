Here's a structured README file for your Student Gradebook project, adhering to best practices in software engineering:

---

# Student Gradebook Application

![Gradebook Logo](logos/logo1.png)

## Overview

The Student Gradebook Application is a desktop application built in Python using TkinterBootstrap and SQLite for managing student records, calculating average scores, exporting data to CSV, visualizing grade distributions, and generating PDF reports.

## Features

- **Dashboard Interface**: Add and Manage student names, IDs, subjects, and grades.
- **Data Management**: Import/export student data via CSV files.
- **Visualization**: Display grade distribution graphs.
- **Reporting**: Generate PDF reports summarizing student data.

## Installation

### Prerequisites

- Python 3.9+
- Ensure required Python packages are installed (`ttkbootstrap`, `matplotlib`, `reportlab`).

### Setup

1. Fork or Clone the repository:

   ```bash
   git clone https://github.com/george-mountain/student-gradebook-desktop-application.git
   cd gradebook
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python main.py
   ```

## Usage

1. **Adding Students**: Enter student details and click "Submit" to save to the database.
2. **Export/Import**: Use buttons to export data to CSV or import from CSV files.
3. **Visualization**: Click "Graphical Analysis" to view grade distribution charts.
4. **Reporting**: Generate PDF reports with student details.

## File Structure

- **`main.py`**: Main application file initializing the GUI and database.
- **`ui_components.py`**: Defines GUI components using TkinterBootstrap.
- **`database.py`**: Handles SQLite database operations for student data.
- **`gradebook_installer.iss`**: Inno Setup script for Windows installation.
