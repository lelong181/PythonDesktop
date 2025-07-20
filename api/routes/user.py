from fastapi import APIRouter, HTTPException, Body
from api.models import User, UserCreate
from api.database import get_connection
from typing import List
import bcrypt

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[User])
def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return row

@router.post("/", response_model=User)
def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Hash password
    password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute(
        "INSERT INTO users (username, password_hash, full_name, role) VALUES (%s, %s, %s, %s)",
        (user.username, password_hash, user.full_name, user.role)
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

@router.put("/{user_id}")
def update_user(user_id: int, data: dict = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()
    # Kiểm tra user có tồn tại không
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Cập nhật thông tin
    cursor.execute("""
        UPDATE users SET
            username = %s,
            full_name = %s,
            role = %s
        WHERE id = %s
    """, (
        data.get("username"),
        data.get("full_name"),
        data.get("role"),
        user_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User updated"}

@router.delete("/{user_id}")
def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    # Kiểm tra user có tồn tại không
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Xóa user
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User deleted"}

@router.patch("/{user_id}/password")
def change_password(user_id: int, data: dict = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()
    # Kiểm tra user có tồn tại không
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Hash password mới
    new_password = data.get("new_password")
    if not new_password:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="New password is required")
    
    password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Cập nhật password
    cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (password_hash, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Password changed"} 