from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from urllib.parse import urlparse, urlunparse, quote

# If the DATABASE_URL contains non-ASCII chars in username/password (for example
# accented characters), some DB drivers can fail when interpreting the DSN. We
# percent-encode username and password parts when a PostgreSQL URL is used.

# Read the database URL from settings (from .env). If you set DATABASE_URL to
# a PostgreSQL URL (eg. postgresql://user:pass@host:port/TOLEDO) the engine will
# connect to Postgres. If you leave the default (sqlite), we keep using a
# local file for development.
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# For SQLite we need to pass check_same_thread; for other DBs we don't.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Try to ensure credentials (user:pass) are percent-encoded to avoid
    # UnicodeDecodeError in the DB driver if the password contains non-ascii
    # characters. This will only modify the netloc userinfo part.
    try:
        parsed = urlparse(SQLALCHEMY_DATABASE_URL)
        if parsed.username or parsed.password:
            username = parsed.username or ""
            password = parsed.password or ""
            # only quote if necessary
            safe_username = quote(username, safe="")
            safe_password = quote(password, safe="")
            # rebuild netloc: user:pass@host:port
            hostport = parsed.hostname or ""
            if parsed.port:
                hostport = f"{hostport}:{parsed.port}"
            netloc = f"{safe_username}:{safe_password}@{hostport}"
            # assemble new URL
            parsed = parsed._replace(netloc=netloc)
            safe_url = urlunparse(parsed)
        else:
            safe_url = SQLALCHEMY_DATABASE_URL
    except Exception:
        safe_url = SQLALCHEMY_DATABASE_URL

    engine = create_engine(safe_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper to create tables (used in development). In production prefer Alembic
# migrations instead of create_all.
def create_tables():
    Base.metadata.create_all(bind=engine)