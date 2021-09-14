USE inversoresnaptrading;

DROP procedure IF EXISTS SP_CONSULTAR_INVERSORES;

DELIMITER $$
USE inversoresnaptrading$$
    CREATE PROCEDURE SP_CONSULTAR_INVERSORES(IN inDesde INT)
    -- obligatorio
BEGIN
    DECLARE totalRegistros BIGINT;
    
    
    CALL SP_VERIFICA_TABLA_EXISTE('tmpInversores');
	IF @table_exists = 1 THEN
		DROP TEMPORARY TABLE tmpInversores;
	END IF;


    CREATE TEMPORARY TABLE tmpInversores
        SELECT
            i.usuario_id,
            i.nombres , i.apellidos,
            i.identificacion,
            i.email,
            i.telefono,
            i.pais
        FROM inversores  i
        LIMIT 20 OFFSET inDesde;

    select count(1) into totalRegistros
    from tmpInversores
    ;

    select  *, totalRegistros AS totalRegistros
    from tmpInversores 
    ;
    CALL SP_VERIFICA_TABLA_EXISTE('tmpInversores');
    IF @table_exists = 1 THEN
    DROP TEMPORARY TABLE tmpInversores;
    END IF;
        
END$$
DELIMITER ;

CALL  SP_CONSULTAR_INVERSORES(0);