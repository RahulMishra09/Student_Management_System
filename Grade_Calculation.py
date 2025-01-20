import mysql.connector

def calculate_grades(score):
    # Calculating grades based on the given score
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"

def update_grades():
    try:
        # Connecting to the MySQL Database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="SCOOH@Sql",
            database="studentdata"
        )

        cursor = conn.cursor()

        table_name = "students"
        data_column = "Total"
        existing_column = "Grades"
        new_column = "Grades"

        # Checking if the 'Grades' column already exists in the table
        cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{existing_column}'")
        column_exists = cursor.fetchone()

        if column_exists:
            # Fetching data from the 'Total' column
            cursor.execute(f"SELECT id, {data_column} FROM {table_name}")
            data = cursor.fetchall()

            # Calculating and updating grades in the 'Grades' column
            for row in data:
                student_id, score = row
                grade = calculate_grades(score)

                cursor.execute(f"UPDATE {table_name} SET {existing_column} = '{grade}' WHERE id = {student_id}")
            print("Grades updated successfully.")
        else:
            # If 'Grades' column doesn't exist, create a new one
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {new_column} VARCHAR(10)")

            # Fetching data from the 'Total' column
            cursor.execute(f"SELECT id, {data_column} FROM {table_name}")
            data = cursor.fetchall()

            # Calculating and updating grades in the new 'Grades' column
            for row in data:
                student_id, score = row
                grade = calculate_grades(score)

                cursor.execute(f"UPDATE {table_name} SET {new_column} = '{grade}' WHERE id = {student_id}")

            print("Created New Column and Pushed to table")

        # Committing the changes to the database
        conn.commit()
        conn.close()
    except mysql.connector.Error as e:
        print("Error: Failed to update grades.")
    except Exception as e:
        print("Error: Failed to update grades.")

# Calling the function to update grades in the database
update_grades()
