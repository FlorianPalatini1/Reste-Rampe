-- Add mailbox management fields to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS mailbox_enabled BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mailbox_password_hash VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS mailbox_quota_mb INTEGER DEFAULT 5120;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mailbox_created_at TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mailbox_active BOOLEAN DEFAULT TRUE;

-- Add email verification fields if not exist
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_email_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR(255) UNIQUE;

SELECT 'Migration complete!' as status;
