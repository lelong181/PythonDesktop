from services.api_client import get, post

def get_subjects():
    return get("/subjects/")

def get_subject(subject_id):
    return get(f"/subjects/{subject_id}")

def create_subject(name, code, description=None):
    return post("/subjects/", json={"name": name, "code": code, "description": description}) 