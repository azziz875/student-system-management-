class Student:
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade

    def to_file_format(self):
        return f"{self.student_id},{self.name},{self.age},{self.grade}\n"


# --- 2. Student System Class ---
class StudentSystem:
    def __init__(self, filename="students.txt"):
        self.filename = filename
        self.students = self.load_from_file()

    def load_from_file(self):
        students_list = []
        try:
            file = open(self.filename, "r")
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 4:
                        s_id, name, age, grade = parts
                        students_list.append({
                            "id": s_id,
                            "name": name,
                            "age": int(age),
                            "grade": float(grade)
                        })
            file.close()
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading file: {e}")
        return students_list

    def save_to_file(self):
        try:
            file = open(self.filename, "w")
            for s in self.students:
                line = f"{s['id']},{s['name']},{s['age']},{s['grade']}\n"
                file.write(line)
            file.close()
        except Exception as e:
            print(f"Error saving file: {e}")
    
    # 1. Add Student 
    def add_student(self):
        print("\n--- Add Student ---")
        student_id = input("Enter ID: ").strip()
        if not student_id:
            print("[!] ID cannot be empty.")
            return

        # Check if ID already exists
        for s in self.students:
            if s["id"] == student_id:
                print("[!] Error: Student ID already exists!")
                return

        name = input("Enter Name: ").strip()
        if not name:
            print("[!] Name cannot be empty.")
            return

        # Handling Age Error 
        while True:
            try:
                age = int(input("Enter Age: "))
                if age <= 0 or age > 120:
                    print("[!] Please enter a realistic age between 1 and 120.")
                    continue
                break
            except ValueError:
                print("[!] Invalid input! Age must be a whole number (e.g., 20). Try again.")

        # Handling Grade Error 
        while True:
            try:
                grade = float(input("Enter Grade: "))
                if grade < 0 or grade > 100:
                    print("[!] Please enter a grade between 0 and 100.")
                    continue
                break
            except ValueError:
                print("[!] Invalid input! Grade must be a number (e.g., 85.5). Try again.")

        # Create Student Object and save
        new_student = Student(student_id, name, age, grade)
        self.students.append(new_student.to_file_format().strip().split(",")) 

        self.students[-1] = {"id": student_id, "name": name, "age": age, "grade": grade}
        
        self.save_to_file()
        print("[✓] Student added successfully!")

    # 2. Show All Students
    def show_all_students(self):
        print("\n--- All Students ---")
        if not self.students:
            print("No students found in the system.")
            return
        
        for s in self.students:
            status = "Pass" if s['grade'] >= 50 else "Fail"
            print(f"ID: {s['id']} | Name: {s['name']} | Age: {s['age']} | Grade: {s['grade']} | Status: {status}")

    # 3. Search Student
    def search_student(self):
        print("\n--- Search Student ---")
        query = input("Enter name or ID to search: ").strip().lower()
        if not query:
            print("[!] Search query cannot be empty.")
            return
            
        found = False
        for s in self.students:
            if query in s['id'].lower() or query in s['name'].lower():
                status = "Pass" if s['grade'] >= 50 else "Fail"
                print(f"[Found] ID: {s['id']} | Name: {s['name']} | Age: {s['age']} | Grade: {s['grade']} | Status: {status}")
                found = True
                
        if not found:
            print("[!] No matching student found.")

    # 4. Pass / Fail Status
    def show_pass_fail_status(self):
        print("\n--- Pass / Fail Status ---")
        if not self.students:
            print("No students found in the system.")
            return
        
        print("\n[Passed Students]")
        passed = [s for s in self.students if s['grade'] >= 50]
        if passed:
            for s in passed:
                print(f" - ID: {s['id']} | Name: {s['name']} | Grade: {s['grade']}")
        else:
            print(" None")

        print("\n[Failed Students]")
        failed = [s for s in self.students if s['grade'] < 50]
        if failed:
            for s in failed:
                print(f" - ID: {s['id']} | Name: {s['name']} | Grade: {s['grade']}")
        else:
            print(" None")

    # 5. Update Student
    def update_student(self):
        print("\n--- Update Student ---")
        student_id = input("Enter ID of student to update: ").strip()
        
        for s in self.students:
            if s['id'] == student_id:
                print(f"Current info -> Name: {s['name']}, Age: {s['age']}, Grade: {s['grade']}")
                
                # Update Name
                new_name = input(f"Enter new name (or press Enter to keep): ").strip()
                if new_name:
                    s['name'] = new_name

                # Update Age 
                new_age_str = input(f"Enter new age (or press Enter to keep): ").strip()
                if new_age_str:
                    try:
                        new_age = int(new_age_str)
                        if 0 < new_age <= 120:
                            s['age'] = new_age
                        else:
                            print("[!] Invalid age range, age was not updated.")
                    except ValueError:
                        print("[!] Invalid age format, age was not updated.")

                # Update Grade 
                new_grade_str = input(f"Enter new grade (or press Enter to keep): ").strip()
                if new_grade_str:
                    try:
                        new_grade = float(new_grade_str)
                        if 0 <= new_grade <= 100:
                            s['grade'] = new_grade
                        else:
                            print("[!] Invalid grade range, grade was not updated.")
                    except ValueError:
                        print("[!] Invalid grade format, grade was not updated.")

                self.save_to_file()
                print("[✓] Student updated successfully!")
                return
                    
        print("[!] Student ID not found.")

    # 6. Delete Student
    def delete_student(self):
        print("\n--- Delete Student ---")
        student_id = input("Enter ID of student to delete: ").strip()
        
        for s in self.students:
            if s['id'] == student_id:
                self.students.remove(s)
                self.save_to_file()
                print("[✓] Student deleted successfully!")
                return
                
        print("[!] Student ID not found.")

    # 7. Show Statistics
    def show_statistics(self):
        print("\n--- Show Statistics ---")
        if not self.students:
            print("No data available to calculate statistics.")
            return
            
        total_students = len(self.students)
        total_grades = sum(s['grade'] for s in self.students)
        avg_grade = total_grades / total_students
        highest_grade = max(s['grade'] for s in self.students)
        passed_count = sum(1 for s in self.students if s['grade'] >= 50)
        failed_count = total_students - passed_count
        
        print(f"Total Students: {total_students}")
        print(f"Average Grade: {avg_grade:.1f}")
        print(f"Highest Grade: {highest_grade}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")

def main():
    system = StudentSystem()
    
    while True:
        print("\n==============================")
        print("     STUDENT SYSTEM MENU      ")
        print("==============================")
        print("1. Add Student")
        print("2. Show All Students")
        print("3. Search Student")
        print("4. Pass/Fail Status")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Show Statistics")
        print("8. Exit")
        print("==============================")
        
        choice = input("Choose an option (1-8): ").strip()
        
        if choice == '1':
            system.add_student()
        elif choice == '2':
            system.show_all_students()
        elif choice == '3':
            system.search_system() if hasattr(system, 'search_system') else system.search_student()
        elif choice == '4':
            system.show_pass_fail_status()
        elif choice == '5':
            system.update_student()
        elif choice == '6':
            system.delete_student()
        elif choice == '7':
            system.show_statistics()
        elif choice == '8':
            print("Goodbye! Exiting program.")
            break
        else:
            print("[!] Invalid choice. Please select from 1 to 8.")

if __name__ == "__main__":
    main()
