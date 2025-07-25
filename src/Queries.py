import tkinter as tk
from tkinter import ttk
import mysql.connector


class DatabaseViewer3:
    def __init__(self, tab_control):
        self.tab_control = tab_control
        self.data_frame = None
        self.canvas = None
        self.queries = {
            "The average total marks for students with Grade A": "SELECT AVG(Total) AS 'Average Total Marks for Grade A' FROM students WHERE Grades = 'A'",
            "Count of students for each grade, ordered by the grade in descending order": "SELECT Grades, COUNT(*) AS 'Number of Students' FROM students GROUP BY Grades ORDER BY Grades DESC",
            "Student details ordered by their name in ascending order": "SELECT * FROM students ORDER BY Name ASC",
            "Students with Grade A": "SELECT * FROM students WHERE Grades='A'",
            "Students who scored above 32 in ETE": "SELECT * FROM students WHERE ETE > 32",
            "Top 5 students with the highest total marks, along with their grades, ordered by total marks in descending order": "SELECT Name, Grades, Total FROM students ORDER BY Total DESC LIMIT 5",
            "Maximum and minimum total marks scored by students": "SELECT MAX(Total) AS 'Maximum Total Marks', MIN(Total) AS 'Minimum Total Marks' FROM students",
            "Student details whose name starts with 'A'": "SELECT * FROM students WHERE Name LIKE 'A%'",
            "Student details whose name contains 'oh'": "SELECT * FROM students WHERE Name LIKE '%oh%'",
            "Student details whose name ends with 'a'": "SELECT * FROM students WHERE Name LIKE '%a';",
            "Sum of total marks for students with Grade B": "SELECT SUM(Total) AS 'Total Marks for Grade B' FROM students WHERE Grades = 'B'",
            "Average marks scored in each category (Project, Course, Assignment, Quiz, MTE, ETE) for students with Grade A": "SELECT AVG(Project) AS 'Avg Project Marks', AVG(Course) AS 'Avg Course Marks', AVG(Assignment) AS 'Avg Assignment Marks', AVG(Quiz) AS 'Avg Quiz Marks', AVG(MTE) AS 'Avg MTE Marks', AVG(ETE) AS 'Avg ETE Marks' FROM students WHERE Grades = 'A'",
            "Count of students whose total marks fall within different ranges (0-50, 51-70, 71-80, 81-100)": "SELECT COUNT(CASE WHEN Total BETWEEN 0 AND 50 THEN 1 END) AS '0-50 Marks', COUNT(CASE WHEN Total BETWEEN 51 AND 70 THEN 1 END) AS '51-70 Marks', COUNT(CASE WHEN Total BETWEEN 71 AND 80 THEN 1 END) AS '71-80 Marks', COUNT(CASE WHEN Total BETWEEN 81 AND 100 THEN 1 END) AS '81-100 Marks' FROM students",
            "Student details who have attended the class on 03th November 2023 and have total marks greater than 70, ordered by their total marks in descending order": "SELECT s.* FROM students s INNER JOIN attendance a ON s.Registration_no = a.Registration_no WHERE a.`03th November 2023` IS NOT NULL AND s.Total > 70 ORDER BY s.Total DESC"
        }

    def create_data_frame(self, tab):
        self.canvas = tk.Canvas(tab)
        self.canvas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.data_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.data_frame, anchor="nw")

        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        v_scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.canvas.yview)
        v_scrollbar.grid(row=1, column=1, sticky="ns")
        h_scrollbar = ttk.Scrollbar(tab, orient="horizontal", command=self.canvas.xview)
        h_scrollbar.grid(row=2, column=0, sticky="ew")
        self.canvas.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    def display_data(self, query_name):
        if self.data_frame:
            for widget in self.data_frame.winfo_children():
                widget.destroy()
        else:
            return

        try:
            conn = mysql.connector.connect(
                host="your_host",
                user="user_name",
                password="your_password",
                database="your_database_name"
            )

            cursor = conn.cursor()
            query = self.queries.get(query_name)
            if query:
                cursor.execute(query)
                data = cursor.fetchall()
                column_names = cursor.column_names
                label_font = ("Helvetica", 10)
                for i, col_name in enumerate(column_names):
                    label = ttk.Label(self.data_frame, text=col_name, font=label_font)
                    label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

                entry_font = ("Helvetica", 9)
                for row_index, row_data in enumerate(data):
                    for col_index, cell_value in enumerate(row_data):
                        entry = ttk.Entry(self.data_frame, font=entry_font)
                        entry.insert(0, str(cell_value))
                        entry.grid(row=row_index + 1, column=col_index, padx=5, pady=5, sticky="w")

                self.data_frame.update_idletasks()
                self.canvas.config(scrollregion=self.canvas.bbox("all"))

            conn.close()
        except mysql.connector.Error as e:
            print(f"Error: {e}")


def create_query_frame(tab, viewer):
    query_frame = tk.Frame(tab, highlightbackground="black", highlightthickness=1)
    query_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    selected_query = tk.StringVar()
    for row, query_name in enumerate(viewer.queries):
        radio_button = ttk.Radiobutton(query_frame, text=query_name, variable=selected_query, value=query_name,
                                       command=lambda name=query_name: viewer.display_data(name))
        radio_button.grid(row=row, column=0, pady=5, padx=5, sticky="ew")


def main():
    user_name = tk.Tk()
    user_name.title("Database Viewer")

    tab_control = ttk.Notebook(user_name)
    tab_control.pack(expand=True, fill=tk.BOTH)

    viewer = DatabaseViewer3(tab_control)

    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text="Queries")

    create_query_frame(tab, viewer)
    viewer.create_data_frame(tab)

    user_name.mainloop()


if __name__ == "__main__":
    main()
