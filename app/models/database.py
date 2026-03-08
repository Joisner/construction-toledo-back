import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from urllib.parse import urlparse, urlunparse, quote

# ---------------------------------------------------------------------------
# Database engine configuration
# ---------------------------------------------------------------------------
# Supports three modes:
#   1. SQLite       – DATABASE_URL starts with "sqlite" (local dev)
#   2. Cloud SQL    – INSTANCE_CONNECTION_NAME env var is set (production)
#   3. Standard PG  – DATABASE_URL is a postgresql:// URL (local Postgres)
# ---------------------------------------------------------------------------

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
INSTANCE_CONNECTION_NAME = settings.INSTANCE_CONNECTION_NAME

if INSTANCE_CONNECTION_NAME:
    # ── Cloud SQL via Python Connector (production on Cloud Run) ──────────
    from google.cloud.sql.connector import Connector

    connector = Connector()

    def _get_cloud_sql_conn():
        return connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=settings.DB_USER,
            password=settings.DB_PASS,
            db=settings.DB_NAME,
        )

    engine = create_engine(
        "postgresql+pg8000://",
        creator=_get_cloud_sql_conn,
    )

elif SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # ── SQLite (local development) ────────────────────────────────────────
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

else:
    # ── Standard PostgreSQL URL (local Postgres) ──────────────────────────
    try:
        parsed = urlparse(SQLALCHEMY_DATABASE_URL)
        if parsed.username or parsed.password:
            username = parsed.username or ""
            password = parsed.password or ""
            safe_username = quote(username, safe="")
            safe_password = quote(password, safe="")
            hostport = parsed.hostname or ""
            if parsed.port:
                hostport = f"{hostport}:{parsed.port}"
            netloc = f"{safe_username}:{safe_password}@{hostport}"
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