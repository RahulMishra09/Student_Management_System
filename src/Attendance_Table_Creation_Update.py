import mysql.connector


def import_data():
    conn = mysql.connector.connect(
        host="your_host",
        user="user_name",
        password="your_password",
        database="your_database_name"
    )
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        ID INT AUTO_INCREMENT PRIMARY KEY,
                        Name VARCHAR(255),
                        Registration_No VARCHAR(255)
                    )''')

    cursor.execute('SELECT id, Name, Registration_No FROM students')
    data_to_insert = cursor.fetchall()

    if data_to_insert:
        for row in data_to_insert:
            cursor.execute('''INSERT INTO attendance (ID, Name, Registration_No)
                              VALUES (%s, %s, %s)
                              ON DUPLICATE KEY UPDATE
                              ID = VALUES(ID),
                              Name = VALUES(Name),
                              Registration_No = VALUES(Registration_No)''', row)

        conn.commit()

    conn.close()


import_data()
