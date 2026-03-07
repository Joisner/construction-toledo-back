import subprocess
import sqlalchemy
from google.cloud.sql.connector import Connector
from google.oauth2 import credentials

def verify_counts():
    result = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, shell=True)
    creds = credentials.Credentials(result.stdout.strip())
    
    instance_name = "project-f605efd3-c798-4a4b-9e0:europe-southwest1:toledo-db"
    connector = Connector(credentials=creds)
    
    def getconn():
        return connector.connect(instance_name, "pg8000", user="postgres", password="ToledoSecurePass2026!", db="TOLEDO")
    
    engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
    
    with engine.connect() as conn:
        tables = ['users', 'projects', 'project_media', 'services', 'quotes', 'budgets']
        for table in tables:
            try:
                res = conn.execute(sqlalchemy.text(f"SELECT COUNT(*) FROM public.{table}"))
                count = res.scalar()
                print(f"Table {table}: {count} rows")
            except Exception as e:
                print(f"Error checking {table}: {e}")

if __name__ == "__main__":
    verify_counts()
