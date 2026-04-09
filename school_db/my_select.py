from sqlalchemy import func, desc, and_
from app.db import SessionLocal
from app.models import Student, Group, Teacher, Subject, Grade

def select_1():
    """Find 5 students with the highest average score across all subjects."""
    session = SessionLocal()
    result = session.query(Student.name, func.round(func.avg(Grade.score), 2).label('avg_score')) \
        .select_from(Grade).join(Student) \
        .group_by(Student.id, Student.name) \
        .order_by(desc('avg_score')) \
        .limit(5).all()
    session.close()
    return result

def select_2(subject_name):
    """Find the student with the highest average score for a specific subject."""
    session = SessionLocal()
    result = session.query(Student.name, func.round(func.avg(Grade.score), 2).label('avg_score')) \
        .select_from(Grade).join(Student).join(Subject) \
        .filter(Subject.name == subject_name) \
        .group_by(Student.id, Student.name) \
        .order_by(desc('avg_score')) \
        .first()
    session.close()
    return result

def select_3(subject_name):
    """Find the average score in groups for a specific subject."""
    session = SessionLocal()
    result = session.query(Group.name, func.round(func.avg(Grade.score), 2).label('avg_score')) \
        .select_from(Grade).join(Student).join(Group).join(Subject) \
        .filter(Subject.name == subject_name) \
        .group_by(Group.id, Group.name).all()
    session.close()
    return result

def select_4():
    """Find the average score across the entire grades table."""
    session = SessionLocal()
    result = session.query(func.round(func.avg(Grade.score), 2)).scalar()
    session.close()
    return result

def select_5(teacher_name):
    """Find the courses taught by a specific teacher."""
    session = SessionLocal()
    result = session.query(Subject.name) \
        .join(Teacher) \
        .filter(Teacher.name == teacher_name).all()
    session.close()
    return result

def select_6(group_name):
    """Find the list of students in a specific group."""
    session = SessionLocal()
    result = session.query(Student.name) \
        .join(Group) \
        .filter(Group.name == group_name).all()
    session.close()
    return result

def select_7(group_name, subject_name):
    """Find student grades in a specific group for a specific subject."""
    session = SessionLocal()
    result = session.query(Student.name, Grade.score, Grade.received_at) \
        .join(Group).join(Grade).join(Subject) \
        .filter(and_(Group.name == group_name, Subject.name == subject_name)).all()
    session.close()
    return result

def select_8(teacher_name):
    """Find the average score given by a specific teacher for their subjects."""
    session = SessionLocal()
    result = session.query(func.round(func.avg(Grade.score), 2)) \
        .select_from(Grade).join(Subject).join(Teacher) \
        .filter(Teacher.name == teacher_name).scalar()
    session.close()
    return result

def select_9(student_name):
    """Find the list of courses a specific student is attending."""
    session = SessionLocal()
    result = session.query(Subject.name) \
        .select_from(Grade).join(Student).join(Subject) \
        .filter(Student.name == student_name) \
        .distinct().all()
    session.close()
    return result

def select_10(student_name, teacher_name):
    """Find the list of courses taught to a specific student by a specific teacher."""
    session = SessionLocal()
    result = session.query(Subject.name) \
        .select_from(Grade).join(Student).join(Subject).join(Teacher) \
        .filter(and_(Student.name == student_name, Teacher.name == teacher_name)) \
        .distinct().all()
    session.close()
    return result

# Additional tasks
def select_11(student_name, teacher_name):
    """Average score a specific teacher gives to a specific student."""
    session = SessionLocal()
    result = session.query(func.round(func.avg(Grade.score), 2)) \
        .select_from(Grade).join(Student).join(Subject).join(Teacher) \
        .filter(and_(Student.name == student_name, Teacher.name == teacher_name)).scalar()
    session.close()
    return result

def select_12(group_name, subject_name):
    """Grades of students in a specific group for a specific subject at the last lesson."""
    session = SessionLocal()
    # Find the last date for this group and subject
    last_date = session.query(func.max(Grade.received_at)) \
        .join(Student).join(Group).join(Subject) \
        .filter(and_(Group.name == group_name, Subject.name == subject_name)).scalar()
    
    if not last_date:
        session.close()
        return []

    result = session.query(Student.name, Grade.score, Grade.received_at) \
        .join(Group).join(Grade).join(Subject) \
        .filter(and_(Group.name == group_name, Subject.name == subject_name, Grade.received_at == last_date)).all()
    session.close()
    return result

if __name__ == "__main__":
    # Example usage (will fail if DB is not ready)
    print("Select 1 (Top 5 average):", select_1())
