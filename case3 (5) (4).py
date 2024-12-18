import json
import hashlib
from abc import ABC, abstractmethod
from datetime import datetime


class Person(ABC):
    def __init__(self, name, phone, address, date_of_birth):
        self._name = name
        self._phone = phone
        self._address = address
        self._date_of_birth = date_of_birth

    @abstractmethod
    def get_details(self):
        pass

    @staticmethod
    def validate_email(email):
        return "@" in email

    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and len(phone) >= 10
    @staticmethod
    def calculate_age(date_of_birth, current_date):
        return current_date.year - date_of_birth.year

    @staticmethod
    def format_address(address):
        return address.title()

    @staticmethod
    def validate_name(name):
        return name.isalpha()

    @classmethod
    def create_from_dict(cls, data):
        return cls(data['name'], data['phone'], data['address'], data['date_of_birth'])

    @classmethod
    def create_default(cls):
        return cls("Default Name", "0000000000", "Default Address", None)
    
class User:
    def __init__(self, id, email, password, role, person):
        self._id = id
        self._password = password
        self._email = email
        self._person = person
        self._role = role

    def get_details(self):
        return {
            "email": self._email,
            "password": self._password,
            "role": self._role,
            "person": self._person.get_details()
        }

    def create(self):
        # TODO
        pass

    def update(self):
        # TODO
        pass

    def delete(self):
        # TODO
        pass

class Admin(Person):
    def __init__(self, name, phone, address, date_of_birth):
        super().__init__(name, phone, address, date_of_birth)

    def get_details(self):
        return {
            "name": self._name,
            "phone": self._phone,
            "address": self._address,
            "date_of_birth": self._date_of_birth
        }


class Student(Person):
    def __init__(self, name, phone, address, date_of_birth, student_id):
        super().__init__(name, phone, address, date_of_birth)
        self.student_id = student_id
        self.courses = []  # List to hold enrolled courses
        self.grades = {}  # Dictionary to hold grades for courses  

    def enroll_course(self, course):
        # Check if the course is already enrolled based on course_id
        if course['course_id'] not in [c['course_id'] for c in self.courses]:
            self.courses.append(course)
            print(f"{self._name} enrolled in {course['name']}.")
        else:
            print(f"{self._name} is already enrolled in {course['name']}.")

    def assign_grade(self, course_name, grade):
        if course_name in self.grades:
            print(f"{self._name} already has a grade for {course_name}.")
        else:
            self.grades[course_name] = grade  # Make sure this is a dictionary update
            print(f"Assigned grade {grade} to {self._name} for course {course_name}.")


    def get_details(self):
        return {
            "name": self._name,
            "phone": self._phone,
            "address": self._address,
            "date_of_birth": self._date_of_birth,
            "student_id": self.student_id,
            "courses": self.courses,
            "grades": self.grades,
        }

    def view_courses(self):
        if not self.courses:
            print(f"{self._name} is not enrolled in any courses yet.")
        else:
            print(f"Courses enrolled by {self._name}:")
            for course in self.courses:
                print(f"- {course['name']}")

    def view_grades(self):
        if not self.grades:
            print(f"{self._name} has no grades assigned.")
        else:
            print(f"Grades for {self._name}:")
            for grade_info in self.grades:  # Iterate over the list of grades
                course_name = grade_info['course_name']
                grade = grade_info['grade']
                print(f"Course: {course_name}, Grade: {grade}")




    def view_assignment_grades(self):
        if not self.grades:
            print(f"{self._name} has no assignment grades.")
        else:
            print(f"Assignment grades for {self._name}:")
            for grade_info in self.grades:  # Iterate over the list of grades
                course_name = grade_info['course_name']
                grade = grade_info['grade']
                print(f"Course: {course_name}, Grade: {grade}")


    # View schedule for all enrolled courses
    def view_schedule(self):
        if not self.courses:
            print(f"{self._name} is not enrolled in any courses yet.")
        else:
            print(f"Schedule for {self._name}:")
            for course in self.courses:
                if 'schedule' in course:
                    schedule = course['schedule']
                    print(f"\nCourse: {course['name']}")
                    print(f"Start Date: {schedule['start_date']}")
                    print(f"End Date: {schedule['end_date']}")
                    print(f"Class Time: {schedule['class_time']}")
                    print(f"Days: {', '.join(schedule['days'])}")
                else:
                    print(f"Schedule not available for {course['name']}.")





