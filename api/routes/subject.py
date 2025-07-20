from fastapi import APIRouter, HTTPException
from api.models import Subject, SubjectCreate
from api.database import get_connection
from typing import List

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.get("/", response_model=List[Subject])
def get_subjects():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM subjects ORDER BY name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@router.get("/{subject_id}", response_model=Subject)
def get_subject(subject_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM subjects WHERE id = %s", (subject_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Subject not found")
    return row

@router.post("/", response_model=Subject)
def create_subject(subject: SubjectCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO subjects (name, code, description) VALUES (%s, %s, %s)",
        (subject.name, subject.code, subject.description)
    )
    conn.commit()
    subject_id = cursor.lastrowid
    cursor.execute("SELECT * FROM subjects WHERE id = %s", (subject_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row 