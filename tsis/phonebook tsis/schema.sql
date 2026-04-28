-- TSIS1 PhoneBook extended schema.
-- This file updates the old Practice 7-8 contacts table instead of deleting it.

-- Old projects usually already have contacts(id, name, phone).
-- IF NOT EXISTS lets this script run even on a new empty database.
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- New table for contact groups/categories.
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Default groups required by the task.
INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

-- New contact fields.
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email VARCHAR(100);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday DATE;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();

-- Name should be unique because JSON import duplicate handling is based on name.
CREATE UNIQUE INDEX IF NOT EXISTS contacts_name_unique ON contacts(name);

-- New 1-to-many table for multiple phone numbers.
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE (contact_id, phone)
);

-- If there is old data in contacts.phone from Practice 7,
-- copy it into phones as mobile numbers. The old phone column can remain unused.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'contacts' AND column_name = 'phone'
    ) THEN
        INSERT INTO phones (contact_id, phone, type)
        SELECT id, phone, 'mobile'
        FROM contacts
        WHERE phone IS NOT NULL AND phone <> ''
        ON CONFLICT DO NOTHING;
    END IF;
END $$;
