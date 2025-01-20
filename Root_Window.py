import tkinter as tk
from tkinter import ttk
from Projects.Student_Data_Management.Attendance_Edit import TabularGUI
from Projects.Student_Data_Management.Attendance_View import DatabaseViewer
from Projects.Student_Data_Management.Marks_Edit import TabularGUI2
from Projects.Student_Data_Management.Student_Data_Edit import StudentDataGUI
from Projects.Student_Data_Management.Student_Data_View import DatabaseViewer2
from Projects.Student_Data_Management.Attendance_Table_Creation_Update import import_data_from_table1_to_table2
from Projects.Student_Data_Management.Grade_Calculation import update_grades
from Projects.Student_Data_Management.Total_Marks_Calculation import Calculate_Total_Marks

def main():
    # Creating the main application window
    root = tk.Tk()
    root.title("Student Data Management")

    # Creating a notebook (tabbed interface) for multiple tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Adding tabs to the notebook

    # Creating attendance table and adding data from students to attendance
    import_data_from_table1_to_table2()

    # Tab 1: Edit Attendance
    tab1 = TabularGUI(notebook, "studentdata", "attendance")
    notebook.add(tab1, text="Add Attendance")

    # Tab 2: View Attendance
    # (No need to create a new instance; it's done in the module)
    db_viewer = DatabaseViewer(notebook)
    db_viewer.fetch_data()

    # Calculating Total Marks
    Calculate_Total_Marks()

    # Calculating Grades
    update_grades()

    # Tab 3: Edit Marks
    tab3 = TabularGUI2(notebook, "studentdata", "students")
    notebook.add(tab3, text="Add Marks")

    # Tab 4: Edit Student Data
    tab4 = StudentDataGUI(notebook)
    tab4.fetch_data()

    # Tab 5: View Student Data
    tab5 = DatabaseViewer2(notebook)
    tab5.fetch_data()

    # Start the main application loop
    root.mainloop()

if __name__ == "__main__":
    main()
