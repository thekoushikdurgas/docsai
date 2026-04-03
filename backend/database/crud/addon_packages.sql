-- CRUD examples: addon_packages — DDL: ../addon_packages.sql

-- SELECT
SELECT * FROM addon_packages WHERE is_active = TRUE;

-- INSERT
INSERT INTO addon_packages (id, name, credits, rate_per_credit, price)
VALUES (:id, :name, :credits, 0.02, 19.99);

-- UPDATE
UPDATE addon_packages SET is_active = FALSE, updated_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM addon_packages WHERE id = :id;
