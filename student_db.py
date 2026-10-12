import sqlite3
import os
import sys

# Database Initialization
DB_NAME = "student_records.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_no INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            marks REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_student():
    print("\n--- ADD NEW STUDENT ---")
    try:
        roll_no = int(input("Enter Roll Number: "))
        name = input("Enter Student Name: ").strip()
        course = input("Enter Course/Department: ").strip()
        marks = float(input("Enter Marks (0-100): "))

        if not name or not course:
            print("[ERROR] Name and Course cannot be empty.")
            return
        if marks < 0 or marks > 100:
            print("[ERROR] Marks must be between 0 and 100.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (roll_no, name, course, marks) VALUES (?, ?, ?, ?)",
                       (roll_no, name, course, marks))
        conn.commit()
        conn.close()
        print(f"[SUCCESS] Student record for Roll No: {roll_no} added successfully!")
    except sqlite3.IntegrityError:
        print(f"[ERROR] Student with Roll No {roll_no} already exists.")
    except ValueError:
        print("[ERROR] Invalid input type. Roll number must be an integer and marks a float.")

def view_all_students():
    print("\n--- ALL STUDENT RECORDS ---")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    conn.close()

    if not records:
        print("[INFO] No student records found in database.")
        return

    print("-" * 65)
    print(f"{'Roll No':<10} | {'Name':<20} | {'Course':<15} | {'Marks':<10}")
    print("-" * 65)
    for row in records:
        print(f"{row[0]:<10} | {row[1]:<20} | {row[2]:<15} | {row[3]:<10.2f}")
    print("-" * 65)

def search_student():
    print("\n--- SEARCH STUDENT ---")
    try:
        roll_no = int(input("Enter Roll Number to Search: "))
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
        row = cursor.fetchone()
        conn.close()

        if row:
            print("\n[RECORD FOUND]")
            print(f"Roll No : {row[0]}")
            print(f"Name    : {row[1]}")
            print(f"Course  : {row[2]}")
            print(f"Marks   : {row[3]}")
        else:
            print(f"[ERROR] No record found for Roll No: {roll_no}")
    except ValueError:
        print("[ERROR] Please enter a valid integer Roll Number.")

def update_student():
    print("\n--- UPDATE STUDENT RECORD ---")
    try:
        roll_no = int(input("Enter Roll Number of Student to Update: "))
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
        row = cursor.fetchone()

        if not row:
            print(f"[ERROR] No record found for Roll No: {roll_no}")
            conn.close()
            return

        print(f"Current Data: Name={row[1]}, Course={row[2]}, Marks={row[3]}")
        new_name = input("Enter New Name (Press Enter to keep current): ").strip()
        new_course = input("Enter New Course (Press Enter to keep current): ").strip()
        new_marks_str = input("Enter New Marks (Press Enter to keep current): ").strip()

        updated_name = new_name if new_name else row[1]
        updated_course = new_course if new_course else row[2]
        updated_marks = float(new_marks_str) if new_marks_str else row[3]

        cursor.execute('''
            UPDATE students 
            SET name = ?, course = ?, marks = ? 
            WHERE roll_no = ?
        ''', (updated_name, updated_course, updated_marks, roll_no))
        conn.commit()
        conn.close()
        print(f"[SUCCESS] Record for Roll No {roll_no} updated successfully!")
    except ValueError:
        print("[ERROR] Invalid numeric input provided for marks.")

def delete_student():
    print("\n--- DELETE STUDENT RECORD ---")
    try:
        roll_no = int(input("Enter Roll Number to Delete: "))
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
        if not cursor.fetchone():
            print(f"[ERROR] No record found for Roll No: {roll_no}")
            conn.close()
            return

        confirm = input(f"Are you sure you want to delete Roll No {roll_no}? (y/n): ").strip().lower()
        if confirm == 'y':
            cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
            conn.commit()
            print(f"[SUCCESS] Record for Roll No {roll_no} deleted.")
        else:
            print("[CANCELLED] Delete operation aborted.")
        conn.close()
    except ValueError:
        print("[ERROR] Please enter a valid integer Roll Number.")

def main_menu():
    connect_db()
    while True:
        print("\n==========================================")
        print("  STUDENT DATABASE MANAGEMENT SYSTEM")
        print("==========================================")
        print("1. Add Student Record")
        print("2. View All Student Records")
        print("3. Search Student Record")
        print("4. Update Student Record")
        print("5. Delete Student Record")
        print("6. Exit")
        print("==========================================")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            view_all_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            print("\nExiting Student Database Management System. Goodbye!")
            sys.exit()
        else:
            print("[ERROR] Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main_menu()
with sqlite3.connect("student_records.db") as conn:
    cursor = conn.cursor()
    cursor.execute(''' UPDATE students SET... ''')
    # Auto-commits and closes when the block ends