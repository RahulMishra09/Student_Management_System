import mysql.connector

def import_data_from_table1_to_table2():
    # Connecting to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SCOOH@Sql",
        database="studentdata"
    )

    # Creating a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Creating Table 2 (attendance) if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        ID INT AUTO_INCREMENT PRIMARY KEY,
                        Name VARCHAR(255),
                        Registration_No VARCHAR(255)
                    )''')

    # Retrieving data from Table 1 (students)
    cursor.execute('SELECT id, Name, Registration_No FROM students')
    data_to_insert = cursor.fetchall()

    if data_to_insert:
        # If there is data in Table 1, insert or update it in Table 2 (attendance)
        for row in data_to_insert:
            cursor.execute('''INSERT INTO attendance (ID, Name, Registration_No)
                              VALUES (%s, %s, %s)
                              ON DUPLICATE KEY UPDATE
                              ID = VALUES(ID),
                              Name = VALUES(Name),
                              Registration_No = VALUES(Registration_No)''', row)

        # Committing the changes to the database
        conn.commit()
        print("Data inserted/updated successfully in attendance.")
    else:
        print("No data to insert/update in attendance.")

    # Closing the database connection
    conn.close()

# Calling the function to import data from students to attendance
import_data_from_table1_to_table2()
