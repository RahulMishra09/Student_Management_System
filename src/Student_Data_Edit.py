import tkinter as tk
from tkinter import ttk
import mysql.connector


class your_database_nameGUI:
    def __init__(self, tab_control, db_name="your_database_name"):
        self.tab_control = tab_control
        self.db_name = db_name
        self.create_database()
        self.create_table()
        self.create_main_frame()
        self.fetch_data()

    def create_database(self):
        try:
            conn = mysql.connector.connect(
                host="your_host",
                user="user_name",
                password="your_password"
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            conn.commit()
            conn.close()
        except mysql.connector.Error as e:
            print(f"Error creating database: {e}")

    def create_table(self):
        try:
            conn = mysql.connector.connect(
                host="your_host",
                user="user_name",
                password="your_password",
                database="your_database_name"
            )
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    Name VARCHAR(255),
                    Registration_no VARCHAR(255)
                )
            """)
            conn.commit()
            conn.close()
        except mysql.connector.Error as e:
            print(f"Error creating table: {e}")

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.tab_control)
        self.tab_control.add(self.main_frame, text="Add Student Data")

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        sub_frame = ttk.Frame(self.main_frame)
        sub_frame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        name_label = ttk.Label(sub_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.name_entry = ttk.Entry(sub_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        reg_no_label = ttk.Label(sub_frame, text="Reg No:")
        reg_no_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.reg_no_entry = ttk.Entry(sub_frame)
        self.reg_no_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        add_button = ttk.Button(sub_frame, text="Add Name & Reg No", command=self.add_data)
        add_button.grid(row=0, column=4, columnspan=2, padx=5, pady=5, sticky="w")

        canvas = tk.Canvas(self.main_frame)
        canvas.grid(row=1, column=0, columnspan=5, sticky="nsew")

        self.data_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.data_frame, anchor="nw")

        vsb = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        vsb.grid(row=1, column=5, sticky="ns")
        canvas.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.main_frame, orient="horizontal", command=canvas.xview)
        hsb.grid(row=2, column=0, columnspan=5, sticky="ew")
        canvas.configure(xscrollcommand=hsb.set)

        self.data_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

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

            label_font = ("Helvetica", 10)
            column_names = cursor.column_names
            for i, col_name in enumerate(column_names):
                label = ttk.Label(self.data_frame, text=col_name, font=label_font)
                label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

            entry_font = ("Helvetica", 9)
            for row_index, row_data in enumerate(data):
                for col_index, cell_value in enumerate(row_data):
                    entry = ttk.Entry(self.data_frame, font=entry_font)
                    entry.insert(0, str(cell_value))
                    entry.grid(row=row_index + 1, column=col_index, padx=5, pady=5, sticky="w")

            conn.close()
        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")

    def add_data(self):
        name = self.name_entry.get()
        reg_no = self.reg_no_entry.get()
        try:
            conn = mysql.connector.connect(
                host="your_host",
                user="user_name",
                password="your_password",
                database="your_database_name"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (Name, Registration_no) VALUES (%s, %s)", (name, reg_no))
            conn.commit()
            conn.close()
            self.fetch_data()
            self.name_entry.delete(0, tk.END)
            self.reg_no_entry.delete(0, tk.END)
        except mysql.connector.Error as e:
            print(f"Error adding data: {e}")


def main():
    user_name = tk.Tk()
    tab_control = ttk.Notebook(user_name)
    tab_control.pack(expand=1, fill="both")
    your_database_nameGUI(tab_control)
    user_name.mainloop()


if __name__ == "__main__":
    main()
