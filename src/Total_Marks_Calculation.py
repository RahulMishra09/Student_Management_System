import mysql.connector

def Calculate_Total_Marks():
    db_config = {
        "host": "your_host",
        "user": "user_name",
        "password": "your_password",
        "database": "your_database_name"
    }

    conn, cursor = None, None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(buffered=True)

        check_query = "SHOW COLUMNS FROM students LIKE 'Total'"
        cursor.execute(check_query)
        column_exists = cursor.fetchone()

        if not column_exists:
            add_column_query = "ALTER TABLE students ADD COLUMN Total INT"
            cursor.execute(add_column_query)

        reset_total_query = "UPDATE students SET Total = 0"
        cursor.execute(reset_total_query)

        select_query = "SELECT id, Project, Course, Assignment, Quiz, MTE, ETE FROM students"
        cursor.execute(select_query)

        for row in cursor.fetchall():
            student_id, Project, Course, Assignment, Quiz, MTE, ETE = row
            total_sum = sum(int(value) for value in row[1:]) if all(row[1:]) else 0

            update_query = "UPDATE students SET Total = %s WHERE id = %s"
            cursor.execute(update_query, (total_sum, student_id))

    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.commit()
            conn.close()

Calculate_Total_Marks()
