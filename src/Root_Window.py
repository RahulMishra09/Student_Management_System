import tkinter as tk
from tkinter import ttk
from Attendance_Edit import TabularGUI
from Attendance_View import DatabaseViewer
from Marks_Edit import TabularGUI2
from Student_Data_Edit import your_database_nameGUI
from Student_Data_View import DatabaseViewer2
from Attendance_Table_Creation_Update import import_data
from Grade_Calculation import update_grades
from Total_Marks_Calculation import Calculate_Total_Marks
from Queries import DatabaseViewer3, create_query_frame


def main():
    user_name = tk.Tk()
    user_name.title("Student Data Management")

    notebook = ttk.Notebook(user_name)
    notebook.pack(fill=tk.BOTH, expand=True)

    import_data()

    tab1 = TabularGUI(notebook, "your_database_name", "attendance")
    notebook.add(tab1, text="Add Attendance")

    db_viewer = DatabaseViewer(notebook)
    db_viewer.fetch_data()

    Calculate_Total_Marks()
    update_grades()

    tab3 = TabularGUI2(notebook, "your_database_name", "students")
    notebook.add(tab3, text="Add Marks")

    tab4 = your_database_nameGUI(notebook)
    tab4.fetch_data()

    tab5 = DatabaseViewer2(notebook)
    tab5.fetch_data()

    viewer = DatabaseViewer3(notebook)
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Queries")
    viewer.create_data_frame(tab)
    create_query_frame(tab, viewer)

    user_name.mainloop()


if __name__ == "__main__":
    main()
