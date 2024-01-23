from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base, Student, Group, Teacher, Subject, Grade
from faker import Faker
import random
import logging

username = 'postgres'
password = '12345'
host = 'localhost'
dbname = 'postgres'
database_url = f"postgresql+psycopg2://{username}:{password}@{host}/{dbname}"
engine = create_engine(database_url)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

faker = Faker()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

with DBSession() as session:

    groups = [Group(name=f"Group {faker.word()}") for _ in range(3)]
    session.add_all(groups)

    teachers = [Teacher(name=faker.name()) for _ in range(5)]
    session.add_all(teachers)

    subjects = [Subject(name=faker.word(), teacher_id=random.randint(1, 5)) for _ in range(8)]
    session.add_all(subjects)

    students = [Student(name=faker.name(), group_id=random.randint(1, 3)) for _ in range(50)]
    session.add_all(students)

    session.commit()

    for student in students:
        for subject in subjects:
            grades = [Grade(
                student_id=student.id,
                subject_id=subject.id,
                grade=random.randint(1, 5),
                date_received=faker.date_time_between(start_date="-1y", end_date="now")
            ) for _ in range(random.randint(5, 20))]
            session.add_all(grades)

    session.commit()
