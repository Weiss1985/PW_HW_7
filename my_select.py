from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade

username = 'postgres'
password = '12345'
host = 'localhost'
dbname = 'postgres'
database_url = f"postgresql+psycopg2://{username}:{password}@{host}/{dbname}"
engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)


def select_1():
    with SessionLocal() as session:
        subquery = session.query(
            Grade.student_id,
            func.avg(Grade.grade).label('average_grade')
        ).group_by(Grade.student_id).subquery()

        top_students = session.query(
            Student.name,
            subquery.c.average_grade
        ).join(
            subquery, Student.id == subquery.c.student_id
        ).order_by(
            subquery.c.average_grade.desc()
        ).limit(5).all()

        return top_students


def select_2(subject_id):
    with SessionLocal() as session:
        subquery = session.query(
            Grade.student_id,
            func.avg(Grade.grade).label('average_grade')
        ).filter(Grade.subject_id == subject_id
        ).group_by(Grade.student_id).subquery()

        top_student = session.query(
            Student.name,
            subquery.c.average_grade
        ).join(
            subquery, Student.id == subquery.c.student_id
        ).order_by(
            subquery.c.average_grade.desc()
        ).first()

        return top_student


def select_3(subject_id):
    with SessionLocal() as session:
        result = session.query(
            Group.name,
            func.avg(Grade.grade).label('average_grade')
        ).join(Student, Student.group_id == Group.id
        ).join(Grade, Grade.student_id == Student.id
        ).filter(Grade.subject_id == subject_id
        ).group_by(Group.id
        ).all()

        return result


def select_4():
    with SessionLocal() as session:
        average_grade = session.query(
            func.avg(Grade.grade).label('average_grade')
        ).scalar()

        return average_grade


def select_5(teacher_id):
    with SessionLocal() as session:
        courses = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
        return [course.name for course in courses]


def select_6(group_id):
    with SessionLocal() as session:
        students = session.query(Student.name).filter(Student.group_id == group_id).all()
        return [student.name for student in students]


def select_7(group_id, subject_id):
    with SessionLocal() as session:
        grades = session.query(
            Student.name,
            Grade.grade
        ).join(Grade, Student.id == Grade.student_id
        ).filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id
        ).all()

        return grades


def select_8(teacher_id):
    with SessionLocal() as session:
        average_grade = session.query(
            func.avg(Grade.grade).label('average_grade')
        ).join(Subject, Subject.id == Grade.subject_id
        ).filter(Subject.teacher_id == teacher_id
        ).scalar()

        return average_grade


def select_9(student_id):
    with SessionLocal() as session:
        courses = session.query(
            Subject.name
        ).join(Grade, Grade.subject_id == Subject.id
        ).filter(Grade.student_id == student_id
        ).distinct().all()

        return [course.name for course in courses]


def select_10(student_id, teacher_id):
    with SessionLocal() as session:
        courses = session.query(
            Subject.name
        ).join(Grade, Grade.subject_id == Subject.id
        ).filter(Grade.student_id == student_id
        ).filter(Subject.teacher_id == teacher_id
        ).distinct().all()

        return [course.name for course in courses]


if __name__ == "__main__":
    print("TESTING FUNCTION:")

    print("5 students with the highest average score:")
    for student in select_1():
        print(student)

    subject_id_example = 1
    print(f"The student with the highest average score in the subject (ID: {subject_id_example}):")
    print(select_2(subject_id_example))

    subject_id_example = 1  
    print(f"Average score in subject groups (ID: {subject_id_example}):")
    for group in select_3(subject_id_example):
        print(group)

    print(f"Average score on stream: {select_4()}")

    teacher_id_example = 1 
    print(f"Courses taught by the teacher (ID: {teacher_id_example}):")
    for course in select_5(teacher_id_example):
        print(course)

    group_id_example = 1 
    print(f"List of students in the group (ID: {group_id_example}):")
    for student in select_6(group_id_example):
        print(student)

    group_id_example = 1 
    subject_id_example = 1 
    print(f"Grades of students (ID: {group_id_example}) in the subject group (ID: {subject_id_example}):")
    for student, grade in select_7(group_id_example, subject_id_example):
        print(f"Student: {student}, Grade: {grade}")

    teacher_id_example = 1 
    print(f"The average score given by the teacher (ID: {teacher_id_example}): {select_8(teacher_id_example)}")

    student_id_example = 1 
    print(f"List of courses attended by the student (ID: {student_id_example}):")
    for course in select_9(student_id_example):
        print(course)

    student_id_example = 1
    teacher_id_example = 1
    print(f"List of courses taught to a student (ID: {student_id_example}) by a teacher (ID: {teacher_id_example}):")
    for course in select_10(student_id_example, teacher_id_example):
        print(course)