from services.api_client import get, post, put

def get_student_exams(student_id=None, exam_id=None):
    if student_id:
        return get(f"/student_exams/?student_id={student_id}")
    if exam_id:
        return get(f"/student_exams/?exam_id={exam_id}")
    return get("/student_exams/")

def create_student_exam(student_id, exam_id, start_time=None):
    data = {"student_id": student_id, "exam_id": exam_id}
    if start_time:
        data["start_time"] = start_time
    return post("/student_exams/", json=data)

def update_student_exam_score(student_exam_id, score, status="completed"):
    data = {"score": score, "status": status}
    return put(f"/student_exams/{student_exam_id}", json=data)