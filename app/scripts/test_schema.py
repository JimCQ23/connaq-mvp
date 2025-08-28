# scripts/test_schema.py
from app.models.user_schema import UserRegister, UserLogin, UserResponse

# ✅ Test UserCreate
try:
    user_data = UserRegister(
        FIRST_NAME="Dora",
        USERNAME="dorahusain",
        EMAIL="dora.husain@example.com",
        PASSWORD="mypassword123!"
    )
    print("UserCreate:", user_data.model_dump())
except Exception as e:
    print("UserCreate Error:", e)

# ✅ Test UserLogin
try:
    login_data = UserLogin(
        USERNAME="zahrahusain",
        PASSWORD="mypassword123!"
    )
    print("UserLogin:", login_data.model_dump())
except Exception as e:
    print("UserLogin Error:", e)

# ✅ Test UserResponse
try:
    response_data = UserResponse(
        USER_ID=1,
        FIRST_NAME="Dora",
        USERNAME="dorahusain",
        EMAIL="dora.husain@example.com"
    )
    print("UserResponse:", response_data.model_dump())
except Exception as e:
    print("UserResponse Error:", e)
