import tkinter as tk
from tkinter import ttk
import mysql.connector

class TabularGUI2(tk.Frame):
    def __init__(self, master, database_name, table_name, host="localhost", user="root", password="SCOOH@Sql"):
        super().__init__(master)
        self.master = master
        self.database_name = database_name
        self.table_name = table_name
        self.host = host
        self.user = user
        self.password = password
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Creating a frame for the data
        self.table_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Configuring the scrollbars
        vscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        vscrollbar.grid(row=0, column=1, sticky="ns")
        hscrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        hscrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.config(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

        # Fetching data from the specified table
        self.column_names, self.data = self.fetch_table_data()

        # Creating a table-like layout
        self.create_table()

        # Binding the canvas to configure the scrollbar based on content
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Ensuring that the widget expands within the tab
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_table_if_not_exist(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="SCOOH@Sql",
                database="studentdata"
            )
            cursor = conn.cursor()
            cursor.execute("""
                 ALTER TABLE students 
                    ADD COLUMN Project VARCHAR(255),
                    ADD COLUMN Course VARCHAR(255),
                    ADD COLUMN Assignment VARCHAR(255),
                    ADD COLUMN Quiz VARCHAR(255),
                    ADD COLUMN MTE VARCHAR(255),
                    ADD COLUMN ETE VARCHAR(255)
            """)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()

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
        # Creating a button to update the columns from the 4th column onwards
        update_column_button = ttk.Button(self.table_frame, text="Update Columns", command=self.update_columns_from_4th_onwards)
        update_column_button.grid(row=0, column=0, columnspan=len(self.column_names), padx=5, pady=10, sticky="w")

        # Creating labels for column names with larger fonts
        label_font = ("Helvetica", 10)
        labels = [ttk.Label(self.table_frame, text=column_name, font=label_font) for column_name in self.column_names]
        for i, label in enumerate(labels):
            label.grid(row=1, column=i, padx=5, pady=5, sticky="w")

        # Creating entry fields for attendance data with smaller fonts
        entry_font = ("Helvetica", 9)  # Decreased font size
        self.entries = []
        for i, row in enumerate(self.data):
            for j, value in enumerate(row):
                entry = ttk.Entry(self.table_frame, font=entry_font)
                entry.grid(row=i + 2, column=j, padx=5, pady=5, sticky="w")
                entry.insert(0, str(value))
                self.entries.append(entry)

        # Configuring row and column weights to expand the inner frame
        for i in range(len(self.column_names)):
            self.table_frame.columnconfigure(i, weight=1)
        self.table_frame.rowconfigure(len(self.data) + 2, weight=1)

    def update_columns_from_4th_onwards(self):
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

            # Determining the columns to update (Starting from the 4th column)
            columns_to_update = column_names[3:]

            for column in columns_to_update:
                # Iterating through the entries and update the values in the corresponding column
                for i, entry in enumerate(self.entries):
                    data = entry.get()

                    # Calculating the row and column index for the current entry
                    row_index = i // len(self.column_names)
                    col_index = i % len(self.column_names)

                    # Checking if the current entry corresponds to the column to update
                    if col_index == column_names.index(column):
                        cursor.execute(f"UPDATE {self.table_name} SET `{column}` = %s WHERE id = %s",
                                       (data, row_index + 1))

            db.commit()
            print(f"Data updated in columns from the 4th column onwards")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if db is not None and db.is_connected():
                cursor.close()
                db.close()

    def on_canvas_configure(self, event):
        # Configuring the canvas scrolling region to fit the entire table
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

def main():
    # Creating the main application window
    root = tk.Tk()
    root.title("Marks Management")

    # Creating a notebook (tabbed interface) for multiple tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="SCOOH@Sql",
            database="studentdata"
        )
        cursor = conn.cursor()
        cursor.execute("""
             ALTER TABLE students 
                ADD COLUMN Project VARCHAR(255),
                ADD COLUMN Course VARCHAR(255),
                ADD COLUMN Assignment VARCHAR(255),
                ADD COLUMN Quiz VARCHAR(255),
                ADD COLUMN MTE VARCHAR(255),
                ADD COLUMN ETE VARCHAR(255)
        """)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

    # Creating an instance of the TabularGUI class and add it as a tab
    tab_gui = TabularGUI2(notebook, "studentdata", "students")
    notebook.add(tab_gui, text="Edit Marks")

    root.mainloop()

if __name__ == "__main__":
    main()