class Instructor(Person):
    def __init__(self, name, phone, address, date_of_birth, instructor_id):
        super().__init__(name, phone, address, date_of_birth)
        self.instructor_id = instructor_id
        self.courses_taught = []
        self.schedules = []  # A list to hold schedules for courses taught by the instructor

    def assign_course(self, course, admin):
        # Find the instructor data in admin
        instructor_data = next((i for i in admin.data["instructors"] if i["instructor_id"] == self.instructor_id), None)
        
        if not instructor_data:
            print(f"Instructor with ID {self.instructor_id} not found.")
            return

        # Check if the course is already assigned
        if any(c["name"] == course["name"] for c in instructor_data["courses_taught"]):
            print(f"{self._name} is already teaching the course {course['name']}.")
        else:
            # Add course to admin data
            instructor_data["courses_taught"].append(course)

            # Synchronize to self.courses_taught
            self.courses_taught.append(course)

            # Save changes to the admin's persistent data
            admin.save_data()

            print(f"Assigned course {course['name']} to instructor {self._name}.")


    def create_assignment(self, course_name, assignment_name, description, due_date, admin):
       
        instructor_data = next((i for i in admin.data["instructors"] if i["instructor_id"] == self.instructor_id), None)
        
        if not instructor_data:
            print(f"Instructor with ID {self.instructor_id} not found.")
            return
        
        # Check if the instructor teaches the given course
        course = next((c for c in instructor_data["courses_taught"] if c["name"] == course_name), None)
        
        if not course:
            print(f"{self._name} is not teaching the course {course_name}.")
            return
        
        # Create the new assignment
        assignment = {
            "assignment_name": assignment_name,
            "description": description,
            "due_date": due_date,
            "grades": []  
        }
        
        
        if "assignments" not in course:
            course["assignments"] = []
        
       
        course["assignments"].append(assignment)
        print(f"Assignment '{assignment_name}' added to course '{course_name}' by {self._name}.")
        
       
        admin.save_data()

    def assign_grade(self, student_id, course_name, assignment_name, grade, admin):
        student_data = next((s for s in admin.data["students"] if s["student_id"] == student_id), None)
        if not student_data:
            print(f"Student with ID {student_id} not found.")
            return

        # Ensure that grades field exists for the student
        if "grades" not in student_data or not isinstance(student_data["grades"], list):
            student_data["grades"] = []  # Initialize grades as an empty list if not present

        # Find the course the instructor is teaching
        course = next((c for c in self.courses_taught if c["name"] == course_name), None)
        if not course:
            print(f"{self._name} is not teaching the course {course_name}.")
            return

        # Find the assignment in the course
        assignment = next((a for a in course.get("assignments", []) if a["assignment_name"] == assignment_name), None)
        if not assignment:
            print(f"Assignment {assignment_name} not found in course {course_name}.")
            return

        # Ensure that grades field exists for the assignment
        if "grades" not in assignment:
            assignment["grades"] = []  # Initialize grades as an empty list if not present

        # Check if the grade for the student already exists in the assignment
        existing_grade = next((g for g in assignment["grades"] if g["student_id"] == student_id), None)
        if existing_grade:
            print(f"Grade for {student_data['name']} in assignment '{assignment_name}' already assigned.")
            return

        # Add the grade to the assignment
        assignment["grades"].append({
            "student_id": student_id,
            "grade": grade
        })

        # Add the grade to the student's record
        student_data["grades"].append({
            "course_name": course_name,
            "assignment_name": assignment_name,
            "grade": grade
        })

        print(f"Grade {grade} assigned to {student_data['name']} for assignment '{assignment_name}' in course {course_name}.")
        admin.save_data()




    def assign_grade(self, student_id, course_name, assignment_name, grade, admin):
        # Find the instructor data
        instructor_data = next((i for i in admin.data["instructors"] if i["instructor_id"] == self.instructor_id), None)

        if instructor_data:
            # Check if the instructor is teaching the course
            if any(course['name'] == course_name for course in instructor_data['courses_taught']):
                # Find the course and assignment
                course_data = next((course for course in instructor_data['courses_taught'] if course['name'] == course_name), None)
                if course_data:
                    assignment_data = next((assignment for assignment in course_data['assignments'] if assignment['assignment_name'] == assignment_name), None)
                    if assignment_data:
                        # Add the grade to the instructor's assignment data
                        existing_grade = next((g for g in assignment_data.get("grades", []) if g["student_id"] == student_id), None)
                        if existing_grade:
                            # Update the existing grade
                            existing_grade['grade'] = grade
                        else:
                            # Add new grade if none exists
                            assignment_data.setdefault("grades", []).append({
                                "student_id": student_id,
                                "grade": grade
                            })

                        # Now add the grade to the student's record as well
                        student_data = next((s for s in admin.data["students"] if s["student_id"] == student_id), None)
                        if student_data:
                            # Ensure grades is a list
                            if not isinstance(student_data["grades"], list):
                                student_data["grades"] = []  # Convert to a list if it's not one

                            student_grade = next((g for g in student_data["grades"] if g["course_name"] == course_name), None)
                            if student_grade:
                                student_grade["grade"] = grade  # Update grade if it exists
                            else:
                                # Add new grade if none exists
                                student_data["grades"].append({
                                    "course_name": course_name,
                                    "grade": grade
                                })
                            print(f"Grade {grade} assigned to student {student_id} for {assignment_name} in {course_name}.")
                        else:
                            print(f"Student with ID {student_id} not found.")
                        
                        admin.save_data()  # Save after modification
                    else:
                        print(f"Assignment {assignment_name} not found in course {course_name}.")
                else:
                    print(f"Course {course_name} not found.")
            else:
                print(f"{self._name} is not teaching the course {course_name}.")
        else:
            print(f"Instructor with ID {self.instructor_id} not found.")
            
            
    def view_courses(self, admin):
        instructor_data = next((i for i in admin.data["instructors"] if i["instructor_id"] == self.instructor_id), None)
        if instructor_data and instructor_data["courses_taught"]:
            print(f"Courses taught by {self._name}:")
            for course in instructor_data["courses_taught"]:
                print(f"- {course['name']}")
        else:
            print(f"{self._name} is not teaching any courses yet.")






    def get_details(self):
        return {
            "name": self._name,
            "phone": self._phone,
            "address": self._address,
            "date_of_birth": self._date_of_birth,
            "instructor_id": self.instructor_id,
            "courses_taught": self.courses_taught,
        }

    # New Method: Assign a schedule to a course
    def assign_schedule(self, course_name, start_date, end_date, class_time, days, admin):
        # Find the course the instructor is teaching
        course = next((c for c in self.courses_taught if c["name"] == course_name), None)
        if not course:
            print(f"{self._name} is not teaching the course {course_name}.")
            return
        
        # Create a new schedule
        schedule = Schedule(course_name, start_date, end_date, class_time, days)
        
        # Add the schedule to the instructor's list of schedules
        self.schedules.append(schedule)
        print(f"Schedule assigned to course '{course_name}' by {self._name}.")
        
        # Save the updated data (this can be customized if needed)
        admin.save_data()

    # New Method: View the schedule of a course
    def view_schedule(self, course_name):
        # Find the schedule for the given course
        schedule = next((s for s in self.schedules if s.course_id == course_name), None)
        if not schedule:
            print(f"No schedule found for course '{course_name}' taught by {self._name}.")
            return
        
        # Print schedule details
        print(f"Schedule for course '{course_name}' taught by {self._name}:")
        print(f"Start Date: {schedule.start_date}")
        print(f"End Date: {schedule.end_date}")
        print(f"Class Time: {schedule.class_time}")
        print(f"Days: {schedule.days}")





