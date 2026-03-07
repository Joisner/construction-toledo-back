import subprocess
import sqlalchemy
from google.cloud.sql.connector import Connector
from google.oauth2 import credentials

def verify_db():
    result = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, shell=True)
    creds = credentials.Credentials(result.stdout.strip())
    
    instance_name = "project-f605efd3-c798-4a4b-9e0:europe-southwest1:toledo-db"
    connector = Connector(credentials=creds)
    
    def getconn():
        return connector.connect(instance_name, "pg8000", user="postgres", password="ToledoSecurePass2026!", db="TOLEDO")
    
    engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
    
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        print(f"Tables in 'public' schema: {tables}")

if __name__ == "__main__":
    verify_db()
