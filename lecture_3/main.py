def take_name():
    """
        ask user to enter your name

        :return: user input text, Student name
    """
    name = input("Enter student name: ")
    name = name.capitalize().strip()
    return name


def check_student(list_s, name):
    """
        find in list student with name

        :param list_s: list of dictionary of students (name + grades)
        :param name: name of student
        :return: dictionary with student's name and grades from list or none
    """
    for student in list_s:
        if student.get("name") == name:
            return student
    return None

def add_student(list_add):
    """
    add new student to list

    :param list_add: list of dictionaries of students (name + grades)
    :return: None
    """
    name = take_name()
    if name == "":
        print("Not a valid name")
    elif check_student(list_add, name) is not None:
        print(f"Student {name} already exists")
    else:
        dictionary = {"name": name, "grades": []}
        list_add.append(dictionary)

def add_grades(list_add):
    """
    add grades for 1 student, any amount of grades, student name take from user input

    :param list_add: list of dictionaries of students (name + grades)
    :return: None
    """
    name = take_name()
    student = check_student(list_add, name)
    if student is None:
        print(f"Student {name} does not exist")
    else:
        while True:
            try:
                text = input("Enter your grade (or done to exit): ")
                if text == "done":
                    break
                else: grade = int(text)
                if grade < 0 or grade > 100:
                    print("Enter a valid grade")
                    continue
            except ValueError:
                print("Enter a valid number")
                continue
            student.get("grades").append(grade)

def report(list_s):
    """
    make report about all students find max, min, overall average

    :param list_s: list of dictionaries of students (name + grades)
    :return: None
    """
    if len(list_s) < 1:
        print("Not any students")
        return
    ans_list = []
    max_g = 0
    min_g = 100
    sum_all = 0
    count = 0
    any_grade = False
    ans_list.append("\n--- Student Report ---")
    for item in list_s:
        grades = item.get("grades")
        try:
            average = sum(grades) / len(grades)
            any_grade = True
            if average < min_g: min_g = average
            if average > max_g: max_g = average
            sum_all += average
            count += 1
            ans_list.append(f"{item.get('name')}'s average grade is {average}.")
        except ZeroDivisionError:
            ans_list.append(f"{item.get('name')}'s average grade is N/A.")
    if not any_grade:
        print("Not any Grades")
        return
    for item in ans_list:
        print(item)
    print("----------------------")
    print(f"Max Average: {max_g}")
    print(f"Min Average: {min_g}")
    print(f"Overall Average: {sum_all / count}")

def max_grade(list_s):
    """
    find student with the highest average grade

    :param list_s: list of dictionaries of students (name + grades)
    :return: None
    """
    if len(list_s) < 1:
        print("Not any students")
        return
    top = max(list_s, key=lambda item: sum(item.get("grades")) / len(item.get("grades")) if item.get("grades") != [] else -1)
    if not top["grades"]:
        print("Not any grades")
        return
    print(f'The student with the highest average is {top["name"]} with a grade of '
          f'{sum(top.get("grades")) / len(top.get("grades"))}.')

#infiny lap with choose variant of action
if __name__ == "__main__":
    students = []
    while True:
        print(f"\n--- Student Grade Analyzer ---\n"
              f"1. Add a new student\n"
              f"2. Add grades for a student\n"
              f"3. Generate a full report\n"
              f"4. Find the top student\n"
              f"5. Exit program\n")
        try:
            chose = int(input("Enter your choice: "))
        except ValueError:
            print("Enter a valid number")
            continue

        match chose:
            case 1: add_student(students)
            case 2: add_grades(students)
            case 3: report(students)
            case 4: max_grade(students)
            case 5: break
            case _:
                print("Enter a valid choice")
                continue
