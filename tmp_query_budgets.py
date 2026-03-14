from sqlalchemy import create_engine, text
db_url = "postgresql+pg8000://postgres:ToledoSecurePass2026!@34.175.249.237:5432/TOLEDO"
engine = create_engine(db_url)
try:
    with engine.connect() as conn:
        res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'budgets'")).fetchall()
        print("Columns in budgets:")
        for r in res:
            print(r[0])
except Exception:
    import traceback
    traceback.print_exc()
