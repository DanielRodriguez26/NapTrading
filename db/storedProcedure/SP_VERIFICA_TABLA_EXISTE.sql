DROP PROCEDURE IF EXISTS SP_VERIFICA_TABLA_EXISTE;
CREATE DEFINER=`root`@`%` PROCEDURE `SP_VERIFICA_TABLA_EXISTE`(table_name VARCHAR(100))
BEGIN
	DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02' SET @err = 1;
    SET @err = 0;
    SET @table_name = table_name;
    SET @sql_query = CONCAT('SELECT 1 FROM ',@table_name);
    PREPARE stmt1 FROM @sql_query;
    IF (@err = 1) THEN
        SET @table_exists = 0;
    ELSE
        SET @table_exists = 1;
        DEALLOCATE PREPARE stmt1;
    END IF;
END