def add_student(students):
    name = input("Enter student name: ").strip()
    # Check if student already exists (case insensitive)
    for student in students:
        if student['name'].lower() == name.lower():
            print(f"Student with name {name} already exists")
            return
    # Create new student dictionary with empty grades list
    new_student = {
        "name": name,
        "grades": []
    }
    students.append(new_student)
    print(f"Student {name} added successfully")

def add_student_grades(students):
    # Check if there are any students
    if not students:
        print("No students available. Please add a student first.")
        return
    name = input("Enter student name: ").strip()
    # Search for student by name (case insensitive)
    for student in students:
        if student['name'].lower() == name.lower():
            # Loop for continuous grade input until 'done'
            while True:
                grade_str = input("Enter a grade (or 'done' to finish): ").strip().lower()
                if grade_str == 'done':
                    return
                try:
                    grade = int(grade_str)
                    # Validate grade is within acceptable range
                    if 0 <= grade <= 100:
                        student['grades'].append(grade)
                    else:
                        print("Invalid input, grade must be between 0 and 100.")
                except ValueError:
                    print("Invalid input, please enter an integer.")
    # Student not found message
    print(f"Student with name {name} is not found")

def show_report(students):
    print("--- Student Report ---")
    # Check if there are students to report on
    if not students:
        print("No students to show report. Please add a student first.")
        return
    # Initialize variables for statistics
    max_average = -1
    min_average = 101
    overall_average = 0
    students_with_grades = 0
    # Process each student
    for student in students:
        student_average = 0
        try:
            # Calculate student's average grade
            for grade in student['grades']:
                student_average += grade
            student_average /= len(student['grades'])
            print(f"{student['name']}'s average grade is {student_average:.1f}")
            # Update overall statistics
            overall_average += student_average
            students_with_grades += 1
            # Update max and min averages
            if max_average < student_average:
                max_average = student_average
            if min_average > student_average:
                min_average = student_average
        except ZeroDivisionError:
            # Handle case where student has no grades
            print(f"{student['name']}'s average grade is N/A")
    # Display overall statistics if there are students with grades
    if students_with_grades:
        overall_average /= students_with_grades
        print(f"----------------\nMax Average: {max_average:.1f}\nMin Average: {min_average:.1f}\nOverall Average: {overall_average:.1f}")
    else:
        print("No students with grades to show report. Please add grades first.")
        

def find_top_performer(students):
    # Check if there are any students
    if not students:
        print("No students to show top performer. Please add a student first.")
        return
    # Filter students who have grades
    students_with_grades = [student for student in students if student['grades']]
    if not students_with_grades:
        print("No students with grades available.")
        return
    # Find student with highest average grade
    top_student = max(students_with_grades, key=lambda student: sum(student['grades']) / len(student['grades']))
    average = sum(top_student['grades']) / len(top_student['grades'])
    print(f"The student with the highest average is {top_student['name']} with a grade of {average:.1f}")

def menu():
    students = []
    # Main program loop
    while True:
        print("\n--- Student Grade Analyzer ---\n1. Add a new student\n2. Add grades for a student\n3. Generate a full report\n4. Find the top student\n5. Exit program")
        try:
            choice = int(input("Enter your choice: ").strip())
            # Handle user's menu choice
            if 1 <= choice <= 5:
                match choice:
                    case 1:
                        add_student(students)
                    case 2:
                        add_student_grades(students)
                    case 3:
                        show_report(students)
                    case 4:
                        find_top_performer(students)
                    case 5:
                        print("Exiting program.")
                        return
            else:
                print("Invalid input, please enter a number from 1 to 5")
        except ValueError:
            print("Invalid input, please enter a number")

# Program entry point
if __name__ == "__main__":
    menu()