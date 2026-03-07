import subprocess
import sqlalchemy
from google.cloud.sql.connector import Connector
from google.oauth2 import credentials

def check_admin_user():
    result = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, shell=True)
    creds = credentials.Credentials(result.stdout.strip())
    
    instance_name = "project-f605efd3-c798-4a4b-9e0:europe-southwest1:toledo-db"
    connector = Connector(credentials=creds)
    
    def getconn():
        return connector.connect(instance_name, "pg8000", user="postgres", password="ToledoSecurePass2026!", db="TOLEDO")
    
    engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
    
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT id, username, email, hashed_password, is_active FROM public.users"))
        users = [dict(row._mapping) for row in result]
        print(f"Users in DB: {users}")

if __name__ == "__main__":
    check_admin_user()
