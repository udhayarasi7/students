import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.student import Student

SAMPLE_STUDENTS = [
    {
        "first_name": "Aarav",
        "last_name": "Sharma",
        "email": "aarav.sharma@university.edu",
        "department": "Computer Science",
        "gpa": 3.85,
        "bio_notes": "Enthusiastic about natural language processing and agentic AI architectures."
    },
    {
        "first_name": "Maya",
        "last_name": "Patel",
        "email": "maya.patel@university.edu",
        "department": "Electrical Engineering",
        "gpa": 3.92,
        "bio_notes": "Focuses on embedded software design and edge hardware computing."
    },
    {
        "first_name": "Rohan",
        "last_name": "Iyer",
        "email": "rohan.iyer@university.edu",
        "department": "Mechanical Engineering",
        "gpa": 3.78,
        "bio_notes": "Interested in robotics and automation systems."
    }
]

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        added_count = 0
        for data in SAMPLE_STUDENTS:
            existing = db.query(Student).filter(Student.email == data["email"]).first()
            if not existing:
                student = Student(**data)
                db.add(student)
                db.commit()
                db.refresh(student)
                print(f"Added: {student.first_name} {student.last_name} (ID: {student.id})")
                added_count += 1

        if added_count == 0:
            print("All sample students are already in the database.")
        else:
            print(f"Successfully added {added_count} new student(s)!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()