class Grade:
    def __init__(self, student_id, course_id, assignment_id, grade_value):
        self.student_id = student_id
        self.course_id = course_id
        self.assignment_id = assignment_id
        self.grade_value = grade_value

    def get_details(self):
        return {
            "student_id": self.student_id,
            "course_id": self.course_id,
            "assignment_id": self.assignment_id,
            "grade_value": self.grade_value,
        }
    
    @staticmethod
    def is_valid_grade(grade_value):
        """Validate if the grade value is within a certain range."""
        return 0 <= grade_value <= 100

    @classmethod
    def from_dict(cls, data):
        """Create a Grade object from a dictionary."""
        return cls(
            data["student_id"],
            data["course_id"],
            data["assignment_id"],
            data["grade_value"]
        )


class Assignment:
    def __init__(self, assignment_id, title, description, due_date, course_id):
        self.assignment_id = assignment_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.course_id = course_id

    def get_details(self):
        return {
            "assignment_id": self.assignment_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "course_id": self.course_id,
        }
    @staticmethod
    def is_due_soon(due_date, current_date):
        """Check if the assignment is due soon given the current date."""
        return (due_date - current_date).days <= 3

    @classmethod
    def from_dict(cls, data):
        """Create an Assignment object from a dictionary."""
        return cls(
            data["assignment_id"],
            data["title"],
            data["description"],
            data["due_date"],
            data["course_id"]
        )


