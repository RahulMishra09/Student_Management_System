import mysql.connector


def calculate_grades(score):
    if score is None:
        return "N/A"
    elif score >= 90:
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
        conn = mysql.connector.connect(
            host="your_host",
            user="user_name",
            password="your_password",
            database="your_database_name"
        )
        cursor = conn.cursor()

        table_name = "students"
        data_column = "Total"
        existing_column = "Grades"
        new_column = "Grades"

        cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{existing_column}'")
        column_exists = cursor.fetchone()

        if column_exists:
            cursor.execute(f"SELECT id, {data_column} FROM {table_name}")
            data = cursor.fetchall()

            for row in data:
                student_id, score = row
                grade = calculate_grades(score)
                cursor.execute(f"UPDATE {table_name} SET {existing_column} = '{grade}' WHERE id = {student_id}")
        else:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {new_column} VARCHAR(10)")
            cursor.execute(f"SELECT id, {data_column} FROM {table_name}")
            data = cursor.fetchall()

            for row in data:
                student_id, score = row
                grade = calculate_grades(score)
                cursor.execute(f"UPDATE {table_name} SET {new_column} = '{grade}' WHERE id = {student_id}")

        conn.commit()
        conn.close()
    except mysql.connector.Error as e:
        print("Error: Failed to update grades.")


update_grades()
