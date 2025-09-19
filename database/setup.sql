-- Run with: sudo -u postgres psql -f setup.sql

-- Drop database if it already exists
DROP DATABASE titanpark_parking_system;

-- Create database
CREATE DATABASE titanpark_parking_system
  WITH
  OWNER = postgres
  TEMPLATE = template0;

-- Connect to database
\c titanpark_parking_system;

-- Create tables
-- ERD url: https://github.com/santi224m/Titan-Park-Documentation/blob/parking-system-architecture/diagrams/out/parking_system_erd_diagram.png
CREATE TABLE parking_structure (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE vehicle (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  make TEXT NOT NULL,
  model TEXT NOT NULL,
  year INT NOT NULL,
  color TEXT NOT NULL,
  license_plate TEXT NOT NULL
);

CREATE TABLE listing (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  post_date TIMESTAMP NOT NULL DEFAULT now(),
  price INT NOT NULL,
  structure_id INT NOT NULL REFERENCES parking_structure(id),
  floor INT NOT NULL CHECK (floor >= 1 AND floor <= 4),
  vehicle_id UUID NOT NULL REFERENCES vehicle(id),
  comment TEXT
);

-- Insert parking structures
INSERT INTO parking_structure (name) VALUES
  ('Nutwood Structure'),
  ('State College Structure'),
  ('Eastside North'),
  ('Eastside South');

-- Show created tables
\dt;

-- Show parking structures
SELECT * FROM parking_structure;

-- Display success message
SELECT 'Database setup completed successfully!' as status;