class Schedule:
    def __init__(self, course_name, start_date, end_date, class_time, days):
        self.course_name = course_name
        self.start_date = start_date
        self.end_date = end_date
        self.class_time = class_time
        self.days = days

    def get_details(self):
        return {
            "course_id": self.course_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "class_time": self.class_time,
            "days": self.days,
        }
    @staticmethod
    def is_active(start_date, end_date, current_date):
        """Check if the schedule is currently active."""
        return start_date <= current_date <= end_date

    @classmethod
    def from_dict(cls, data):
        """Create a Schedule object from a dictionary."""
        return cls(
            data["course_id"],
            data["start_date"],
            data["end_date"],
            data["class_time"],
            data["days"]
        )

class Course:
    def __init__(self, course_id, name, description, schedule, duration, level, enrollments, instructor, module_list, start_date,price):
        self.course_id = course_id
        self.name = name
        self.description = description
        self.schedule = schedule
        self.duration = duration
        self.level = level
        self.enrollments = enrollments
        self.instructor = instructor
        self.module_list = module_list
        self.start_date = start_date
        self.price = price

    def get_course_details(self):
        return{

        }

class Module:
    def __init_(self, module_id, title, description, lessons, module_duration, order):
        self.module_id = module_id
        self.title = title
        self.description = description
        self.lessons = lessons
        self.module_duration = module_duration
        self.order = order

    def get_module():
        return{

        }

class Online_class:
    def __init__(self, online_class_id, title, schedule, module, link, class_type, duration, recorded):
        self.online_class_id = online_class_id
        self.title = title
        self.schedule = schedule
        self.module = module
        self.link = link
        self.class_type = class_type
        self.duraton = duration
        self.recorded = recorded
    
    def get_online_details():
        return{

        }
    
class Enrollment:
    def __init__(self, enrollment_id, student, course, status, enrollment_date, progress):
        self.enrollment_id = enrollment_id
        self.student = student
        self.course = course
        self.status = status
        self.enrollment_date = enrollment_date
        self.progress = progress

    def get_enroll_student():
        return{

        }

