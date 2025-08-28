from app.services.user_service import register_user
from app.models.user_schema import UserRegister
import pyodbc

new_user = UserRegister(
    FIRST_NAME="Phapda",
    USERNAME="Phapda123",
    EMAIL="Phapda@example.com",
    PASSWORD="Password123"
)

response = register_user(new_user)
print(response)
