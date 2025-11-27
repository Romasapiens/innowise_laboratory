"""
Student Grade Analyzer System
A program to manage student records and grade calculations.
"""

from typing import List, Dict, Optional

def add_student(students: List[Dict[str, str | List[int]]]) -> None:
    """
    Add a new student to the system.
    
    Args:
        students: List of student dictionaries containing name and grades
        
    Raises:
        None: All exceptions are handled within the function
    """
    name = input("Enter student name: ").strip()
    # Check if student already exists (case insensitive)
    for student in students:
        if student['name'].lower() == name.lower():
            print(f"Student with name {name} already exists")
            return
    
    # Create new student dictionary with empty grades list
    new_student: Dict[str, str | List[int]] = {
        "name": name,
        "grades": []
    }
    students.append(new_student)
    print(f"Student {name} added successfully")

def add_student_grades(students: List[Dict[str, str | List[int]]]) -> None:
    """
    Add grades for an existing student.
    
    Args:
        students: List of student dictionaries
        
    Notes:
        - Validates grade range (0-100)
        - Handles invalid input gracefully
        - Case-insensitive student search
    """
    # Check if there are any students
    if not students:
        print("No students available. Please add a student first.")
        return
    name = input("Enter student name: ").strip()
    student_found: Optional[Dict[str, str | List[int]]] = None
    
    # Search for student by name (case insensitive)
    for student in students:
        if student['name'].lower() == name.lower():
            student_found = student
            break
    
    if not student_found:
        print(f"Student with name '{name}' not found")
        return
    
    # Loop for continuous grade input until 'done'
    while True:
        grade_str = input("Enter a grade (0-100) or 'done' to finish: ").strip().lower()
        
        if grade_str == 'done':
            break
            
        try:
            grade: int = int(grade_str)
            # Validate grade is within acceptable range
            if 0 <= grade <= 100:
                student_found['grades'].append(grade)
                print(f"Grade {grade} added successfully.")
            else:
                print("Invalid input: Grade must be between 0 and 100.")
                
        except ValueError:
            print("Invalid input: Please enter a valid integer.")
    
    print(f"Final grades for {student_found['name']}: {student_found['grades']}")

def show_report(students: List[Dict[str, str | List[int]]]):
    """
    Generate a comprehensive report of all students' performance.
    
    Args:
        students: List of student dictionaries
        
    Calculates:
        - Individual student averages
        - Overall statistics (max, min, overall average)
        - Handles students with no grades appropriately
    """
    print("--- Student Report ---")

    # Check if there are students to report on
    if not students:
        print("No students to show report. Please add a student first.")
        return
    
    # Initialize variables for statistics
    max_average: float = -1.0
    min_average: float = 101.0
    overall_average: float = 0.0
    students_with_grades: int = 0

    # Process each student
    for student in students:
        grades: List[int] = student['grades']
        try:
            student_average: float = sum(grades) / len(grades)
            print(f"{student['name']}'s average grade is {student_average:.1f}")
            
            # Update overall statistics
            overall_average += student_average
            students_with_grades += 1
            
            # Update max and min averages
            max_average = max(max_average, student_average)
            min_average = min(min_average, student_average)
                
        except ZeroDivisionError:
            # Student has no grades
            print(f"{student['name']}'s average grade is N/A")

    if students_with_grades:
        overall_average /= students_with_grades
        print(f"----------------\nMax Average: {max_average:.1f}\nMin Average: {min_average:.1f}\nOverall Average: {overall_average:.1f}")
    else:
        print("No students with grades to show report. Please add grades first.")
        
def find_top_performer(students: List[Dict[str, str | List[int]]]):
    """
    Find and display the student with the highest average grade.
    
    Args:
        students: List of student dictionaries
        
    Notes:
        - Only considers students with grades
        - Handles ties by showing the first encountered
        - Provides clear feedback for edge cases
    """

    # Check if there are any students
    if not students:
        print("No students to show top performer. Please add a student first.")
        return
    
    # Filter students who have grades
    students_with_grades: List[Dict[str, str | List[int]]] = [
        student for student in students if student['grades']
    ]

    if not students_with_grades:
        print("No students with grades available.")
        return
    
    # Find student with highest average grade
    top_student: Dict[str, str | List[int]] = max(
        students_with_grades,
        key=lambda student: sum(student['grades']) / len(student['grades'])
    )

    average: float = sum(top_student['grades']) / len(top_student['grades'])
    print(f"The student with the highest average is {top_student['name']} with a grade of {average:.1f}")

def menu():
    """
    Main program menu and control loop.
    
    Features:
        - Continuous operation until explicit exit
        - Input validation for menu choices
        - Clear user interface
        - Proper error handling
    """
    students: List[Dict[str, str | List[int]]] = []
    # Main program loop
    while True:
        print("\n--- Student Grade Analyzer ---\n1. Add a new student\n2. Add grades for a student\n3. Generate a full report\n4. Find the top student\n5. Exit program")
        try:
            choice: int = int(input("Enter your choice: ").strip())
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