class PlatformAdmin:
    def __init__(self, data_file="data2.json"):
        self.data_file = data_file
        self.data = {
            "users": [],
            "students": [],
            "instructors": [],
            "courses": [],
            "assignments": [],
            "grades": [],
            "schedules": [],
        }
        self.load_data()

    def add_assignment(self, assignment_id, title, description, due_date, course_id):
        assignment = Assignment(assignment_id, title, description, due_date, course_id)
        self.data["assignments"].append(assignment.get_details())
        self.save_data()
        print(f"Assignment {title} added successfully!")

    def list_assignments(self, course_id=None):
        if course_id:
            assignments = [a for a in self.data["assignments"] if a["course_id"] == course_id]
        else:
            assignments = self.data["assignments"]

        if assignments:
            print("Assignments:")
            for assignment in assignments:
                print(f"- {assignment['title']} (ID: {assignment['assignment_id']})")
        else:
            print("No assignments found.")

    def add_schedule(self, course_id, start_date, end_date, class_time, days):
        schedule = Schedule(course_id, start_date, end_date, class_time, days)
        self.data["schedules"].append(schedule.get_details())
        self.save_data()
        print(f"Schedule for course {course_id} added successfully!")

    def list_schedules(self):
        if self.data["schedules"]:
            print("Course Schedules:")
            for schedule in self.data["schedules"]:
                print(
                    f"- Course ID: {schedule['course_id']}, Start: {schedule['start_date']}, "
                    f"End: {schedule['end_date']}, Time: {schedule['class_time']}, Days: {schedule['days']}"
                )
        else:
            print("No schedules found.")

    def add_grade(self, student_id, course_id, assignment_id, grade_value):
        grade = Grade(student_id, course_id, assignment_id, grade_value)
        self.data["grades"].append(grade.get_details())
        self.save_data()
        print(f"Grade {grade_value} added for student {student_id} in course {course_id}.")

    def list_grades(self, student_id=None, course_id=None):
        grades = self.data["grades"]
        if student_id:
            grades = [g for g in grades if g["student_id"] == student_id]
        if course_id:
            grades = [g for g in grades if g["course_id"] == course_id]

        if grades:
            print("Grades:")
            for grade in grades:
                print(
                    f"- Student ID: {grade['student_id']}, Course ID: {grade['course_id']}, "
                    f"Assignment ID: {grade['assignment_id']}, Grade: {grade['grade_value']}"
                )
        else:
            print("No grades found.")

    def load_data(self):
        try:
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
                print("Data loaded successfully.")
        except FileNotFoundError:
            print("Data file not found. Starting with empty data.")
        except json.JSONDecodeError:
            print("Data file is corrupt. Starting with empty data.")

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)
            print("Data saved successfully.")

    def sign_up(self, name, email, phone, address, date_of_birth, password, role):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_id = len(self.data["users"]) + 1

        if role == "student":
            student_id = input("Enter Student ID: ")
            student = Student(name, phone, address, date_of_birth, student_id)
            user = User(id=user_id, email=email, password=hashed_password, role=role, person=student)
            self.data["users"].append(user.get_details())
            self.data["students"].append(student.get_details())
            self.save_data()
            print(f"Student {name} signed up successfully with ID {student_id}!")
        elif role == "instructor":
            instructor_id = input("Enter Instructor ID: ")
            instructor = Instructor(name, phone, address, date_of_birth, instructor_id)
            user = User(id=user_id, email=email, password=hashed_password, role=role, person=instructor)
            self.data["users"].append(user.get_details())
            self.data["instructors"].append(instructor.get_details())
            self.save_data()
            print(f"Instructor {name} signed up successfully with ID {instructor_id}!")
        elif role == "admin":
            admin = Admin(name, phone, address, date_of_birth)
            user = User(id=user_id, email=email, password=hashed_password, role=role, person=admin)
            self.data["users"].append(user.get_details())
            self.save_data()

    def login(self, email, password):
        for user in self.data["users"]:
            if user["email"] == email:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user["password"] == hashed_password:
                    print(f"Welcome {user['person']['name']}!")
                    return user["role"]
                else:
                    print("Invalid password.")
                    return None
        print("User not found.")
        return None

    def add_course(self, course):
        self.data["courses"].append(course)
        self.save_data()
        print(f"Added course {course['name']}.")

    def list_courses(self):
        print("Available courses:")
        for course in self.data["courses"]:
            print(f"- {course['name']}")

    def view_student_courses(self, student_id):
        student = next((s for s in self.data["students"] if s["student_id"] == student_id), None)
        if student:
            print(f"Courses for student {student['name']}:")
            for course in student["courses"]:
                print(f"- {course['name']}")
        else:
            print("Student not found.")


    def add_grade(self, assignment_id, student_id, grade):
        print(f"Grade for assignment {assignment_id} and student {student_id} is now {grade}.")
       


