import os
import sys
import subprocess
from google.cloud.sql.connector import Connector
import sqlalchemy
from google.oauth2 import credentials
from passlib.context import CryptContext

# Configuration identical to app/core/security.py
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

def get_access_token():
    print("Getting access token from gcloud...")
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True,
        text=True,
        shell=True
    )
    if result.returncode != 0:
        print(f"Error getting access token: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def reset_password():
    new_password = "admin12345"
    hashed_password = pwd_context.hash(new_password)
    
    instance_name = "project-f605efd3-c798-4a4b-9e0:europe-southwest1:toledo-db"
    db_user = "postgres"
    db_pass = "ToledoSecurePass2026!"
    db_name = "TOLEDO"

    token = get_access_token()
    creds = credentials.Credentials(token)

    print(f"Connecting to {instance_name}...")
    connector = Connector(credentials=creds)

    def getconn():
        return connector.connect(
            instance_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name
        )

    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

    with engine.connect() as conn:
        print(f"Updating password for user 'admin'...")
        result = conn.execute(
            sqlalchemy.text("UPDATE public.users SET hashed_password = :hp WHERE username = :uname"),
            {"hp": hashed_password, "uname": "admin"}
        )
        conn.commit()
        if result.rowcount > 0:
            print("Password updated successfully.")
        else:
            print("User 'admin' not found in the database.")

if __name__ == "__main__":
    reset_password()
