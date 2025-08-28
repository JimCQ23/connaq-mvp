from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Schema for user registration
class UserRegister(BaseModel):
    first_name: str = Field(..., alias="FIRST_NAME", max_length=50)
    username: str = Field(..., alias="USERNAME", max_length=50)
    email: EmailStr = Field(..., alias="EMAIL")
    password: str = Field(..., alias="PASSWORD", max_length=255)
    class Config:
        allow_population_by_field_name = True  # Allows using either field or alias names
        from_attributes = True


# Schema for login
class UserLogin(BaseModel):
    username: str = Field(..., alias="USERNAME", max_length=100)
    password: str = Field(..., alias="PASSWORD", max_length=255)
    class Config:
        allow_population_by_field_name = True
        from_attributes = True

# Schema for DB model / response (optional)
class UserResponse(BaseModel):
    user_id: int|None = Field(..., alias="ID")
    first_name: str = Field(..., alias="FIRST_NAME")
    username: str = Field(..., alias="USERNAME")
    email: EmailStr = Field(..., alias="EMAIL")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        from_attributes = True

class LoginRequest(BaseModel):
    first_name: str = Field(..., alias="FIRST_NAME")
    password: str = Field(..., alias="PASSWORD")
    class Config:
        allow_population_by_field_name = True
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"