from app.services.user_service import verify_password
from app.utils.jwt_utils import create_access_token, decode_access_token
from app.connection.database import get_connection

def test_login(name: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch user by FIRST_NAME
    cursor.execute("""
        SELECT ID, FIRST_NAME, PASSWORD FROM USERS 
        WHERE LOWER(FIRST_NAME) = LOWER(?)
    """, (name,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("❌ User not found")
        return

    user_id, db_name, db_password = row

    # Verify password
    if not verify_password(password, db_password):
        print("❌ Incorrect password")
        return

    # Create JWT token
    token = create_access_token({"sub": db_name})
    print("✅ Login successful!")
    print("User ID:", user_id)
    print("Token:", token)

    # Simulate protected route
    payload = decode_access_token(token)
    if not payload:
        print("❌ Token invalid")
    else:
        print("🔒 Accessing protected route...")
        print("Hello", payload["sub"], "🎉")

if __name__ == "__main__":
    # Test with sample credentials
    test_login("Sharmila", "Password123")
