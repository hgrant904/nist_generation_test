-- Initial database setup for NIST Reports
-- This file contains example schema for reference

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Example: Users table
-- CREATE TABLE IF NOT EXISTS users (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     email VARCHAR(255) UNIQUE NOT NULL,
--     username VARCHAR(100) UNIQUE NOT NULL,
--     hashed_password VARCHAR(255) NOT NULL,
--     is_active BOOLEAN DEFAULT true,
--     is_superuser BOOLEAN DEFAULT false,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Example: Reports table
-- CREATE TABLE IF NOT EXISTS reports (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     user_id UUID REFERENCES users(id) ON DELETE CASCADE,
--     title VARCHAR(255) NOT NULL,
--     report_type VARCHAR(50) NOT NULL,
--     status VARCHAR(50) DEFAULT 'pending',
--     content JSONB,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Create indexes for better query performance
-- CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
-- CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);
-- CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
-- CREATE INDEX IF NOT EXISTS idx_reports_created_at ON reports(created_at);
