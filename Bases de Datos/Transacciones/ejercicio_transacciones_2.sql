-- EXERCISE 2: PURCHASE TRANSACTION
-- Run this file while connected to the "transaction_practice" database.
-- Edit the user ID, product IDs, and quantities below for each test.

-- If any step raises an exception, the transaction is rolled back.
BEGIN;

DO $$
DECLARE
    -- Purchase inputs: the positions in both arrays must match.
    v_user_id INTEGER := 1;
    v_product_ids INTEGER[] := ARRAY[1, 2];
    v_quantities INTEGER[] := ARRAY[2, 1];

    -- Working variables.
    v_item_count INTEGER;
    v_index INTEGER;
    v_bill_id INTEGER;
    v_unit_price NUMERIC(12, 2);
    v_available_stock INTEGER;
    v_bill_total NUMERIC(12, 2) := 0;
BEGIN
    -- Validate the input arrays.
    v_item_count := COALESCE(array_length(v_product_ids, 1), 0);

    IF v_item_count = 0 THEN
        RAISE EXCEPTION 'The purchase must contain at least one product.';
    END IF;

    IF v_item_count <> COALESCE(array_length(v_quantities, 1), 0) THEN
        RAISE EXCEPTION 'Product IDs and quantities must have the same length.';
    END IF;

    -- Validate the user before creating the bill.
    PERFORM 1 FROM users WHERE user_id = v_user_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'User % does not exist.', v_user_id;
    END IF;

    -- Validate positive quantities, IDs, and duplicate product IDs.
    FOR v_index IN 1..v_item_count LOOP
        IF v_product_ids[v_index] IS NULL THEN
            RAISE EXCEPTION 'A product ID cannot be NULL.';
        END IF;

        IF v_quantities[v_index] IS NULL OR v_quantities[v_index] <= 0 THEN
            RAISE EXCEPTION 'Quantity must be positive for product %.',
                v_product_ids[v_index];
        END IF;

        IF array_position(v_product_ids, v_product_ids[v_index]) <> v_index THEN
            RAISE EXCEPTION 'Product % was entered more than once.',
                v_product_ids[v_index];
        END IF;
    END LOOP;

    -- Create the bill header. All changes will be undone if a later step fails.
    INSERT INTO bills (user_id, total, status)
    VALUES (v_user_id, 0, 'ACTIVE')
    RETURNING bill_id INTO v_bill_id;

    -- Check stock and record each line item.
    FOR v_index IN 1..v_item_count LOOP
        -- Lock the product row until the transaction ends.
        SELECT price, stock
        INTO v_unit_price, v_available_stock
        FROM products
        WHERE product_id = v_product_ids[v_index]
        FOR UPDATE;

        IF NOT FOUND THEN
            RAISE EXCEPTION 'Product % does not exist.',
                v_product_ids[v_index];
        END IF;

        IF v_available_stock < v_quantities[v_index] THEN
            RAISE EXCEPTION 'Insufficient stock for product %. Available: %, requested: %.',
                v_product_ids[v_index],
                v_available_stock,
                v_quantities[v_index];
        END IF;

        INSERT INTO bill_items (bill_id, product_id, quantity, unit_price)
        VALUES (
            v_bill_id,
            v_product_ids[v_index],
            v_quantities[v_index],
            v_unit_price
        );

        UPDATE products
        SET stock = stock - v_quantities[v_index]
        WHERE product_id = v_product_ids[v_index];

        v_bill_total := v_bill_total + v_unit_price * v_quantities[v_index];
    END LOOP;

    -- Save the calculated total after inserting all items.
    UPDATE bills
    SET total = v_bill_total
    WHERE bill_id = v_bill_id;

    RAISE NOTICE 'Purchase completed. Bill ID: %, total: %.',
        v_bill_id, v_bill_total;
END
$$;

COMMIT;

-- Optional queries to inspect results:
-- SELECT * FROM products ORDER BY product_id;
-- SELECT * FROM bills ORDER BY bill_id;
-- SELECT * FROM bill_items ORDER BY bill_item_id;
