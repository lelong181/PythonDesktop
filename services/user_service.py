from services.api_client import get, post, put, delete, patch

def login(username, password):
    return post("/auth/login", json={"username": username, "password": password})

def get_user(user_id):
    return get(f"/users/{user_id}")

def get_users():
    return get("/users/")

def create_user(username, password, full_name, role):
    return post("/users/", json={
        "username": username,
        "password": password,
        "full_name": full_name,
        "role": role
    })

def update_user(user_id, data):
    return put(f"/users/{user_id}", json=data)

def delete_user(user_id):
    return delete(f"/users/{user_id}")

def change_password(user_id, new_password):
    return patch(f"/users/{user_id}/password", json={"new_password": new_password}) 