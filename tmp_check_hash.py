import os
import sys
import subprocess
from google.cloud.sql.connector import Connector
import sqlalchemy
from google.oauth2 import credentials

def get_access_token():
    result = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def check_admin_hash():
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

    with engine.connect() as conn:
        print("Checking admin hash...")
        result = conn.execute(sqlalchemy.text("SELECT username, hashed_password FROM public.users WHERE username = 'admin'"))
        user = result.fetchone()
        if user:
            print(f"User: {user[0]}, Hash: {user[1]}")
        else:
            print("Admin user not found.")

if __name__ == "__main__":
    check_admin_hash()
