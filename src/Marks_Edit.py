import tkinter as tk
from tkinter import ttk
import mysql.connector


class TabularGUI2(tk.Frame):
    def __init__(self, master, database_name, table_name, host="your_host", user="user_name", password="your_password"):
        super().__init__(master)
        self.master = master
        self.database_name = database_name
        self.table_name = table_name
        self.host = host
        self.user = user
        self.password = password
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.table_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        vscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        vscrollbar.grid(row=0, column=1, sticky="ns")
        hscrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        hscrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.config(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

        self.column_names, self.data = self.fetch_table_data()
        self.create_table()
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_table_if_not_exist(self):
        try:
            conn = mysql.connector.connect(
                host="your_host",
                user="user_name",
                password="your_password",
                database="your_database_name"
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
        update_column_button = ttk.Button(self.table_frame, text="Update Columns",
                                          command=self.update_columns_from_4th_onwards)
        update_column_button.grid(row=0, column=0, columnspan=len(self.column_names), padx=5, pady=10, sticky="w")

        label_font = ("Helvetica", 10)
        labels = [ttk.Label(self.table_frame, text=column_name, font=label_font) for column_name in self.column_names]
        for i, label in enumerate(labels):
            label.grid(row=1, column=i, padx=5, pady=5, sticky="w")

        entry_font = ("Helvetica", 9)
        self.entries = []
        for i, row in enumerate(self.data):
            for j, value in enumerate(row):
                entry = ttk.Entry(self.table_frame, font=entry_font)
                entry.grid(row=i + 2, column=j, padx=5, pady=5, sticky="w")
                entry.insert(0, str(value))
                self.entries.append(entry)

        for i in range(len(self.column_names)):
            self.table_frame.columnconfigure(i, weight=1)
        self.table_frame.rowconfigure(len(self.data) + 2, weight=1)

    def update_columns_from_4th_onwards(self):
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

            columns_to_update = column_names[3:]

            for column in columns_to_update:
                for i, entry in enumerate(self.entries):
                    data = entry.get()
                    row_index = i // len(self.column_names)
                    col_index = i % len(self.column_names)

                    if col_index == column_names.index(column):
                        cursor.execute(f"UPDATE {self.table_name} SET `{column}` = %s WHERE id = %s",
                                       (data, row_index + 1))

            db.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if db is not None and db.is_connected():
                cursor.close()
                db.close()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def main():
    user_name = tk.Tk()
    user_name.title("Marks Management")

    notebook = ttk.Notebook(user_name)
    notebook.pack(fill=tk.BOTH, expand=True)

    try:
        conn = mysql.connector.connect(
            host="your_host",
            user="user_name",
            password="your_password",
            database="your_database_name"
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

    tab_gui = TabularGUI2(notebook, "your_database_name", "students")
    notebook.add(tab_gui, text="Edit Marks")

    user_name.mainloop()


if __name__ == "__main__":
    main()
