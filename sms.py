import json
import random

students = {}

current_user = None

def save_data():
    with open("students.json", "w") as file:
        json.dump(students, file, indent=4)

def load_data():
    global students

    try:
        with open("students.json", "r") as file:
            students = json.load(file)

        # fix old data automatically
        for student_id in students:
            if "role" not in students[student_id]:
                students[student_id]["role"] = "student"

    except FileNotFoundError:
        students = {}

def register_student():
    new_student = {
        "name": input("Enter student full-name: ").capitalize(),
        "department": input("Enter student department: ").capitalize()
    }
    password = input("Create a password: ")

    # Check for duplicate student
    for student in students.values():
        if (student["name"] == new_student["name"] and student["department"] == new_student["department"]):
            print(f"{new_student['name']} is already registered in {new_student['department']} department")
            return

    # Generate unique ID
    while True:
        student_id = str(random.randint(111111, 999999))
        if student_id not in students:
            break

    students[student_id] = {
        "name": new_student["name"],
        "department": new_student["department"],
        "password" : password,
        "role" : "student",
        "courses": {}
    }
    print("\n -----Student Information-----")
    print(f"\nSTUDENT_ID: {student_id}")
    print(f"{new_student['name']} has been registered successfully in {new_student['department']} department")

    save_data()


def login():
    global current_user

    student_id = input("Enter STUDENT_ID: ")
    password = input("Enter password: ")

    if student_id in students:
        if students[student_id]["password"] == password:
            current_user = student_id

            print(f"\nWelcome {students[student_id]['name']}")

            if students[student_id]["role"] == "admin":
                print("Redirecting to Admin Dashboard...")
                admin_dashboard()

        else:
            print("Wrong password")
    else:
        print("User not found")


def admin_dashboard():
    if not current_user:
        print("You must login first")
        return

    if students[current_user]["role"] != "admin":
        print("Access denied: Admin only")
        return

    while True:
        print("\n------------- ADMIN DASHBOARD ---------------")
        print("1. View all students")
        print("2. Delete student")
        print("3. View student details")
        print("4. Logout to main menu")

        choice = input("Choose option: ")

        if choice == "1":
            view_all_students()

        elif choice == "2":
            delete_student()

        elif choice == "3":
            search_student()

        elif choice == "4":
            print("Exiting admin dashboard...")
            break

        else:
            print("Invalid option")

def view_all_students():
    if not students:
        print("No students found")
        return

    print("\n--- ALL STUDENTS ---")
    for student_id, student in students.items():
        print(f"ID: {student_id}")
        print(f"Name: {student['name']}")
        print(f"Department: {student['department']}")
        print(f"Role: {student.get('role', 'student')}")
        print("----------------------")

def search_student():
    student_id = input("Enter STUDENT_ID: ")

    if student_id in students:
        student = students[student_id]

        print("\n -----Student Found-----")
        print(f"STUDENT_ID: {student_id}\n")
        print(f"Name: {student['name']}\n")
        print(f"Department: {student['department']}")
    else:
        print("Student not found.")

def create_default_admin():
    if "000000" not in students:
        students["000000"] = {
            "name": "Admin",
            "department": "System",
            "password": "admin123",
            "role": "admin",
            "courses": {}
        }
        save_data()


def delete_student():
    student_id = input("Enter STUDENT_ID to delete: ")

    if student_id in students:
        deleted_student = students.pop(student_id)

        print(f"{deleted_student['name']} has been deleted.")
        save_data()
    else:
        print("Student does not exist.")

def add_course_score():
    if not current_user:
        print("Login required")
        return

    if students[current_user]["role"] != "student":
        print("Only students can add courses")
        return


    student_id = current_user

    course_code = input("Enter course code (e.g CSC101): ").upper()

    try:
        score = int(input("Enter score (0-100): "))

        if score < 0 or score > 100:
            print("Invalid score range")
            return

    except ValueError:
        print("Score must be a number")
        return

    students[student_id]["courses"][course_code] = score

    print(f"{course_code} added for {students[student_id]['name']}")

    save_data()

def calculate_gpa():
    if not current_user:
        print("You must login first")
        return

    student_id = current_user

    courses = students[student_id]["courses"]

    if not courses:
        print("No courses found")
        return

    total_points = 0
    total_courses = len(courses)

    for score in courses.values():
        if score >= 70:
            total_points += 5
        elif score >= 60:
            total_points += 4
        elif score >= 50:
            total_points += 3
        elif score >= 45:
            total_points += 2
        elif score >= 40:
            total_points += 1
        else:
            total_points += 0

    gpa = total_points / total_courses

    print("\n--- GPA RESULT ---")
    print(f"Name: {students[student_id]['name']}")
    print(f"GPA: {round(gpa, 2)}")

def logout():
    global current_user

    if current_user:
        print(f"{students[current_user]['name']} logged out")
        current_user = None
    else:
        print("No user is logged in")

def menu():
    print("------------ Student Management System Menu ----------")
    print("1. Register")
    print("2. Login")
    print("3. Logout")
    print("4. View students")
    print("5. Search student")
    print("6. Delete student")
    print("7. Add course score")
    print("8. Calculate GPA")
    print("0. Exit ")


load_data()
create_default_admin()


def menu():
    print("\n=========== Student Management System Menu ===========")
    print("1. Register")
    print("2. Login")
    print("3. Logout")
    print("4. View all students (Admin)")
    print("5. Search student")
    print("6. Delete student (Admin)")
    print("7. Add course score (Student)")
    print("8. Calculate GPA (Student)")
    print("0. Exit")
    print("==========================================================")


while True:
    menu()
    choice = input("Select option (0 - 8):")
    print(" ")

    if choice == "1":
        register_student()

    elif choice == "2":
        login()

    elif choice == "3":
        logout()

    elif choice == "4":
        if current_user and students[current_user]["role"] == "admin":
            view_all_students()
        else:
            print("Admin only")

    elif choice == "5":
        search_student()

    elif choice == "6":
        if current_user and students[current_user]["role"] == "admin":
            delete_student()
        else:
            print("Admin only")

    elif choice == "7":
        add_course_score()

    elif choice == "8":
        calculate_gpa()

    elif choice == "0":
        print("Exiting Program...")
        break

    else:
        print("Invalid option")

