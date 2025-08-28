from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import user_routes

#main.py → user_routes.py → user_service.py → main.py
# Load environment variables
#http://127.0.0.1:8000/users working

load_dotenv()

app = FastAPI(title="Connaq API", version="1.0")

# Root & health routes
@app.get("/")
async def root():
    return {"message": "Welcome to Connaq!"}

@app.get("/api/health")
async def health():
    return {"status": "OK"}

# Include user routes
app.include_router(user_routes.router, prefix="/user", tags=["Users"])
