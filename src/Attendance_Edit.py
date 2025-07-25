import tkinter as tk
from datetime import datetime
from tkinter import ttk
import mysql.connector


class TabularGUI(tk.Frame):
    def __init__(self, master, database_name, table_name, host="your_host", user="user_name", password="your_password"):
        super().__init__(master)
        self.master = master
        self.database_name = database_name
        self.table_name = table_name
        self.host = host
        self.user = user
        self.password = password

        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vscrollbar.config(command=self.canvas.yview)
        hscrollbar.config(command=self.canvas.xview)

        self.table_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor=tk.NW)

        self.column_names, self.data = self.fetch_table_data()
        self.create_table()
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def create_column_with_current_date(self):
        try:
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name
            )
            cursor = db.cursor()
            self.table_name = "attendance"
            current_date = datetime.now().strftime("%dth %B %Y")

            cursor.execute(f"SHOW COLUMNS FROM {self.table_name} LIKE '{current_date}'")
            result = cursor.fetchone()

            if not result:
                cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN `{current_date}` VARCHAR(255)")
                db.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    def fetch_table_data(self):
        try:
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name
            )
            cursor = db.cursor()
            cursor.execute(f"SHOW COLUMNS FROM {self.table_name}")
            column_names = [row[0] for row in cursor.fetchall()]

            cursor.execute(f"SELECT * FROM {self.table_name}")
            data = cursor.fetchall()

            return column_names, data

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return [], []

        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    def create_table(self):
        table_container = ttk.Frame(self.table_frame)
        table_container.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        update_column_button = ttk.Button(table_container, text="Update Column",
                                          command=self.update_column_with_current_date)
        update_column_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        create_column_button = ttk.Button(table_container, text="Create Column with Current Date",
                                          command=self.create_column_with_current_date)
        create_column_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        label_font = ("Helvetica", 10)
        labels = [ttk.Label(table_container, text=column_name, font=label_font) for column_name in self.column_names]
        for i, label in enumerate(labels):
            label.grid(row=1, column=i, padx=5, pady=5, sticky="w")

        entry_font = ("Helvetica", 9)
        self.entries = []
        for i, row in enumerate(self.data):
            for j, value in enumerate(row):
                entry = ttk.Entry(table_container, font=entry_font)
                entry.grid(row=i + 2, column=j, padx=5, pady=5, sticky="w")
                entry.insert(0, str(value))
                self.entries.append(entry)

        table_container.columnconfigure(0, weight=1)
        table_container.columnconfigure(1, weight=1)
        table_container.rowconfigure(len(self.data) + 2, weight=1)

    def update_column_with_current_date(self):
        try:
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name
            )
            cursor = db.cursor()
            current_date = datetime.now().strftime("%dth %B %Y")

            cursor.execute(f"SHOW COLUMNS FROM {self.table_name} LIKE '{current_date}'")
            result = cursor.fetchone()

            if not result:
                cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN `{current_date}` VARCHAR(255)")
                db.commit()

            for i, entry in enumerate(self.entries):
                data = entry.get()
                row_index = i // len(self.column_names)

                cursor.execute(f"UPDATE {self.table_name} SET `{current_date}` = %s WHERE id = %s",
                               (data, row_index + 1))

            db.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def main():
    user_name = tk.Tk()
    user_name.title("Attendance Management")

    notebook = ttk.Notebook(user_name)
    notebook.pack(fill=tk.BOTH, expand=True)

    tab_gui = TabularGUI(notebook, "your_database_name", "attendance")
    notebook.add(tab_gui, text="Add Attendance")

    tab_gui.pack(fill=tk.BOTH, expand=True)

    user_name.mainloop()


if __name__ == "__main__":
    main()
