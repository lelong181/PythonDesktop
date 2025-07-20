from fastapi import APIRouter, HTTPException, Query
from api.database import get_connection
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/exam_questions", tags=["exam_questions"])

class ExamQuestionCreate(BaseModel):
    exam_id: int
    question_id: int
    question_order: int

@router.post("/")
def add_exam_question(eq: ExamQuestionCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO exam_questions (exam_id, question_id, question_order) VALUES (%s, %s, %s)",
        (eq.exam_id, eq.question_id, eq.question_order)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Added"}

@router.get("/", response_model=List[dict])
def get_exam_questions(exam_id: Optional[int] = Query(None)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if exam_id:
        cursor.execute("SELECT * FROM exam_questions WHERE exam_id = %s ORDER BY question_order", (exam_id,))
    else:
        cursor.execute("SELECT * FROM exam_questions ORDER BY exam_id, question_order")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@router.get("/with_questions/", response_model=List[dict])
def get_exam_questions_with_detail(exam_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT q.*, eq.question_order
        FROM exam_questions eq
        JOIN questions q ON eq.question_id = q.id
        WHERE eq.exam_id = %s
        ORDER BY eq.question_order
    """, (exam_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@router.delete("/{exam_id}")
def delete_exam_questions(exam_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exam_questions WHERE exam_id = %s", (exam_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Deleted"} 