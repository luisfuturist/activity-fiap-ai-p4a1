-- Truncate all tables in the public schema.  USE WITH EXTREME CAUTION!
-- This will DELETE all data.  Always back up your database first.
DO $$
DECLARE
  tbl_name TEXT;
BEGIN
  FOR tbl_name IN
    SELECT tablename
    FROM pg_tables
    WHERE schemaname = 'public'
  LOOP
    EXECUTE FORMAT('TRUNCATE TABLE %I RESTART IDENTITY CASCADE;', tbl_name);
  END LOOP;
END $$;


-- Delete all tables from the public schema.  USE WITH EXTREME CAUTION!
-- This will DELETE all data.  Always back up your database first.
DO $$
DECLARE
  tbl_name TEXT;
BEGIN
    FOR tbl_name IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        EXECUTE FORMAT('DROP TABLE %I CASCADE;', tbl_name);
    END LOOP;
END $$;