import pyodbc
from passlib.context import CryptContext
from app.models.user_schema import UserRegister, UserResponse
from app.connection.database import get_connection
from fastapi import HTTPException, status
#from app.utils.jwt_utils import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_all_users_from_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM USERS;")
    columns = [col[0].upper() for col in cursor.description]  # column names in uppercase
    rows = cursor.fetchall()
    conn.close()

    users = []
    for row in rows:
        row_dict = dict(zip(columns, row))  # map col name → value
        users.append(UserResponse(**row_dict))  # unpack dict directly into Pydantic model

    return users
#---------------------------------------------------------------------------------------------
#                               REGISTER USER
#---------------------------------------------------------------------
# Hash password
def hashing_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)

# Check if user exists with same first_name + email
def check_user_exists(first_name: str, email: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM USERS 
        WHERE FIRST_NAME = ? AND EMAIL = ?
    """, (first_name, email))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Get user by email (for login)
def get_user_by_email(email: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, FIRST_NAME, USERNAME, EMAIL, PASSWORD, CREATED_AT FROM USERS WHERE EMAIL = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    return row
#---------------------------------------------------------------------------------------------
#                             INSERTING USER IN DB
#---------------------------------------------------------------------------------------------
def register_user(user_data: UserRegister) -> UserResponse:
    if check_user_exists(user_data.first_name, user_data.email):
            raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,  # 409 = resource conflict
        detail="User with same name and email already exists."
    )

    ENCRYPTED_PASSWORD = hashing_password(user_data.password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO USERS (FIRST_NAME, USERNAME, EMAIL, PASSWORD)
        OUTPUT INSERTED.ID ,INSERTED.FIRST_NAME, INSERTED.USERNAME, INSERTED.EMAIL, INSERTED.CREATED_AT
        VALUES (?, ?, ?, ?)
    """, (
        user_data.first_name,
        user_data.username,
        user_data.email,
        ENCRYPTED_PASSWORD
    ))

    row = cursor.fetchone()
    conn.commit()
    conn.close()

     # Convert pyodbc.Row → dict (with uppercase keys)
    row_dict = dict(zip([column[0] for column in cursor.description], row))
    
     # Pass directly to Pydantic model (aliases will map automatically)
    return UserResponse(**row_dict)

######
#---------------------------------------------------------------------------------------------
#                        RETRIEVING PASSWORD BY FIRST_NAME
#---------------------------------------------------------------------

def get_user_password(first_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT PASSWORD FROM USERS WHERE FIRST_NAME = ?
    """, (first_name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None
