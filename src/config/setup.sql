-- Business Card Extraction Database Setup (PostgreSQL/Supabase)
-- This script creates the table for storing extracted business card information

-- Create the contacts table (database should already exist in Supabase)
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    designation VARCHAR(100),
    company VARCHAR(100),
    phone VARCHAR(50),
    email VARCHAR(100),
    website VARCHAR(100),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add index for better query performance
CREATE INDEX IF NOT EXISTS idx_name ON contacts(name);
CREATE INDEX IF NOT EXISTS idx_company ON contacts(company);
CREATE INDEX IF NOT EXISTS idx_created_at ON contacts(created_at);

-- Display table structure
\d contacts; 