def student_menu(admin, student_id):
    while True:
        print("\n--- Student Menu ---")
        print("1. View Courses")
        print("2. View Grades for Courses")
        print("3. View Assignment Grades")
        print("4. Enroll in a Course") 
        print("5. View Schedule")  # New option to view schedule
        print("6. Logout")
        
        choice = input("Select an option: ")

        if choice == "1":
            student_data = next((s for s in admin.data["students"] if s["student_id"] == student_id), None)
            if student_data:
                student = Student(
                    student_data["name"],
                    student_data["phone"],
                    student_data["address"],
                    student_data["date_of_birth"],
                    student_data["student_id"]
                )
                student.courses = student_data.get("courses", [])
                student.view_courses()
            else:
                print("Student not found.")

        elif choice == "2":
            student_data = next((s for s in admin.data["students"] if s["student_id"] == student_id), None)
            if student_data:
                student = Student(
                    student_data["name"],
                    student_data["phone"],
                    student_data["address"],
                    student_data["date_of_birth"],
                    student_data["student_id"]
                )
                student.grades = student_data.get("grades", {})
                student.view_grades()
            else:
                print("Student not found.")

        elif choice == "3":
            student_data = next((s for s in admin.data["students"] if s["student_id"] == student_id), None)
            if student_data:
                student = Student(
                    student_data["name"],
                    student_data["phone"],
                    student_data["address"],
                    student_data["date_of_birth"],
                    student_data["student_id"]
                )
                student.grades = student_data.get("grades", {})
                student.view_assignment_grades()
            else:
                print("Student not found.")

        elif choice == "4":
            admin.list_courses()
            course_name = input("Enter the name of the course you want to enroll in: ")
            course = next((c for c in admin.data["courses"] if c.get("name") == course_name), None)
            if course:
                student_data = next((s for s in admin.data["students"] if s["student_id"] == student_id), None)
                if student_data:
                    student = Student(
                        student_data["name"],
                        student_data["phone"],
                        student_data["address"],
                        student_data["date_of_birth"],
                        student_data["student_id"]
                    )
                    student.enroll_course(course)

                    # Here, we're appending the full course object to the student's course list, including the schedule
                    student_data["courses"].append(course)
                    admin.save_data()
                    print(f"{student_data['name']} successfully enrolled in {course['name']}!")
                else:
                    print("Student not found.")
            else:
                print(f"Course with Name '{course_name}' not found.")


        # Inside the student_menu function, when the user selects option 5 (View Schedule)
        elif choice == "5":
            student_data = next((s for s in admin.data["students"] if s["student_id"] == student_id), None)
            if student_data:
                student = Student(
                    student_data["name"],
                    student_data["phone"],
                    student_data["address"],
                    student_data["date_of_birth"],
                    student_data["student_id"]
                )
                student.courses = student_data.get("courses", [])
                
                # View the schedule for each course the student is enrolled in
                print(f"\nSchedule for {student._name}:")
                student.view_schedule()  # Call view_schedule without passing any argument
            else:
                print("Student not found.")


        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid option, please try again.")



