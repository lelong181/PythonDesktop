from fastapi import APIRouter, HTTPException
from api.models import User
from api.database import get_connection
from pydantic import BaseModel
import bcrypt

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=User)
def login(request: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (request.username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="Tài khoản không tồn tại")
    if not bcrypt.checkpw(request.password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Mật khẩu không đúng")
    return user 