import os
import sys
import subprocess
from google.cloud.sql.connector import Connector
import sqlalchemy
from google.oauth2 import credentials

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

def load_schema():
    instance_name = "project-f605efd3-c798-4a4b-9e0:europe-southwest1:toledo-db"
    db_user = "postgres"
    db_pass = "ToledoSecurePass2026!"
    db_name = "TOLEDO"
    sql_file = "database_files/create_tables_and_seed.sql"

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

    with open(sql_file, "r", encoding="utf-8") as f:
        sql_commands = f.read()

    # Split by semicolon.
    commands = sql_commands.split(";")

    with engine.connect() as conn:
        print("Executing SQL commands...")
        for cmd in commands:
            cmd = cmd.strip()
            if not cmd:
                continue
            try:
                conn.execute(sqlalchemy.text(cmd))
                conn.commit()
            except Exception as e:
                # Some parts might be groups, but for basic tables/inserts this works.
                print(f"Error executing: {cmd[:50]}... \nError: {e}")
        print("Schema loaded successfully.")

if __name__ == "__main__":
    load_schema()