def instructor_menu(admin, instructor_id):
    # Retrieve instructor data at the beginning of the menu
    instructor_data = next((i for i in admin.data["instructors"] if i["instructor_id"] == instructor_id), None)

    # Check if instructor data exists
    if not instructor_data:
        print(f"Error: No instructor found with ID {instructor_id}.")
        return  # Exit the function if no instructor is found

    # Create the instructor instance once
    instructor = Instructor(
        instructor_data["name"],
        instructor_data["phone"],
        instructor_data["address"],
        instructor_data["date_of_birth"],
        instructor_data["instructor_id"]
    )

    # Instructor menu options
    while True:
        print("\n--- Instructor Menu ---")
        print("1. View Courses")
        print("2. Assign Grade")
        print("3. Add Course to Teach")
        print("4. Create Assignment")
        print("5. Logout")
        choice = input("Select an option: ")

        if choice == "1":
            instructor.view_courses(admin)

        elif choice == "2":
            course_name = input("Enter course name: ")
            assignment_name = input("Enter assignment name: ")
            grade = input(f"Enter grade for assignment {assignment_name}: ")
            student_id = input("Enter student ID: ")
            instructor.assign_grade(student_id, course_name, assignment_name, grade, admin)

        elif choice == "3":
            course_name = input("Enter course name: ")
            course_description = input("Enter course description: ")
            course = {"name": course_name, "description": course_description, "assignments": []}
            instructor.assign_course(course, admin)

        elif choice == "4":
            course_name = input("Enter course name: ")
            assignment_name = input("Enter assignment name: ")
            description = input("Enter assignment description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            instructor.create_assignment(course_name, assignment_name, description, due_date, admin)

        elif choice == "5":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")




def admin_menu(admin):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Student")
        print("2. Add Instructor")
        print("3. Add Course")
        print("4. List Students")
        print("5. List Instructors")
        print("6. List Courses")
        print("7. Logout")
        choice = input("Select an option: ")

        if choice == "1":
            name = input("Enter student's name: ")
            email = input("Enter student's email: ")
            phone = input("Enter student's phone: ")
            address = input("Enter student's address: ")
            date_of_birth = input("Enter student's date of birth (YYYY-MM-DD): ")
            student_id = input("Enter student ID: ")

           
            student = Student(name, phone, address, date_of_birth, student_id)
            admin.data["students"].append(student.get_details())

            temp_password = "password123"  # Temporary default password
            hashed_password = hashlib.sha256(temp_password.encode()).hexdigest()
            user_id = len(admin.credentials) + 1
            user = User(id=user_id, email=email, password=hashed_password, role="student", person=student)
            admin.data["users"].append(user.get_details())

            # admin.credentials[user_id] = {
            #     "name": name,
            #     "email": email,
            #     "password": hashed_password,
            #     "role": "student"
            # }
           
            admin.save_data()
            # admin.save_credentials()

            print(f"Student {name} added successfully!")
            print(f"Credentials for {name}:")
            print(f"Username: {email}")
            print(f"Password: {temp_password} (Change it after logging in!)")

        elif choice == "2":
            
            name = input("Enter instructor's name: ")
            email = input("Enter instructor's email: ")
            phone = input("Enter instructor's phone: ")
            address = input("Enter instructor's address: ")
            date_of_birth = input("Enter instructor's date of birth (YYYY-MM-DD): ")
            instructor_id = input("Enter instructor ID: ")

            instructor = Instructor(name, phone, address, date_of_birth, instructor_id)
            admin.data["instructors"].append(instructor.get_details())

            temp_password = "password123"  # Temporary default password
            hashed_password = hashlib.sha256(temp_password.encode()).hexdigest()
            user_id = len(admin.credentials) + 1
            user = User(id=user_id, email=email, password=hashed_password, role="student", person=instructor)
            admin.data["users"].append(user.get_details())

            admin.save_data()
            print(f"Instructor {name} added successfully!")
            print(f"Credentials for {name}:")
            print(f"Username: {email}")
            print(f"Password: {temp_password} (Change it after logging in!)")

        elif choice == "3":
         
            course_id = input("Enter course ID: ")
            course_name = input("Enter course name: ")
            course_description = input("Enter course description: ")
            course = {"course_id": course_id, "name": course_name, "description": course_description}
            admin.add_course(course)

        elif choice == "4":
            print("Listing all students:")
            for student in admin.data["students"]:
                print(f"- {student['name']} (ID: {student['student_id']})")

        elif choice == "5":
            print("Listing all instructors:")
            for instructor in admin.data["instructors"]:
                print(f"- {instructor['name']} (ID: {instructor['instructor_id']})")

        elif choice == "6":
            admin.list_courses()

        elif choice == "7":
            print("Logging out...")
            break

        else:
            print("Invalid option. Please try again.")

def main():
    admin = PlatformAdmin()

    while True:
        print("\n--- Main Menu ---")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            phone = input("Enter phone number: ")
            address = input("Enter address: ")
            date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
            password = input("Enter password: ")
            role = input("Enter role (student/instructor/admin): ")
            if role not in ["student", "instructor", "admin"]:
                print("Invalid role. Please choose 'student', 'instructor', or 'admin'.")
                continue
            admin.sign_up(name, email, phone, address, date_of_birth, password, role)

        elif choice == "2":
            email = input("Enter email: ")
            password = input("Enter password: ")
            role = admin.login(email, password)
            if role == "admin":
                admin_menu(admin)
            elif role == "instructor":
                instructor_id = input("Enter your instructor ID: ")
                instructor_menu(admin, instructor_id)
            elif role == "student":
                student_id = input("Enter your student ID: ")
                student_menu(admin, student_id)
            else:
                print("Login failed.")

        elif choice == "3":
            print("Goodbye!")
            break
 

if __name__ == "__main__":
    main()
