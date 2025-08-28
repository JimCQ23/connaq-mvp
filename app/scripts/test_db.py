# app/scripts/test_db.py
from app.connection.database import get_connection

def test_select_users():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Try selecting from Users table (if exists)
        try:
            cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;")
            for row in cursor.fetchall():
                print(row)

            cursor.execute("SELECT * FROM Users;")
            rows = cursor.fetchall()
            if row:
                print("Connected. Sample row from Users:", row)
                for row in rows:
                    print(row)
            else:
                print("Connected. Users table exists but has no rows.")
        except Exception as e_table:
            # fallback: simple select to check connectivity
            print("Users table not queried (maybe doesn't exist). Trying simple SELECT 1. (table error:", e_table, ")")
            cursor.execute("SELECT 1;")
            print("SELECT 1 returned:", cursor.fetchone())
    except Exception as e:
        print("Connection/test failed:", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    test_select_users()
