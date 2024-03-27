-- Cleaning up from previous run
-- -----------------------------------------------------
DROP DATABASE IF EXISTS hebo_week_7;

DROP USER IF EXISTS hebo_user@localhost;
DROP USER IF EXISTS hebo_super_user@localhost;
DROP USER IF EXISTS hebo_admin_schema;
DROP USER IF EXISTS hebo_admin_database;
DROP USER IF EXISTS hebo_admin_root;
-- -----------------------------------------------------



-- Creating and using database
-- -----------------------------------------------------
CREATE DATABASE hebo_week_7;
USE hebo_week_7;
-- -----------------------------------------------------



-- Creating tables
-- -----------------------------------------------------
CREATE TABLE Category(
    category_id int NOT NULL AUTO_INCREMENT,
    name varchar(100),
    description varchar(100),
    PRIMARY KEY (category_id)
);

CREATE TABLE Item(
    item_id int NOT NULL AUTO_INCREMENT,
    name varchar(100),
    description varchar(100),
    category_id int,
    price int,
    stock int,
    stock_target int,
    PRIMARY KEY (item_id),
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
);

CREATE TABLE Transaction(
    transaction_id int NOT NULL AUTO_INCREMENT,
    item_id int NOT NULL,
    transaction_time DATETIME DEFAULT current_timestamp,
    amount int NOT NULL,
    transaction_type varchar(100) NOT NULL,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);

CREATE TABLE Log(
    log_id int NOT NULL AUTO_INCREMENT,
    event_name varchar(20) NOT NULL,
    table_name varchar(20) NOT NULL,
    user_name varchar(100) NOT NULL,
    event_date DATETIME DEFAULT current_timestamp,
    PRIMARY KEY (log_id)
);
-- -----------------------------------------------------



-- Creating procedures --
-- -----------------------------------------------------
DELIMITER //
-- Helper procedure
CREATE PROCEDURE execute_search(
	IN query varchar(1000),
	IN param1 varchar(100),
	IN param2 varchar(100),
    In param3 varchar(100),
	IN param4 varchar(100),
    IN param5 varchar(100),
    IN param6 varchar(100),
    IN param7 varchar(100)
)
BEGIN
    SET @next_val = null;
    SET @surrogate1 = null;
    SET @surrogate2 = null;
    SET @surrogate3 = null;
    SET @surrogate4 = null;
    SET @surrogate5 = null;
    SET @surrogate6 = null;
    SET @surrogate7 = null;
    
    REPEAT 
		CASE 
			WHEN param1 IS NOT NULL THEN 
				SET @next_val = param1;
                SET param1 = null;
			WHEN param2 IS NOT NULL THEN 
				SET @next_val = param2;
                SET param2 = null;
			WHEN param3 IS NOT NULL THEN 
				SET @next_val = param3;
                SET param3 = null;
            WHEN param4 IS NOT NULL THEN 
            	SET @next_val = param4;
                SET param4 = null;
            WHEN param5 IS NOT NULL THEN 
            	SET @next_val = param5;
                SET param5 = null;
            WHEN param6 IS NOT NULL THEN 
            	SET @next_val = param6;
                SET param6 = null;
			ELSE 
            	SET @next_val = param7;
                SET param7 = null;
		END CASE;
        
        CASE
            WHEN @surrogate1 IS NULL THEN
                SET @surrogate1 = @next_val;
            WHEN @surrogate2 IS NULL THEN
                SET @surrogate2 = @next_val;
            WHEN @surrogate3 IS NULL THEN
                SET @surrogate3 = @next_val;
			WHEN @surrogate4 IS NULL THEN
                SET @surrogate4 = @next_val;
			WHEN @surrogate5 IS NULL THEN
                SET @surrogate5 = @next_val;
			WHEN @surrogate6 IS NULL THEN
                SET @surrogate6 = @next_val;
			WHEN @surrogate7 IS NULL THEN
                SET @surrogate7 = @next_val;
			ELSE
				SET @next_val= @next_val;
        END CASE;
    UNTIL @next_val IS NULL
    END REPEAT;
    
    PREPARE stmt FROM @query;

    IF @surrogate7 IS NOT NULL THEN
        EXECUTE stmt USING @surrogate1, @surrogate2, @surrogate3, @surrogate4, @surrogate5, @surrogate6, @surrogate7;    
    ELSEIF @surrogate6 IS NOT NULL THEN
        EXECUTE stmt USING @surrogate1, @surrogate2, @surrogate3, @surrogate4, @surrogate5, @surrogate6;
    ELSEIF @surrogate5 IS NOT NULL THEN
        EXECUTE stmt USING @surrogate1, @surrogate2, @surrogate3, @surrogate4, @surrogate5;
    ELSEIF @surrogate4 IS NOT NULL THEN
        EXECUTE stmt USING @surrogate1, @surrogate2, @surrogate3, @surrogate4;
    ELSEIF @surrogate3 IS NOT NULL THEN
        EXECUTE stmt USING @surrogate1, @surrogate2, @surrogate3;
    ELSEIF @surrogate2 IS NOT NULL THEN
        EXECUTE stmt USING @surrogate1, @surrogate2;
    ELSEIF @surrogate1 IS NOT NULL THEN
        EXECUTE stmt USING @surrogate1;
    ELSE
        EXECUTE stmt;
    END IF;
    
    DEALLOCATE PREPARE stmt;
