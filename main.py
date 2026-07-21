from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Student Management API")

class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str

students = [
    Student(id=1, name="Ali", age=20, course="Computer Science"),
    Student(id=2, name="Ahmed", age=21, course="Software Engineering")
]

@app.get("/students", response_model=List[Student])
def get_students():
    return students

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    for student in students:
        if student.id == student_id:
            return student
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def add_student(student: Student):
    for s in students:
        if s.id == student.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student ID already exists"
            )
    students.append(student)
    return student

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    for index, student in enumerate(students):
        if student.id == student_id:
            students[index] = updated_student
            return updated_student
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student.id == student_id:
            students.remove(student)
            return {"message": "Student deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )
