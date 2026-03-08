import os
import sys
import subprocess
from google.cloud.sql.connector import Connector
import sqlalchemy
from google.oauth2 import credentials

def get_access_token():
    result = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def check_all_users():
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
        print("Listing all users...")
        result = conn.execute(sqlalchemy.text("SELECT id, username, hashed_password FROM public.users"))
        users = result.fetchall()
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Hash: {user[2]}")

if __name__ == "__main__":
    check_all_users()