END//


-- Add procedures
CREATE PROCEDURE add_item (
	IN item_name varchar(100),
    In item_description varchar(100),
	IN cat_id int,
    IN item_price int,
    IN item_stock int,
    IN item_stock_target int
)
BEGIN
	INSERT INTO Item 
    (name, description, category_id, price, stock, stock_target) 
    VALUES(item_name, item_description, cat_id, item_price, item_stock, item_stock_target);
	SELECT LAST_INSERT_ID() as item_id;
END//

CREATE PROCEDURE add_transaction (
	IN item_id int, 
    IN amount int,
    IN action_type varchar(100)
)
BEGIN
	INSERT INTO Transaction (item_id, amount, transaction_type) VALUES(item_id, amount, action_type);
	SELECT LAST_INSERT_ID() as transaction_id, current_timestamp as transaction_time;
END//

CREATE PROCEDURE add_category (
	IN category_name varchar(100), 
    IN category_description varchar(100))
BEGIN
	INSERT INTO Category (name, description) VALUES(category_name, category_description);
	SELECT LAST_INSERT_ID() as category_id;
END//


-- Generic search procedures
CREATE PROCEDURE search_item (
	IN item_id int,
	IN item_name varchar(100),
    In item_description varchar(100),
	IN cat_id int,
    IN item_price int,
    IN item_stock int,
    IN item_stock_target int
)
BEGIN
	DECLARE query VARCHAR(1000);
            
	-- Create query based on parameters
    SET @query = "SELECT * FROM Item WHERE 1=1";

    IF item_id IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND item_id = ?");
    END IF;
    
    IF item_name IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND name LIKE CONCAT('%', ?, '%')");
    END IF;
    
    IF item_description IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND description LIKE CONCAT('%', ?, '%')");
    END IF;
    
    IF cat_id IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND category_id = ?");
    END IF;
    
    IF item_price IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND price >= ?");
    END IF;
    
    IF item_stock IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND stock >= ?");
    END IF;
    
    IF item_stock_target IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND stock_target >= ?");
    END IF;
    
    CALL execute_search(@query, item_id, item_name, item_description, cat_id, item_price, item_stock, item_stock_target);
END//

CREATE PROCEDURE search_category (
    IN category_id int,
    IN name varchar(100),
    IN description varchar(100)
)
BEGIN
	DECLARE query VARCHAR(1000);

	-- Create query based on parameters
    SET @query = "SELECT * FROM Category WHERE 1=1";
    
    IF category_id IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND category_id = ?");
    END IF;
    
    IF name IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND name LIKE CONCAT('%', ?, '%')");
    END IF;
    
    IF description IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND description LIKE CONCAT('%', ?, '%')");
    END IF;
    
    CALL execute_search(@query, category_id, name, description, null, null, null, null);
