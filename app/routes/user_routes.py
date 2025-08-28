# app/routes/user_routes.py
from fastapi import APIRouter, HTTPException
from app.models.user_schema import UserRegister, UserResponse, LoginRequest, TokenResponse
from app.services.user_service import register_user, verify_password, get_all_users_from_db
from app.connection.database import get_connection
from app.utils.jwt_utils import create_access_token
from typing import List

#from app.utils.jwt_utils import create_access_token

router = APIRouter()

# user_routes.py
@router.get("/all", response_model=List[UserResponse])
def get_all_users():
    return get_all_users_from_db()  # implemented in user_service.py


# ---------------------------------------------------------
#                       User Registration
# ---------------------------------------------------------
@router.post("/register", response_model=UserResponse)
def register(user: UserRegister):
    return register_user(user)


# ---------------------------------------------------------
#                    User Login (name + password)
# ---------------------------------------------------------
@router.post("/login", response_model=TokenResponse)
def login(login_req: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ID, FIRST_NAME, PASSWORD 
        FROM USERS 
        WHERE LOWER(FIRST_NAME) = LOWER(?)
    """, (login_req.first_name,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    user_id, db_name, db_password = row

    if not verify_password(login_req.password, db_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({"sub": db_name})

    return TokenResponse(access_token=token)  # ✅ matches your response_model


