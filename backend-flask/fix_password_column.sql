-- Fix password_hash column size
ALTER TABLE users ALTER COLUMN password_hash TYPE VARCHAR(255);