END//

CREATE PROCEDURE search_transaction (
    IN transaction_id int,
    IN item_id int,
    IN transaction_time DATETIME,
    IN amount int,
    IN transaction_type varchar(100)
)
BEGIN
	DECLARE query VARCHAR(1000);

	-- Create query based on parameters
    SET @query = "SELECT * FROM Transaction WHERE 1=1";
    
    IF transaction_id IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND transaction_id = ?");
    END IF;
    
    IF item_id IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND item_id = ?");
    END IF;
    
    IF transaction_time IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND transaction_time > ?");
    END IF;
    
    IF amount IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND amount >= ?");
    END IF;
    
	IF transaction_type IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND transaction_type = ?");
    END IF;
    
	CALL execute_search(@query, transaction_id, item_id, transaction_time, amount, transaction_type, null, null);
END//

CREATE PROCEDURE search_log (
	IN log_id int,
    IN event_name varchar(20),
    IN table_name varchar(20),
    IN user_name varchar(100),
    IN event_date DATETIME
)
BEGIN
	DECLARE query VARCHAR(1000);

	-- Create query based on parameters
    SET @query = "SELECT * FROM Log WHERE 1=1";
    
    IF log_id IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND log_id = ?");
    END IF;
    
    IF event_name IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND event_name = ?");
    END IF;
    
    IF table_name IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND table_name = ?");
    END IF;
    
    IF user_name IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND user_name = ?");
    END IF;
    
	IF event_date IS NOT NULL THEN
        SET @query = CONCAT(@query, " AND event_date > ?");
    END IF;
    
	CALL execute_search(@query, log_id, event_name, table_name, user_name, event_date, null, null);
END//


-- Specific search procedures
CREATE PROCEDURE search_low_stock (
    IN category_id int
)
BEGIN
	DECLARE query VARCHAR(1000);

	-- Create query based on parameters
    SET @query = "SELECT * FROM Item WHERE stock < stock_target";
    
    IF category_id IS NOT NULL THEN
        SET @query = CONCAT(@query, " and category_id = ?");
    END IF;
    
    CALL execute_search(@query, category_id, null, null, null, null, null, null);
END//

CREATE PROCEDURE search_category_nulls ()
BEGIN
	SELECT * 
    FROM Category
    WHERE category_id IS NULL OR name IS NULL or description IS NULL;
END//

CREATE PROCEDURE search_item_nulls ()
BEGIN
	SELECT * 
    FROM Item 
    WHERE item_id IS NULL OR name IS NULL OR description IS NULL OR category_id IS NULL OR price IS NULL OR stock IS NULL OR stock_target IS NULL;
END//
DELIMITER ;
-- -----------------------------------------------------



-- Creating Triggers
-- -----------------------------------------------------
DELIMITER //
-- Update item on adding Transaction
CREATE
    TRIGGER insert_transaction
    AFTER INSERT ON Transaction
    FOR EACH ROW
    BEGIN
		UPDATE Item
        SET stock = stock + NEW.amount
        WHERE item_id = NEW.item_id;
    END//


-- Log Item
CREATE
    TRIGGER log_item_insert
    BEFORE INSERT ON Item
    FOR EACH ROW
    BEGIN
		INSERT INTO Log
		(event_name,table_name,user_name)
		VALUES('Insert', 'Item', USER());
    END//

CREATE
    TRIGGER log_item_update
    BEFORE UPDATE ON Item
    FOR EACH ROW
    BEGIN
		INSERT INTO Log
		(event_name,table_name,user_name)
		VALUES('Update', 'Item', USER());
    END//

CREATE
    TRIGGER log_item_delete
    BEFORE DELETE ON Item
    FOR EACH ROW
    BEGIN
		INSERT INTO Log
		(event_name,table_name,user_name)
		VALUES('Delete', 'Item', USER());
    END//
    
    
-- Log Category
CREATE
    TRIGGER log_category_insert
    BEFORE INSERT ON Category
    FOR EACH ROW
    BEGIN
		INSERT INTO Log
		(event_name,table_name,user_name)
		VALUES('Insert', 'Category', USER());
    END//

