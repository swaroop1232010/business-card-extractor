-- Business Card Extraction Database Setup
-- This script creates the database and table for storing extracted business card information

-- Create the database
CREATE DATABASE IF NOT EXISTS business_cards;
USE business_cards;

-- Create the contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
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
CREATE INDEX idx_name ON contacts(name);
CREATE INDEX idx_company ON contacts(company);
CREATE INDEX idx_created_at ON contacts(created_at);

-- Display table structure
DESCRIBE contacts; 