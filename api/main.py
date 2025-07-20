from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import subject, exam, question, user, answer, auth, student_exam, exam_question

app = FastAPI(title="Exam Bank API", version="1.0")

# CORS cho phép truy cập từ client local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subject.router)
app.include_router(exam.router)
app.include_router(question.router)
app.include_router(user.router)
app.include_router(answer.router)
app.include_router(auth.router)
app.include_router(student_exam.router)
app.include_router(exam_question.router)

@app.get("/")
def root():
    return {"message": "Welcome to Exam Bank API"} 