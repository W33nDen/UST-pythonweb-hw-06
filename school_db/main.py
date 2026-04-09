import argparse
from app.db import SessionLocal
from app.models import Teacher, Group, Student, Subject, Grade

def main():
    parser = argparse.ArgumentParser(description="CRUD operations for school database")
    parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"], required=True, help="CRUD action")
    parser.add_argument("-m", "--model", choices=["Teacher", "Group", "Student", "Subject", "Grade"], required=True, help="Model to operate on")
    parser.add_argument("-n", "--name", help="Name for create/update")
    parser.add_argument("--id", type=int, help="ID for update/remove")
    parser.add_argument("--group_id", type=int, help="Group ID for student")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID for subject")
    parser.add_argument("--student_id", type=int, help="Student ID for grade")
    parser.add_argument("--subject_id", type=int, help="Subject ID for grade")
    parser.add_argument("--score", type=float, help="Score for grade")

    args = parser.parse_args()
    session = SessionLocal()

    try:
        model_class = globals()[args.model]

        if args.action == "create":
            if args.model == "Teacher":
                obj = Teacher(name=args.name)
            elif args.model == "Group":
                obj = Group(name=args.name)
            elif args.model == "Student":
                obj = Student(name=args.name, group_id=args.group_id)
            elif args.model == "Subject":
                obj = Subject(name=args.name, teacher_id=args.teacher_id)
            elif args.model == "Grade":
                obj = Grade(score=args.score, student_id=args.student_id, subject_id=args.subject_id)
            
            session.add(obj)
            session.commit()
            print(f"Created {args.model} with ID {obj.id}")

        elif args.action == "list":
            items = session.query(model_class).all()
            for item in items:
                if hasattr(item, 'name'):
                    print(f"ID: {item.id}, Name: {item.name}")
                else:
                    print(f"ID: {item.id}, Data: {item.__dict__}")

        elif args.action == "update":
            obj = session.query(model_class).filter(model_class.id == args.id).first()
            if obj:
                if args.name: obj.name = args.name
                if args.group_id: obj.group_id = args.group_id
                if args.teacher_id: obj.teacher_id = args.teacher_id
                if args.score: obj.score = args.score
                session.commit()
                print(f"Updated {args.model} with ID {args.id}")
            else:
                print(f"Not found: {args.model} with ID {args.id}")

        elif args.action == "remove":
            obj = session.query(model_class).filter(model_class.id == args.id).first()
            if obj:
                session.delete(obj)
                session.commit()
                print(f"Removed {args.model} with ID {args.id}")
            else:
                print(f"Not found: {args.model} with ID {args.id}")

    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
