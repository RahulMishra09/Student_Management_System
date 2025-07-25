import tkinter as tk
from tkinter import ttk
import mysql.connector

class DatabaseViewer2:
    def __init__(self, tab_control):
        self.tab_control = tab_control

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="your_host",
                user="user_name",
                password="your_password",
                database="your_database_name"
            )

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")

            data = cursor.fetchall()

            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text="View Student Data")

            canvas = tk.Canvas(tab)
            canvas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            data_frame = ttk.Frame(canvas)
            canvas.create_window((0, 0), window=data_frame, anchor="nw")

            tab.grid_rowconfigure(1, weight=1)
            tab.grid_columnconfigure(0, weight=1)

            v_scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
            v_scrollbar.grid(row=1, column=1, sticky="ns")
            h_scrollbar = ttk.Scrollbar(tab, orient="horizontal", command=canvas.xview)
            h_scrollbar.grid(row=2, column=0, sticky="ew")
            canvas.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

            column_names = cursor.column_names
            label_font = ("Helvetica", 10)
            for i, col_name in enumerate(column_names):
                label = ttk.Label(data_frame, text=col_name, font=label_font)
                label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

            entry_font = ("Helvetica", 9)
            for row_index, row_data in enumerate(data):
                for col_index, cell_value in enumerate(row_data):
                    entry = ttk.Entry(data_frame, font=entry_font)
                    entry.insert(0, str(cell_value))
                    entry.grid(row=row_index + 1, column=col_index, padx=5, pady=5, sticky="w")

            data_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

            conn.close()
        except mysql.connector.Error as e:
            print(f"Error: {e}")

def main():
    user_name = tk.Tk()
    user_name.title("Database Viewer")

    tab_control = ttk.Notebook(user_name)
    tab_control.pack(expand=True, fill=tk.BOTH)

    viewer = DatabaseViewer2(tab_control)
    viewer.fetch_data()

    user_name.mainloop()

if __name__ == "__main__":
    main()
