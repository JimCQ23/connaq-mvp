import pyodbc
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_login(name, password):
    # DB connection
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS01;"
        "DATABASE=CONNAQ_DB;"
        "UID=DBUSER_ZAHRA;"
        "PWD=your_password_here;"
    )
    print("Connecting to database...")
    conn = pyodbc.connect(conn_str)
    print("✅ Connected!")
    
    cursor = conn.cursor()

    # Ensure matching case for column names
    cursor.execute(
        "SELECT USER_ID, USERNAME, PASSWORD FROM USERS WHERE USERNAME = ?",
        (name,)
    )
    row = cursor.fetchone()

    if not row:
        print("❌ User not found.")
        return
    
    db_user_id = row.USER_ID
    db_username = row.USERNAME
    db_password_hash = row.PASSWORD  # CAPS as in DB

    if bcrypt_context.verify(password, db_password_hash):
        print(f"✅ Login successful for {db_username} (User ID: {db_user_id})")
    else:
        print("❌ Invalid password.")

    conn.close()

if __name__ == "__main__":
    test_login("Phapda", "Password123")
