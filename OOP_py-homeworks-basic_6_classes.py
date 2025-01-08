import itertools
import statistics

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):

   def __init__(self, name, surname, average_grade = None):
       super().__init__(name, surname)
       self.grades = {}
       self.average_grade = average_grade

   def __le__(self, other):
       return self.average_grade <= other.average_grade

   def __str__(self):
       return (f'Имя: {self.name}\n'
               f'Фамилия: {self.surname}\n'
               f'Средняя оценка за лекции: \033[94m{self.average_grade}\033[0m')

class Reviewer(Lecturer):

    # Задание № 2

    def rate_homework(self, student, course, grade):
        if isinstance(student, Student) and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
                student.average_grade = statistics.mean(list(itertools.chain.from_iterable(student.grades.values())))
            else:
                student.grades[course] = [grade]
                student.average_grade = statistics.mean(list(itertools.chain.from_iterable(student.grades.values())))
        else:
            return 'Ошибка: Курс не найден'

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')

class Student:
    def __init__(self, name, surname, average_grade = None):
        self.name = name
        self.surname = surname
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.average_grade = average_grade

    # Задание № 2

    def rate_lecturer(self, lecturer, course, grade):
        if (isinstance(some_student, Student) and isinstance(lecturer, Lecturer) and (course in self.finished_courses
            or course in self.courses_in_progress) and course in some_lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
                lecturer.average_grade = statistics.mean(list(itertools.chain.from_iterable(lecturer.grades.values())))
            else:
                lecturer.grades[course] = [grade]
                lecturer.average_grade = statistics.mean(list(itertools.chain.from_iterable(lecturer.grades.values())))
        else:
            return 'Ошибка: Курс не найден'

    def __le__(self, other):
        return self.average_grade <= other.average_grade

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: \033[94m{self.average_grade}\033[0m\n'
                f'Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {', '.join(self.finished_courses)}')

# Задание № 4

def students_average_hw_grade_for_course(students_list, course):
    grades_list = []
    for student_grades in students_list:
        grades_list.append(student_grades.grades.get(course))

    return (f'Средняя оценка за домашние задания на курсе {course}: '
               f'\033[94m{statistics.mean(list(itertools.chain.from_iterable(grades_list)))}\033[0m')

def lecturers_average_grade_for_course(lecturers_list, course):
    grades_list = []
    for lecturer_grades in lecturers_list:
        grades_list.append(lecturer_grades.grades.get(course))

    return (f'Средняя оценка курса {course} студентами: '
               f'\033[94m{statistics.mean(list(itertools.chain.from_iterable(grades_list)))}\033[0m')

# Задание № 1 и 2. Полевые испытания

students_list = []
lecturers_list = []

some_student = Student('Ruoy', 'Eman')
students_list.append(some_student)
some_student2 = Student('Ruoy2', 'Eman2')
students_list.append(some_student2)
some_student.courses_in_progress += ['Python', 'Git']
some_student.finished_courses += ['Введение в программирование']
some_student2.courses_in_progress += ['Python', 'Git']
some_student2.finished_courses += ['Введение в программирование']

some_reviewer = Reviewer('Some', 'Buddy')
some_reviewer2 = Reviewer('Some2', 'Buddy2')

some_lecturer = Lecturer('Some', 'Buddy')
lecturers_list.append(some_lecturer)
some_lecturer2 = Lecturer('Some2', 'Buddy2')
lecturers_list.append(some_lecturer2)
some_lecturer.courses_attached += ['Python', 'Git', 'Введение в программирование']

some_reviewer.rate_homework(some_student, 'Python', 9.8)
some_reviewer.rate_homework(some_student, 'Git', 10)
some_reviewer.rate_homework(some_student2, 'Python', 10)
some_reviewer.rate_homework(some_student2, 'Git', 9.8)

some_student.rate_lecturer(some_lecturer, 'Python', 10)
some_student.rate_lecturer(some_lecturer, 'Git', 9.8)
some_student2.rate_lecturer(some_lecturer2, 'Python', 9.8)
some_student2.rate_lecturer(some_lecturer2, 'Git', 10)

# Задание № 3. Полевые испытания

print(some_reviewer, '\n')
print(some_lecturer, '\n')
print(some_student, '\n')

print(some_student >= some_student2, '\n')
print(some_lecturer <= some_lecturer2, '\n')

# Задание № 4. Полевые испытания

print(students_average_hw_grade_for_course(students_list, 'Python'), '\n')
print(lecturers_average_grade_for_course(lecturers_list, 'Git'), '\n')