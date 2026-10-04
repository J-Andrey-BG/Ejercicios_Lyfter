CREATE TABLE `Products`(
    `Code` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(255) NOT NULL,
    `Price` DECIMAL(8, 2) NOT NULL,
    `Entry date` DATETIME NOT NULL,
    `Brand` VARCHAR(255) NOT NULL,
    `Stock available` INT NOT NULL
);
CREATE TABLE `Invoices`(
    `Invoice Number` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Purchase date` DATETIME NOT NULL,
    `Buyer email` VARCHAR(255) NOT NULL,
    `Total amount` DECIMAL(8, 2) NOT NULL
);
CREATE TABLE `Products Per Invoice`(
    `Product code` INT UNSIGNED NOT NULL,
    `Invoice number` INT UNSIGNED NOT NULL,
    `Quantity` INT NOT NULL,
    `Total amount` DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY(`Invoice number`, `Product code`)
);
CREATE TABLE `Shopping Cart`(
    `Cart ID` INT NOT NULL,
    `Buyer email` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`Cart ID`)
);
ALTER TABLE
    `Shopping Cart` ADD UNIQUE `shopping cart_buyer email_unique`(`Buyer email`);
CREATE TABLE `Products Per Cart`(
    `Product code` INT UNSIGNED NOT NULL,
    `Cart ID` INT NOT NULL,
    `Quantity` INT NOT NULL,
    PRIMARY KEY(`Cart ID`, `Product code`)
);
CREATE TABLE `Users`(
    `Buyer email` VARCHAR(255) NOT NULL,
    `Name` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`Buyer email`)
);
ALTER TABLE
    `Products Per Cart` ADD CONSTRAINT `products per cart_cart id_foreign` FOREIGN KEY(`Cart ID`) REFERENCES `Shopping Cart`(`Cart ID`);
ALTER TABLE
    `Products Per Invoice` ADD CONSTRAINT `products per invoice_invoice number_foreign` FOREIGN KEY(`Invoice number`) REFERENCES `Invoices`(`Invoice Number`);
ALTER TABLE
    `Products Per Cart` ADD CONSTRAINT `products per cart_product code_foreign` FOREIGN KEY(`Product code`) REFERENCES `Products`(`Code`);
ALTER TABLE
    `Shopping Cart` ADD CONSTRAINT `shopping cart_buyer email_foreign` FOREIGN KEY(`Buyer email`) REFERENCES `Users`(`Buyer email`);
ALTER TABLE
    `Products Per Invoice` ADD CONSTRAINT `products per invoice_product code_foreign` FOREIGN KEY(`Product code`) REFERENCES `Products`(`Code`);
ALTER TABLE
    `Invoices` ADD CONSTRAINT `invoices_buyer email_foreign` FOREIGN KEY(`Buyer email`) REFERENCES `Users`(`Buyer email`);