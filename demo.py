import psycopg2
from psycopg2 import Error

USER="postgres"
PASSWORD="postgres"
HOST="localhost"
DB_NAME = "crud"
def connect_to_db():
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database="postgres"
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname='" + DB_NAME + "'")
        exists = cursor.fetchone()
        if exists:
            print("Database already exists, skipping...")
        else:
            cursor.execute("CREATE DATABASE " + DB_NAME)
            print("Database created successfully")
        cursor.close()
        connection.autocommit = False
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=DB_NAME
        )
        if not exists:
            initialize_database(connection)
        return connection
    except Error as e:
        print("Error while connecting ", e)

def get_all_students(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        print("List of Students:")
        for student in students:
            print(student)
    except Error as e:
        print("Error while fetching data ", e)
    cursor.close()

def add_student(connection, first_name, last_name, email, enrollment_date):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, email, enrollment_date))
        connection.commit()
        print("Student added successfully")
    except Error as e:
        print("Error while adding student to PostgreSQL", e)
    cursor.close()

def update_student_email(connection, student_id, new_email):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE students SET email = %s WHERE student_id = %s",
                       (new_email, student_id))
        connection.commit()
        print("Email address updated successfully")
    except Error as e:
        print("Error while updating email address ", e)
    cursor.close()

def delete_student(connection, student_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        connection.commit()
        print("Student deleted successfully")
    except Error as e:
        print("Error while deleting student ", e)
    cursor.close()

def initialize_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                enrollment_date DATE
            )
        """)
        print("Table 'students' created successfully")
        cursor.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
            ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
            ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
            ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')
        """)
        print("Initial data inserted successfully")
        connection.commit()
    except Error as e:
        print("Error while initializing database", e)
    cursor.close()

def start_crud():
    connection = connect_to_db()
    if connection:
        while True:
            print("\nChoose an operation:")
            print("1. Get all students")
            print("2. Add a student")
            print("3. Update student email")
            print("4. Delete a student")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                get_all_students(connection)
            elif choice == '2':
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                email = input("Enter email: ")
                enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
                add_student(connection, first_name, last_name, email, enrollment_date)
            elif choice == '3':
                student_id = input("Enter student ID: ")
                new_email = input("Enter new email: ")
                update_student_email(connection, student_id, new_email)
            elif choice == '4':
                student_id = input("Enter student ID: ")
                delete_student(connection, student_id)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")
            connection.commit() # Clear queue

        connection.close()

if __name__ == "__main__":
    start_crud()
