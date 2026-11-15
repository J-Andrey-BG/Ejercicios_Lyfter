-- EXERCISE 3: PRODUCT RETURN TRANSACTION
-- Run this file while connected to the "transaction_practice" database.
-- Edit bill ID, product IDs, and return quantities below for each test.
-- A bill is RETURNED only when all purchased units have been returned.

BEGIN;

DO $$
DECLARE
    -- Return inputs: each product ID matches a quantity at the same position.
    v_bill_id INTEGER := 1;
    v_product_ids INTEGER[] := ARRAY[1, 2];
    v_return_quantities INTEGER[] := ARRAY[1, 1];

    -- Working variables.
    v_item_count INTEGER;
    v_index INTEGER;
    v_bill_status VARCHAR(20);
    v_purchased_quantity INTEGER;
    v_already_returned INTEGER;
    v_remaining_quantity INTEGER;
    v_new_status VARCHAR(20);
BEGIN
    -- Validate the input arrays.
    v_item_count := COALESCE(array_length(v_product_ids, 1), 0);

    IF v_item_count = 0 THEN
        RAISE EXCEPTION 'The return must contain at least one product.';
    END IF;

    IF v_item_count <> COALESCE(array_length(v_return_quantities, 1), 0) THEN
        RAISE EXCEPTION 'Product IDs and return quantities must have the same length.';
    END IF;

    -- Lock the bill so two returns cannot modify it simultaneously.
    SELECT status
    INTO v_bill_status
    FROM bills
    WHERE bill_id = v_bill_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Bill % does not exist.', v_bill_id;
    END IF;

    IF v_bill_status = 'RETURNED' THEN
        RAISE EXCEPTION 'Bill % has already been fully returned.', v_bill_id;
    END IF;

    -- Validate quantities, product IDs, and duplicate entries.
    FOR v_index IN 1..v_item_count LOOP
        IF v_product_ids[v_index] IS NULL THEN
            RAISE EXCEPTION 'A product ID cannot be NULL.';
        END IF;

        IF v_return_quantities[v_index] IS NULL
           OR v_return_quantities[v_index] <= 0 THEN
            RAISE EXCEPTION 'Return quantity must be positive for product %.',
                v_product_ids[v_index];
        END IF;

        IF array_position(v_product_ids, v_product_ids[v_index]) <> v_index THEN
            RAISE EXCEPTION 'Product % was entered more than once.',
                v_product_ids[v_index];
        END IF;
    END LOOP;

    -- Return each product and restore its stock.
    FOR v_index IN 1..v_item_count LOOP
        SELECT quantity, returned_quantity
        INTO v_purchased_quantity, v_already_returned
        FROM bill_items
        WHERE bill_id = v_bill_id
          AND product_id = v_product_ids[v_index]
        FOR UPDATE;

        IF NOT FOUND THEN
            RAISE EXCEPTION 'Product % is not listed on bill %.',
                v_product_ids[v_index], v_bill_id;
        END IF;

        v_remaining_quantity := v_purchased_quantity - v_already_returned;

        IF v_return_quantities[v_index] > v_remaining_quantity THEN
            RAISE EXCEPTION
                'Cannot return % units of product %. Remaining returnable units: %.',
                v_return_quantities[v_index],
                v_product_ids[v_index],
                v_remaining_quantity;
        END IF;

        UPDATE products
        SET stock = stock + v_return_quantities[v_index]
        WHERE product_id = v_product_ids[v_index];

        UPDATE bill_items
        SET returned_quantity = returned_quantity + v_return_quantities[v_index]
        WHERE bill_id = v_bill_id
          AND product_id = v_product_ids[v_index];
    END LOOP;

    -- Mark the bill as fully or partially returned.
    IF EXISTS (
        SELECT 1
        FROM bill_items
        WHERE bill_id = v_bill_id
          AND returned_quantity < quantity
    ) THEN
        v_new_status := 'PARTIALLY_RETURNED';
    ELSE
        v_new_status := 'RETURNED';
    END IF;

    UPDATE bills
    SET status = v_new_status
    WHERE bill_id = v_bill_id;

    RAISE NOTICE 'Return completed. Bill ID: %, new status: %.',
        v_bill_id, v_new_status;
END
$$;

COMMIT;

-- Optional queries to inspect results:
-- SELECT * FROM products ORDER BY product_id;
-- SELECT * FROM bills ORDER BY bill_id;
-- SELECT * FROM bill_items ORDER BY bill_item_id;
