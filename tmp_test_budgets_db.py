import os
from dotenv import load_dotenv

load_dotenv()
os.environ["INSTANCE_CONNECTION_NAME"] = "project-f605efd3-c798-4a4b-9e0:europe-southwest1:toledo-db"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASS"] = "ToledoSecurePass2026!"
os.environ["DB_NAME"] = "TOLEDO"

import app.core.config
app.core.config.settings.INSTANCE_CONNECTION_NAME = os.environ["INSTANCE_CONNECTION_NAME"]
app.core.config.settings.DB_USER = os.environ["DB_USER"]
app.core.config.settings.DB_PASS = os.environ["DB_PASS"]
app.core.config.settings.DB_NAME = os.environ["DB_NAME"]

from app.models.database import SessionLocal
from app.models import models

def check_budgets():
    print("Testing DB Connection to budgets...")
    try:
        db = SessionLocal()
        budgets = db.query(models.Budget).all()
        print("Success, found", len(budgets), "budgets.")
    except Exception as e:
        print("Error during DB query:")
        import traceback
        traceback.print_exc()

check_budgets()
