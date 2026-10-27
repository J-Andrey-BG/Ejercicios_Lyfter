PRAGMA foreign_keys = ON;

-- Create tables
CREATE TABLE IF NOT EXISTS Authors (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Books (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Author INTEGER,
    FOREIGN KEY (Author) REFERENCES Authors(ID)
);

CREATE TABLE IF NOT EXISTS Customers (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Rents (
    ID INTEGER PRIMARY KEY,
    BookID INTEGER NOT NULL,
    CustomerID INTEGER NOT NULL,
    State TEXT NOT NULL,
    FOREIGN KEY (BookID) REFERENCES Books(ID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(ID)
);

-- Insert records
INSERT INTO Authors (ID, Name) VALUES
(1, 'Miguel de Cervantes'),
(2, 'Dante Alighieri'),
(3, 'Takehiko Inoue'),
(4, 'Akira Toriyama'),
(5, 'Walt Disney');

INSERT INTO Books (ID, Name, Author) VALUES
(1, 'Don Quijote', 1),
(2, 'La Divina Comedia', 2),
(3, 'Vagabond 1-3', 3),
(4, 'Dragon Ball 1', 4),
(5, 'The Book of the 5 Rings', NULL);

INSERT INTO Customers (ID, Name, Email) VALUES
(1, 'John Doe', 'j.doe@email.com'),
(2, 'Jane Doe', 'jane@doe.com'),
(3, 'Luke Skywalker', 'darth.son@email.com');

INSERT INTO Rents (ID, BookID, CustomerID, State) VALUES
(1, 1, 2, 'Returned'),
(2, 2, 2, 'Returned'),
(3, 1, 1, 'On time'),
(4, 3, 1, 'On time'),
(5, 2, 2, 'Overdue');

-- 1. Get all books and their authors, including books without an author
SELECT b.ID, b.Name AS Book, a.Name AS Author
FROM Books AS b
LEFT JOIN Authors AS a ON b.Author = a.ID
ORDER BY b.ID;

-- 2. Get all books without an author
SELECT b.ID, b.Name AS Book
FROM Books AS b
LEFT JOIN Authors AS a ON b.Author = a.ID
WHERE a.ID IS NULL
ORDER BY b.ID;

-- 3. Get all authors without books
SELECT a.ID, a.Name AS Author
FROM Authors AS a
LEFT JOIN Books AS b ON a.ID = b.Author
WHERE b.ID IS NULL
ORDER BY a.ID;

-- 4. Get all books that have ever been rented, without duplicates
SELECT DISTINCT b.ID, b.Name AS Book
FROM Books AS b
INNER JOIN Rents AS r ON b.ID = r.BookID
ORDER BY b.ID;

-- 5. Get all books that have never been rented
SELECT b.ID, b.Name AS Book
FROM Books AS b
LEFT JOIN Rents AS r ON b.ID = r.BookID
WHERE r.ID IS NULL
ORDER BY b.ID;

-- 6. Get all customers who have never rented a book
SELECT c.ID, c.Name AS Customer, c.Email
FROM Customers AS c
LEFT JOIN Rents AS r ON c.ID = r.CustomerID
WHERE r.ID IS NULL
ORDER BY c.ID;

-- 7. Get all books with an overdue rental, without duplicates
SELECT DISTINCT b.ID, b.Name AS Book
FROM Books AS b
INNER JOIN Rents AS r ON b.ID = r.BookID
WHERE r.State = 'Overdue'
ORDER BY b.ID;
