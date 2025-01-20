import tkinter as tk
from datetime import datetime
from tkinter import ttk
import mysql.connector

class TabularGUI(tk.Frame):
    def __init__(self, master, database_name, table_name, host="localhost", user="root", password="SCOOH@Sql"):
        super().__init__(master)
        self.master = master
        self.database_name = database_name
        self.table_name = table_name
        self.host = host
        self.user = user
        self.password = password

        # Adding vertical scrollbar
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Adding horizontal scrollbar
        hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Creating a canvas with the scrollbars
        self.canvas = tk.Canvas(self, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configuring the scrollbars
        vscrollbar.config(command=self.canvas.yview)
        hscrollbar.config(command=self.canvas.xview)

        # Creating a frame inside the canvas for the table
        self.table_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor=tk.NW)

        # Fetching data from the specified table
        self.column_names, self.data = self.fetch_table_data()

        # Creating a table-like layout
        self.create_table()

        # Binding the canvas to configure the scrollbar based on content
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def create_column_with_current_date(self):
        try:
            # Connecting to the MySQL database
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name
            )

            cursor = db.cursor()

            self.table_name = "attendance"

            # Current date as the column name in the format "28th September 2023"
            current_date = datetime.now().strftime("%dth %B %Y")

            # Checking if the column already exists
            cursor.execute(f"SHOW COLUMNS FROM {self.table_name} LIKE '{current_date}'")
            result = cursor.fetchone()

            if result:
                print(f"Column '{current_date}' already exists.")
            else:
                # Adding a new column to the table
                cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN `{current_date}` VARCHAR(255)")
                db.commit()
                print(f"Column '{current_date}' added successfully.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    def fetch_table_data(self):
        try:
            # Connecting to the MySQL database
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name
            )

            cursor = db.cursor()

            # Fetching column names
            cursor.execute(f"SHOW COLUMNS FROM {self.table_name}")
            column_names = [row[0] for row in cursor.fetchall()]

            # Fetching data
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
        # Creating a single frame to hold buttons, labels, and entry fields
        table_container = ttk.Frame(self.table_frame)
        table_container.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Creating buttons within the container frame
        update_column_button = ttk.Button(table_container, text="Update Column",
                                          command=self.update_column_with_current_date)
        update_column_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        create_column_button = ttk.Button(table_container, text="Create Column with Current Date",
                                          command=self.create_column_with_current_date)
        create_column_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Creating labels for column names with larger fonts
        label_font = ("Helvetica", 10)
        labels = [ttk.Label(table_container, text=column_name, font=label_font) for column_name in self.column_names]
        for i, label in enumerate(labels):
            label.grid(row=1, column=i, padx=5, pady=5, sticky="w")  # Row 1 for labels

        # Creating entry fields for attendance data with smaller fonts
        entry_font = ("Helvetica", 9)  # Decreased font size
        self.entries = []
        for i, row in enumerate(self.data):
            for j, value in enumerate(row):
                entry = ttk.Entry(table_container, font=entry_font)
                entry.grid(row=i + 2, column=j, padx=5, pady=5, sticky="w")
                entry.insert(0, str(value))
                self.entries.append(entry)

        # Configuring row and column weights to expand the container frame
        table_container.columnconfigure(0, weight=1)
        table_container.columnconfigure(1, weight=1)
        table_container.rowconfigure(len(self.data) + 2, weight=1)

    def update_column_with_current_date(self):
        try:
            # Connecting to the MySQL database
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name
            )

            cursor = db.cursor()

            # Getting the current date as the column name
            current_date = datetime.now().strftime("%dth %B %Y")

            # Checking if the column already exists
            cursor.execute(f"SHOW COLUMNS FROM {self.table_name} LIKE '{current_date}'")
            result = cursor.fetchone()

            if result:
                print(f"Column '{current_date}' already exists.")
            else:
                # Adding a new column to the table
                cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN `{current_date}` VARCHAR(255)")
                db.commit()
                print(f"Column '{current_date}' added successfully.")

            # Iterating through the entries and update the values in the corresponding column
            row_count = len(self.data)
            for i, entry in enumerate(self.entries):
                data = entry.get()

                # Calculating the row and column index for the current entry
                row_index = i // len(self.column_names)
                col_index = i % len(self.column_names)

                # Updating the value in the corresponding row and column of the table
                cursor.execute(f"UPDATE {self.table_name} SET `{current_date}` = %s WHERE id = %s",
                               (data, row_index + 1))

            db.commit()
            print(f"Data updated in column '{current_date}'")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    def on_canvas_configure(self, event):
        # Configuring the canvas scrolling region to fit the content
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

def main():
    root = tk.Tk()
    root.title("Attendance Management")

    # Creating a notebook (tabbed interface) for multiple tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Creating an instance of the TabularGUI class and add it as a tab
    tab_gui = TabularGUI(notebook, "studentdata", "attendance")
    notebook.add(tab_gui, text="Add Attendance")  # Specify the tab text here

    # Adding the tab to the main window and expand it to fill
    tab_gui.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
