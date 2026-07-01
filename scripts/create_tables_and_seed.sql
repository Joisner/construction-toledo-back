-- Create tables for Construction Toledo

-- users
CREATE TABLE IF NOT EXISTS public.users (
  id TEXT PRIMARY KEY,
  username VARCHAR UNIQUE,
  email VARCHAR UNIQUE,
  hashed_password VARCHAR,
  is_active BOOLEAN DEFAULT TRUE,
  is_admin BOOLEAN DEFAULT FALSE
);

-- projects
CREATE TABLE IF NOT EXISTS public.projects (
  id TEXT PRIMARY KEY,
  title VARCHAR,
  description TEXT,
  location VARCHAR,
  service VARCHAR,
  completion_date TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- project_media
CREATE TABLE IF NOT EXISTS public.project_media (
  id TEXT PRIMARY KEY,
  project_id TEXT REFERENCES public.projects(id),
  file_url VARCHAR,
  mime VARCHAR,
  media_type VARCHAR,
  description TEXT,
  is_before BOOLEAN,
  created_at TIMESTAMP DEFAULT now()
);

-- services
CREATE TABLE IF NOT EXISTS public.services (
  id TEXT PRIMARY KEY,
  title VARCHAR,
  description TEXT,
  details TEXT,
  image_url VARCHAR,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- quotes
CREATE TABLE IF NOT EXISTS public.quotes (
  id TEXT PRIMARY KEY,
  name VARCHAR,
  email VARCHAR,
  phone VARCHAR,
  service VARCHAR,
  message TEXT,
  status VARCHAR DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Sample inserts (replace passwords appropriately).
-- Users: create an admin placeholder (use register endpoint to set a proper password)
INSERT INTO public.users (id, username, email, hashed_password, is_active, is_admin)
VALUES ('admin-1', 'admin', 'admin@localhost', '$pbkdf2-sha256$29000$sJYyJgSAkHJOibEWwtj7fw$4icEsM6.E5EH1w2jDXpKm39Kfmzxu4A3zgyst0XA0o8', true, true)
ON CONFLICT (id) DO NOTHING;

-- Sample service
INSERT INTO public.services (id, title, description, details, image_url, is_active)
VALUES ('serv-1', 'Reforma Cocina', 'Reforma integral de cocina', 'Detalles de servicio', '', true)
ON CONFLICT (id) DO NOTHING;

-- Sample project
INSERT INTO public.projects (id, title, description, location, service, completion_date, is_active)
VALUES ('proj-1', 'Casa Perez', 'Reforma completa de vivienda', 'Calle Falsa 123', 'Reforma Cocina', now(), true)
ON CONFLICT (id) DO NOTHING;

-- Sample media (antes y despues placeholders)
INSERT INTO public.project_media (id, project_id, file_url, mime, media_type, description, is_before)
VALUES ('media-1', 'proj-1', '/uploads/projects/proj-1/before1.jpg', 'image/jpeg', 'image', 'Antes - fachada', true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.project_media (id, project_id, file_url, mime, media_type, description, is_before)
VALUES ('media-2', 'proj-1', '/uploads/projects/proj-1/after1.jpg', 'image/jpeg', 'image', 'Despues - fachada', false)
ON CONFLICT (id) DO NOTHING;

-- Sample quote
INSERT INTO public.quotes (id, name, email, phone, service, message, status)
VALUES ('quote-1', 'Cliente Ejemplo', 'cliente@example.com', '600000000', 'Reforma Cocina', 'Quisiera presupuesto', 'pending')
ON CONFLICT (id) DO NOTHING;

-- budgets
CREATE TABLE IF NOT EXISTS public.budgets (
  id TEXT PRIMARY KEY,
  number VARCHAR,
  date TIMESTAMP,
  clientName VARCHAR,
  clientAddress TEXT,
  clientDNI VARCHAR,
  clientPhone VARCHAR,
  clientEmail VARCHAR,
  items JSONB,
  taxRate VARCHAR,
  validUntil TIMESTAMP,
  conditions TEXT,
  iban VARCHAR,
  created_at TIMESTAMP DEFAULT now()
);

-- Sample budget
INSERT INTO public.budgets (id, number, date, clientName, clientAddress, clientDNI, clientPhone, clientEmail, items, taxRate, validUntil, conditions, iban, created_at)
VALUES (
  'budget-1',
  'BUD-2026-001',
  now(),
  'Cliente Presupuesto',
  'Calle Presupuesto 1',
  '12345678A',
  '600111222',
  'cliente.bud@example.com',
  '[{"description": "Trabajo A", "qty": 1, "unit_price": 1200.00}]',
  '21%',
  now() + interval '30 days',
  'Condiciones generales',
  'ES0012345678901234567890',
  now()
)
ON CONFLICT (id) DO NOTHING;

-- invoices
CREATE TABLE IF NOT EXISTS public.invoices (
  id TEXT PRIMARY KEY,
  number VARCHAR,
  date TIMESTAMP,
  clientName VARCHAR,
  clientAddress TEXT,
  clientDNI VARCHAR,
  clientPhone VARCHAR,
  clientEmail VARCHAR,
  items JSONB,
  taxRate VARCHAR,
  iban VARCHAR,
  created_at TIMESTAMP DEFAULT now()
);

-- Sample invoice
INSERT INTO public.invoices (id, number, date, clientName, clientAddress, clientDNI, clientPhone, clientEmail, items, taxRate, iban, created_at)
VALUES (
  'invoice-1',
  'INV-2026-001',
  now(),
  'Cliente Factura',
  'Calle Factura 2',
  '87654321B',
  '600333444',
  'cliente.inv@example.com',
  '[{"description": "Trabajo B", "qty": 2, "unit_price": 450.00}]',
  '21%',
  'ES0098765432109876543210',
  now()
)
ON CONFLICT (id) DO NOTHING;
