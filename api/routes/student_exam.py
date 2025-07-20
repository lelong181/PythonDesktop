from fastapi import APIRouter, HTTPException, Query, Body
from api.models import StudentExam, StudentExamCreate
from api.database import get_connection
from typing import List, Optional
import datetime

router = APIRouter(prefix="/student_exams", tags=["student_exams"])

@router.get("/", response_model=List[StudentExam])
def get_student_exams(student_id: Optional[int] = Query(None), exam_id: Optional[int] = Query(None)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if student_id:
        cursor.execute("SELECT * FROM student_exams WHERE student_id = %s ORDER BY id DESC", (student_id,))
    elif exam_id:
        cursor.execute("SELECT * FROM student_exams WHERE exam_id = %s ORDER BY id DESC", (exam_id,))
    else:
        cursor.execute("SELECT * FROM student_exams ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@router.post("/", response_model=StudentExam)
def create_student_exam(student_exam: StudentExamCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    start_time = student_exam.start_time or datetime.datetime.now()
    cursor.execute(
        "INSERT INTO student_exams (student_id, exam_id, start_time, status) VALUES (%s, %s, %s, %s)",
        (student_exam.student_id, student_exam.exam_id, start_time, 'in_progress')
    )
    conn.commit()
    exam_id = cursor.lastrowid
    cursor.execute("SELECT * FROM student_exams WHERE id = %s", (exam_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row 

@router.put("/{student_exam_id}")
def update_student_exam(student_exam_id: int, data: dict = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()
    # Chỉ cho phép cập nhật score và status
    score = data.get("score")
    status = data.get("status")
    if score is not None and status is not None:
        cursor.execute("UPDATE student_exams SET score = %s, status = %s, end_time = NOW() WHERE id = %s", (score, status, student_exam_id))
    elif score is not None:
        cursor.execute("UPDATE student_exams SET score = %s, end_time = NOW() WHERE id = %s", (score, student_exam_id))
    elif status is not None:
        cursor.execute("UPDATE student_exams SET status = %s, end_time = NOW() WHERE id = %s", (status, student_exam_id))
    else:
        raise HTTPException(status_code=400, detail="No valid fields to update.")
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Student exam updated"} 