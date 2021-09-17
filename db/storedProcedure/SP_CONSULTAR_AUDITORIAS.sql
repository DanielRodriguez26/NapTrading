USE inversoresnaptrading;

DROP procedure IF EXISTS SP_CONSULTAR_AUDITORIAS;

DELIMITER $$
USE inversoresnaptrading$$
    CREATE PROCEDURE SP_CONSULTAR_AUDITORIAS(IN inDesde INT,
	IN inFiltro NVARCHAR(100),)
    
BEGIN
    DECLARE totalRegistros BIGINT;
    
    
    CALL SP_VERIFICA_TABLA_EXISTE('tmpAuditoria');
	IF @table_exists = 1 THEN
		DROP TEMPORARY TABLE tmpAuditoria;
	END IF;


    CREATE TEMPORARY TABLE tmpAuditoria
   SELECT
            i.nombres,
            i.apellidos,
            i.identificacion,
            a.fecha,
            a.accion,
            a.descripcion
        FROM auditorias  as a
        INNER JOIN inversores as i ON a.usuario_id  = i.usuario_id        
        WHERE i.nombres LIKE CONCAT('%',inFiltro,'%')
        OR i.apellidos LIKE CONCAT('%',inFiltro,'%')
        OR i.identificacion LIKE CONCAT('%',inFiltro,'%')
        OR a.descripcion LIKE CONCAT('%',inFiltro,'%')
        UNION
        SELECT
            ad.nombre,
            ad.apellido,
            ad.identificacion,
            a.fecha,
            a.accion,
            a.descripcion
        FROM auditorias  as a
        INNER JOIN administrativos  as ad ON a.usuario_id  = ad.usuario_id 
        WHERE ad.nombre LIKE CONCAT('%',inFiltro,'%')
        OR ad.apellido LIKE CONCAT('%',inFiltro,'%')
        OR ad.identificacion LIKE CONCAT('%',inFiltro,'%')
        OR a.descripcion LIKE CONCAT('%',inFiltro,'%')
    LIMIT 20 OFFSET inDesde;

    select count(1) into totalRegistros
    from auditorias
    ;

    select  *, totalRegistros AS totalRegistros
    from tmpAuditoria 
    ;
    CALL SP_VERIFICA_TABLA_EXISTE('tmpAuditoria');
    IF @table_exists = 1 THEN
    DROP TEMPORARY TABLE tmpAuditoria;
    END IF;
        
END$$
DELIMITER ;

CALL  SP_CONSULTAR_AUDITORIAS(0);