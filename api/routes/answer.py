from fastapi import APIRouter, HTTPException, Query
from api.models import Answer, AnswerCreate
from api.database import get_connection
from typing import List, Optional

router = APIRouter(prefix="/answers", tags=["answers"])

@router.get("/", response_model=List[Answer])
def get_answers(student_exam_id: Optional[int] = Query(None)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if student_exam_id:
        cursor.execute("SELECT * FROM student_answers WHERE student_exam_id = %s ORDER BY id DESC", (student_exam_id,))
    else:
        cursor.execute("SELECT * FROM student_answers ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@router.post("/", response_model=Answer)
def create_answer(answer: AnswerCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO student_answers (student_exam_id, question_id, selected_answer, is_correct) VALUES (%s, %s, %s, %s)",
        (answer.student_exam_id, answer.question_id, answer.selected_answer, answer.is_correct)
    )
    conn.commit()
    answer_id = cursor.lastrowid
    cursor.execute("SELECT * FROM student_answers WHERE id = %s", (answer_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row 