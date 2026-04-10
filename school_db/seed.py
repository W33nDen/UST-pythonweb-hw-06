import random
from faker import Faker
from sqlalchemy.orm import Session
from app.db import engine, SessionLocal
from app.models import Group, Student, Teacher, Subject, Grade
import datetime

fake = Faker()

def seed_data():
    with SessionLocal() as session:
        try:
            # 1. Create 3 groups
            groups = [Group(name=f"Group {i+1}") for i in range(3)]
            session.add_all(groups)
            session.flush()

            # 2. Create 3-5 teachers
            teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]
            session.add_all(teachers)
            session.flush()

            # 3. Create 5-8 subjects
            subject_names = ["Mathematics", "Physics", "Chemistry", "History", "Literature", "Biology", "Programming", "English"]
            subjects = []
            for i in range(random.randint(5, 8)):
                subjects.append(Subject(
                    name=subject_names[i] if i < len(subject_names) else f"Subject {i+1}",
                    teacher=random.choice(teachers)
                ))
            session.add_all(subjects)
            session.flush()

            # 4. Create 30-50 students
            students = []
            for _ in range(random.randint(30, 50)):
                students.append(Student(
                    name=fake.name(),
                    group=random.choice(groups)
                ))
            session.add_all(students)
            session.flush()

            # 5. Create grades (up to 20 for each student)
            for student in students:
                for _ in range(random.randint(1, 20)):
                    grade = Grade(
                        student=student,
                        subject=random.choice(subjects),
                        score=random.uniform(2.0, 5.0),  # Assuming 2-5 scale
                        received_at=fake.date_time_between(start_date='-1y', end_date='now')
                    )
                    session.add(grade)
            
            session.commit()
            print("Database successfully seeded!")

        except Exception as e:
            session.rollback()
            print(f"An error occurred during seeding: {e}")
            raise

if __name__ == "__main__":
    seed_data()
