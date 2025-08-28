from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt_utils import decode_access_token
from fastapi import APIRouter, HTTPException

# 1️⃣ Define the router
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.get("/user/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['sub']}"}
