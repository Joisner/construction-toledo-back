import os
import sys
import subprocess
from google.cloud.sql.connector import Connector
import sqlalchemy
from google.oauth2 import credentials
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

def get_access_token():
    result = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def force_reset_admin():
    instance_name = "project-f605efd3-c798-4a4b-9e0:europe-southwest1:toledo-db"
    db_user = "postgres"
    db_pass = "ToledoSecurePass2026!"
    db_name = "TOLEDO"

    token = get_access_token()
    creds = credentials.Credentials(token)
    connector = Connector(credentials=creds)

    def getconn():
        return connector.connect(instance_name, "pg8000", user=db_user, password=db_pass, db=db_name)

    engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
    
    hashed_password = pwd_context.hash("123456")

    with engine.connect() as conn:
        print("Cleaning up any existing admin users...")
        conn.execute(sqlalchemy.text("DELETE FROM public.users WHERE username = 'admin'"))
        
        print("Inserting fresh admin user...")
        conn.execute(
            sqlalchemy.text("INSERT INTO public.users (id, username, email, hashed_password, is_active, is_admin) VALUES (:id, :username, :email, :password, :active, :admin)"),
            {
                "id": "admin-final",
                "username": "admin",
                "email": "admin@construction-toledo.com",
                "password": hashed_password,
                "active": True,
                "admin": True
            }
        )
        conn.commit()
        print("Admin user recreated successfully.")

if __name__ == "__main__":
    force_reset_admin()