CREATE
    TRIGGER log_category_update
    BEFORE UPDATE ON Category
    FOR EACH ROW
    BEGIN
		INSERT INTO Log
		(event_name,table_name,user_name)
		VALUES('Update', 'Category', USER());
    END//

CREATE
    TRIGGER log_category_delete
    BEFORE DELETE ON Category
    FOR EACH ROW
    BEGIN
		INSERT INTO Log
		(event_name,table_name,user_name)
		VALUES('Delete', 'Category', USER());
    END//
     
     
-- Log Transaction
CREATE
    TRIGGER log_transaction_insert
    BEFORE INSERT ON Transaction
    FOR EACH ROW
    BEGIN
		INSERT INTO Log
		(event_name,table_name,user_name)
		VALUES('Insert', 'Transaction', USER());
    END//

CREATE
    TRIGGER log_transaction_update
    BEFORE UPDATE ON Transaction
    FOR EACH ROW
    BEGIN
		INSERT INTO Log
		(event_name,table_name,user_name)
		VALUES('Update', 'Transaction', USER());
    END//

CREATE
    TRIGGER log_transaction_delete
    BEFORE DELETE ON Transaction
    FOR EACH ROW
    BEGIN
		INSERT INTO Log
		(event_name,table_name,user_name)
		VALUES('Delete', 'Transaction', USER());
    END//
DELIMITER ;
-- -----------------------------------------------------



-- Create user
-- -----------------------------------------------------
CREATE USER 'hebo_user'@'localhost' IDENTIFIED BY 'test123';
GRANT EXECUTE ON PROCEDURE hebo_week_7.add_transaction TO 'hebo_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.search_item TO 'hebo_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.search_category TO 'hebo_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.search_low_stock TO 'hebo_user'@'localhost';

CREATE USER 'hebo_super_user'@'localhost' IDENTIFIED BY 'test123';
GRANT SELECT, INSERT, UPDATE, DELETE ON hebo_week_7.Item TO 'hebo_super_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.add_transaction TO 'hebo_super_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.search_item TO 'hebo_super_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.search_category TO 'hebo_super_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.search_low_stock TO 'hebo_super_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.add_item TO 'hebo_super_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.add_category TO 'hebo_super_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.search_item_nulls TO 'hebo_super_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.search_category_nulls TO 'hebo_super_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.search_log TO 'hebo_super_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hebo_week_7.search_transaction TO 'hebo_super_user'@'localhost';

CREATE USER 'hebo_admin_schema'@'%' IDENTIFIED BY 'test123';
GRANT ALL PRIVILEGES ON hebo_week_7.* TO 'hebo_admin_schema'@'%';

CREATE USER 'hebo_admin_database'@'%' IDENTIFIED BY 'test123';
GRANT ALL PRIVILEGES ON *.* TO 'hebo_admin_database'@'%';

CREATE USER 'hebo_admin_root'@'%' IDENTIFIED BY 'test123';
GRANT ALL PRIVILEGES ON *.* TO 'hebo_admin_root'@'%' WITH GRANT OPTION;
-- -----------------------------------------------------



-- Populating tables
-- -----------------------------------------------------
INSERT INTO Category (name, description) VALUES ('Miscellaneous', 'For everything not in other categories');
INSERT INTO Category (name, description) VALUES ('Book', 'Books are for reading');
INSERT INTO Item (name, description, category_id, price, stock) VALUES ('Reading for dummies', 'a book about reading', '2', 100, 10);
INSERT INTO Item (name, description, category_id, price, stock) VALUES ('Reading for dummies 2', 'still a book about reading', '2', 100, 10);
INSERT INTO transaction (item_id, amount, transaction_type) VALUES (1, -1, 'sale');
INSERT INTO transaction (item_id, amount, transaction_type) VALUES (1, -1, 'sale');
INSERT INTO transaction (item_id, amount, transaction_type) VALUES (2, 1, 'buy');
-- -----------------------------------------------------
