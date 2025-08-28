# app/connection/database.py
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
ODBC_DRIVER = os.getenv("ODBC_DRIVER")


def build_conn_str():
    # If a port is provided use server,port format. If server contains backslash (named instance), use it as-is.
    if DB_PORT:
        server_part = f"{DB_SERVER},{DB_PORT}"
    else:
        server_part = DB_SERVER
    conn_str = (
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={server_part};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "TrustServerCertificate=YES;"
    )
    return conn_str

def get_connection():
    """
    Creates and returns a new database connection.
    """
    try:
        conn_str = build_conn_str()
        print(f"Connecting to {DB_SERVER} (DB: {DB_NAME}) with driver {ODBC_DRIVER}...")
        print(f"pyodbc version: {pyodbc.version}")
        
        # Set timeout to 5 seconds
        conn = pyodbc.connect(conn_str, autocommit=False, timeout=8)
        print("✅ Connected!")
        return conn
    except pyodbc.Error as e:
        print("❌ Database connection failed.")
        print(f"Error details: {e}")
        raise
