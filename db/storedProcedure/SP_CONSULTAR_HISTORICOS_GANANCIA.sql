USE inversoresnaptrading;

DROP procedure IF EXISTS SP_CONSULTAR_HISTORICOS_GANANCIA;

DELIMITER $$
USE inversoresnaptrading$$
    CREATE PROCEDURE SP_CONSULTAR_HISTORICOS_GANANCIA(
        IN inDesde INT,
	    IN inFiltro NVARCHAR(100),)
    
BEGIN
    DECLARE totalRegistros BIGINT;
    
    
    CALL SP_VERIFICA_TABLA_EXISTE('tmpHistoricoGanancia');
	IF @table_exists = 1 THEN
		DROP TEMPORARY TABLE tmpHistoricoGanancia;
	END IF;


    CREATE TEMPORARY TABLE tmpHistoricoGanancia
        SELECT
            sum(g.monto) Ganancias
            FROM historicomovimientos h 
            INNER JOIN ganancias g ON h.historico_movimientos_id = g.historico_movimiento_id
            WHERE h.usuario_id =  inFiltro
        LIMIT 20 OFFSET inDesde
        ;

    select count(1) into totalRegistros
    from auditorias
    ;

    select  *, totalRegistros AS totalRegistros
    from tmpHistoricoGanancia 
    ;
    CALL SP_VERIFICA_TABLA_EXISTE('tmpHistoricoGanancia');
    IF @table_exists = 1 THEN
    DROP TEMPORARY TABLE tmpHistoricoGanancia;
    END IF;
        
END$$
DELIMITER ;
