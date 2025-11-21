#def 1

#def 2

#def 3

#def 4

def menu():
    students = []
    while True:
        print("--- Student Grade Analyzer ---\n1. Add a new student\n2. Add grades for a student\n3. Generate a full report\n4. Find the top student\n5. Exit program")
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= 5:
                match choice:
                    case 1:
                        return "1"
                    case 2:
                        return "2"
                    case 3:
                        return "3"
                    case 4:
                        return "4"
                    case 5:
                        print("Exiting program.")
                        return
            else:
                print("Invalid input, please enter a number from 1 to 5")
        except ValueError:
            print("Invalid input, please enter a number")




if __name__ == "__main__":
    menu()