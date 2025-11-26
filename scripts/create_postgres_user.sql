-- Script to create database user and grant privileges for TOLEDO
-- Replace 'tu_contraseña_segura' with a strong password

-- Run as a superuser (e.g., psql -U postgres -f create_postgres_user.sql)

CREATE USER toledo_user WITH PASSWORD 'tu_contraseña_segura';
GRANT CONNECT ON DATABASE TOLEDO TO toledo_user;
\c TOLEDO
CREATE SCHEMA IF NOT EXISTS public AUTHORIZATION toledo_user;
ALTER DATABASE TOLEDO OWNER TO toledo_user;
GRANT ALL PRIVILEGES ON DATABASE TOLEDO TO toledo_user;

-- For objects in the schema, run the following after tables are created:
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO toledo_user;
-- GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO toledo_user;
