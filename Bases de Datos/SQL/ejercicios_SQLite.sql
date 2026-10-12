-- Enables foreign key enforcement in SQLite
PRAGMA foreign_keys = ON;

-- =========================
-- TABLES
-- =========================

CREATE TABLE Users (
    buyer_email TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE Products (
    code INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL CHECK (price >= 0),
    entry_date TEXT NOT NULL,
    brand TEXT NOT NULL,
    stock_available INTEGER NOT NULL CHECK (stock_available >= 0)
);

CREATE TABLE Invoices (
    invoice_number INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_date TEXT NOT NULL,
    buyer_email TEXT NOT NULL,
    total_amount NUMERIC NOT NULL CHECK (total_amount >= 0),
    FOREIGN KEY (buyer_email) REFERENCES Users(buyer_email)
);

CREATE TABLE ProductsPerInvoice (
    product_code INTEGER NOT NULL,
    invoice_number INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total_amount NUMERIC NOT NULL CHECK (total_amount >= 0),

    PRIMARY KEY (invoice_number, product_code),

    FOREIGN KEY (product_code) REFERENCES Products(code),
    FOREIGN KEY (invoice_number) REFERENCES Invoices(invoice_number)
);

CREATE TABLE ShoppingCart (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_email TEXT NOT NULL UNIQUE,
    FOREIGN KEY (buyer_email) REFERENCES Users(buyer_email)
);

CREATE TABLE ProductsPerCart (
    product_code INTEGER NOT NULL,
    cart_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),

    PRIMARY KEY (cart_id, product_code),

    FOREIGN KEY (product_code) REFERENCES Products(code),
    FOREIGN KEY (cart_id) REFERENCES ShoppingCart(cart_id)
);

-- =========================
-- ALTER TABLE
-- =========================

ALTER TABLE Invoices
ADD COLUMN buyer_phone TEXT;

ALTER TABLE Invoices
ADD COLUMN cashier_employee_code TEXT;

-- =========================
-- SAMPLE DATA
-- =========================

INSERT INTO Users (buyer_email, name) VALUES
('ana@example.com', 'Ana Mora'),
('carlos@example.com', 'Carlos Ruiz'),
('maria@example.com', 'Maria Solano');

INSERT INTO Products (name, price, entry_date, brand, stock_available) VALUES
('Keyboard', 35000.00, '2026-10-01', 'Logitech', 20),
('Monitor', 125000.00, '2026-10-02', 'Samsung', 10),
('Laptop', 480000.00, '2026-10-03', 'Lenovo', 5),
('Mouse', 18000.00, '2026-10-04', 'Logitech', 30),
('Printer', 85000.00, '2026-10-05', 'Epson', 8);

INSERT INTO Invoices
(purchase_date, buyer_email, total_amount, buyer_phone, cashier_employee_code)
VALUES
('2026-10-05 10:30:00', 'ana@example.com', 195000.00, '8888-1111', 'EMP001'),
('2026-10-05 14:15:00', 'carlos@example.com', 498000.00, '8888-2222', 'EMP002'),
('2026-10-06 09:00:00', 'ana@example.com', 53000.00, '8888-1111', 'EMP001'),
('2026-10-06 16:45:00', 'maria@example.com', 210000.00, '8888-3333', 'EMP003');

INSERT INTO ProductsPerInvoice
(product_code, invoice_number, quantity, total_amount)
VALUES
(1, 1, 2, 70000.00),
(2, 1, 1, 125000.00),
(3, 2, 1, 480000.00),
(4, 2, 1, 18000.00),
(1, 3, 1, 35000.00),
(4, 3, 1, 18000.00),
(2, 4, 1, 125000.00),
(5, 4, 1, 85000.00);

INSERT INTO ShoppingCart (buyer_email) VALUES
('ana@example.com'),
('carlos@example.com'),
('maria@example.com');

INSERT INTO ProductsPerCart (product_code, cart_id, quantity) VALUES
(3, 1, 1),
(4, 1, 2),
(2, 2, 1),
(5, 3, 1);

-- =========================
-- SELECTS
-- =========================

-- 1. All stored products
SELECT *
FROM Products;

-- 2. Products with price greater than 50000
SELECT *
FROM Products
WHERE price > 50000;

-- 3. All purchases of the same product by id
SELECT *
FROM ProductsPerInvoice
WHERE product_code = 1;

-- 4. Purchases grouped by product with total quantity purchased
SELECT
    product_code,
    SUM(quantity) AS total_purchased
FROM ProductsPerInvoice
GROUP BY product_code;

-- 5. All invoices from the same buyer
SELECT *
FROM Invoices
WHERE buyer_email = 'ana@example.com';

-- 6. All invoices ordered by total amount descending
SELECT *
FROM Invoices
ORDER BY total_amount DESC;

-- 7. One invoice by invoice number
SELECT *
FROM Invoices
WHERE invoice_number = 1;

/*
SQLITE LIMITATIONS / DIFFERENCES

1. SQLite does not use MySQL AUTO_INCREMENT.
    INTEGER PRIMARY KEY already auto-generates integer identifiers.
    AUTOINCREMENT was added here so deleted identifiers are not reused.

2. SQLite uses type affinity rather than strict data types.
    NUMERIC is used for prices and totals. DECIMAL(p,s) is not enforced
    in the same strict way as in MySQL.

3. SQLite does not have a strict DATETIME storage class.
    Dates and times are stored as TEXT in ISO format:
    YYYY-MM-DD or YYYY-MM-DD HH:MM:SS.

4. ALTER TABLE in SQLite is more limited than in engines such as MySQL.
    ADD COLUMN is supported, so it is used for buyer_phone and
    cashier_employee_code.
*/
