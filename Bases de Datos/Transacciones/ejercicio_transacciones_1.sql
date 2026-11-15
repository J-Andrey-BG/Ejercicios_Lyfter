-- EXERCISE 1: DATABASE AND TABLE CREATION
--
-- STEP 1: Connect to the default "postgres" database.
-- Execute ONLY the next statement to create the database.
CREATE DATABASE transaction_practice;

-- STEP 2: Change your connection to "transaction_practice".
-- Then execute all statements BELOW this comment.

-- Users who can make purchases.
CREATE TABLE users (
    user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE
);

-- Products available for purchase.
CREATE TABLE products (
    product_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(12, 2) NOT NULL CHECK (price > 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

-- Bill header: one bill belongs to one user.
CREATE TABLE bills (
    bill_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (total >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
        CHECK (status IN ('ACTIVE', 'PARTIALLY_RETURNED', 'RETURNED'))
);

-- Bill details: one bill can contain multiple products.
-- returned_quantity records how many units have already been returned.
CREATE TABLE bill_items (
    bill_item_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    bill_id INTEGER NOT NULL REFERENCES bills(bill_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price > 0),
    returned_quantity INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT valid_returned_quantity
        CHECK (returned_quantity >= 0 AND returned_quantity <= quantity),
    CONSTRAINT unique_product_per_bill UNIQUE (bill_id, product_id)
);

-- Example users.
INSERT INTO users (full_name, email)
VALUES
    ('Ana Torres', 'ana@example.com'),
    ('Carlos Mora', 'carlos@example.com');

-- Example products. Prices are sample values in Costa Rican colones.
INSERT INTO products (name, price, stock)
VALUES
    ('Keyboard', 12500.00, 10),
    ('Mouse', 6500.00, 5),
    ('Monitor', 89000.00, 3);

-- Inspect the initial records.
SELECT * FROM users ORDER BY user_id;
SELECT * FROM products ORDER BY product_id;
SELECT * FROM bills ORDER BY bill_id;
SELECT * FROM bill_items ORDER BY bill_item_id;
