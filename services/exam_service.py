from services.api_client import get, post, delete

def get_exams():
    return get("/exams/")

def get_exam(exam_id):
    return get(f"/exams/{exam_id}")

def create_exam(exam_code, subject_id, title, duration, total_questions, created_by):
    return post("/exams/", json={
        "exam_code": exam_code,
        "subject_id": subject_id,
        "title": title,
        "duration": duration,
        "total_questions": total_questions,
        "created_by": created_by
    })

def get_exam_by_code(exam_code):
    exams = get_exams()
    for exam in exams:
        if exam['exam_code'] == exam_code:
            return exam
    return None

def delete_exam(exam_id):
    return delete(f"/exams/{exam_id}")

def get_exam_by_id(exam_id):
    return get_exam(exam_id) 