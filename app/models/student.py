from sqlalchemy import Column, Integer, String, Float, Text, event
from app.database import Base
from app.services.vector_service import vector_service

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    department = Column(String(50), index=True)
    gpa = Column(Float, default=0.0)
    bio_notes = Column(Text, nullable=True)

# Event listeners for automatic ChromaDB sync
def sync_vector_on_save(mapper, connection, target: Student):
    metadata = {
        "department": target.department or "",
        "email": target.email,
        "full_name": f"{target.first_name} {target.last_name}"
    }
    vector_service.upsert_student_bio(
        student_id=target.id,
        bio_notes=target.bio_notes or "",
        metadata=metadata
    )

def sync_vector_on_delete(mapper, connection, target: Student):
    vector_service.delete_student_bio(student_id=target.id)

event.listen(Student, 'after_insert', sync_vector_on_save)
event.listen(Student, 'after_update', sync_vector_on_save)
event.listen(Student, 'after_delete', sync_vector_on_delete)