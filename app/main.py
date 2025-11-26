from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, projects, services, quotes
from app.models.database import create_tables
from app.models.models import Base
from fastapi.staticfiles import StaticFiles
import os
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Create database tables
create_tables()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Temporary middleware to log raw request bodies for the login endpoint
# This runs before FastAPI dependency parsing, so it helps diagnose 422 issues
class _LoginBodyLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if request.url.path == f"{settings.API_V1_STR}/auth/login" and request.method == "POST":
                body = await request.body()
                # print raw bytes and decoded (if possible)
                print("---- Login raw body (bytes) ----")
                print(body)
                try:
                    print("---- Login raw body (decoded utf-8) ----")
                    print(body.decode('utf-8'))
                except Exception:
                    pass
                # recreate request so downstream can still read the body
                async def _receive():
                    # Properly mimic ASGI receive with the body and indicate no more
                    # body data (more_body=False) so downstream readers don't see
                    # an unexpected EndOfStream.
                    return {"type": "http.request", "body": body, "more_body": False}

                new_request = Request(request.scope, _receive)
                return await call_next(new_request)
        except Exception as exc:
            print("LoginBodyLogger error:", exc)
        return await call_next(request)


app.add_middleware(_LoginBodyLogger)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(services.router, prefix=f"{settings.API_V1_STR}/services", tags=["services"])
app.include_router(quotes.router, prefix=f"{settings.API_V1_STR}/quotes", tags=["quotes"])

@app.get("/")
def root():
    return {
        "message": "Welcome to Construction Company API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

# Serve uploaded media from the uploads/ folder
uploads_dir = os.path.abspath(os.path.join(os.getcwd(), "uploads"))
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")