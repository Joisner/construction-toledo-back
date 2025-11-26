# Construction Company Backend API

Backend API for the Construction Company website built with FastAPI.

## Features

- Admin authentication and authorization
- Project management (CRUD operations)
- Service management (CRUD operations)
- Quote management
- File uploads for project images

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file with the following variables:
   ```
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

Postgres quick setup (example)
1. Create database and user (run these commands in a psql shell as a superuser):

```sql
-- create database TOLEDO and a dedicated user
CREATE DATABASE TOLEDO;
CREATE USER toledo_user WITH PASSWORD 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON DATABASE TOLEDO TO toledo_user;
```

Or use the provided script `scripts/create_postgres_user.sql`:

```bash
psql -U postgres -f scripts/create_postgres_user.sql
```

2. Set `DATABASE_URL` in `.env` to point to the new DB, e.g.:

```
DATABASE_URL=postgresql://toledo_user:tu_contraseña_segura@localhost:5432/TOLEDO
```

3. Start the server; the app will create tables automatically in development (SQLite or PostgreSQL depending on `DATABASE_URL`):

```powershell
Set-Location -Path 'C:\Users\Familia Gonzalez\Documents\Projects\Backend\backend-construction-toledo'
uvicorn app.main:app --reload
```

If you prefer migrations for production, initialize Alembic (see next section).

Media endpoints
----------------
- Single media upload: POST /api/v1/projects/{project_id}/media (multipart file + optional `description` and `is_before`)
- Batch upload: POST /api/v1/projects/{project_id}/media/batch (multipart files array `files[]` + optional `description` and `is_before`)
- Delete media: DELETE /api/v1/projects/{project_id}/media/{media_id}

Uploaded files are served from `/uploads/...` (local disk). In production you should use S3 or another object store.

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`