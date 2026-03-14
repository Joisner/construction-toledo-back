from sqlalchemy import create_engine, text

db_url = "postgresql+pg8000://postgres:ToledoSecurePass2026!@34.175.249.237:5432/TOLEDO"
engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        # Check if invoices table exists
        res = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'invoices' ORDER BY ordinal_position")).fetchall()
        if res:
            print("Columns in 'invoices' table:")
            for r in res:
                print(f"  {r[0]:20s} {r[1]}")
        else:
            print("Table 'invoices' does NOT exist!")
            # List all tables
            tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")).fetchall()
            print("\nExisting tables:")
            for t in tables:
                print(f"  {t[0]}")
            
        # Try a direct SELECT
        print("\nTrying SELECT * FROM invoices LIMIT 1...")
        try:
            res2 = conn.execute(text("SELECT * FROM invoices LIMIT 1")).fetchall()
            print(f"Success! Got {len(res2)} rows")
            if res2:
                print("Columns:", res2[0]._fields if hasattr(res2[0], '_fields') else "unknown")
        except Exception as e:
            print(f"Error: {e}")
            
except Exception:
    import traceback
    traceback.print_exc()
