USE inversoresnaptrading;

DROP procedure IF EXISTS SP_CONSULTAR_AUDITORIAS;

DELIMITER $$
USE inversoresnaptrading$$
    CREATE PROCEDURE SP_CONSULTAR_AUDITORIAS(IN inDesde INT)
    -- obligatorio
BEGIN
    DECLARE totalRegistros BIGINT;
    
    
    CALL SP_VERIFICA_TABLA_EXISTE('tmpAuditoria');
	IF @table_exists = 1 THEN
		DROP TEMPORARY TABLE tmpAuditoria;
	END IF;


    CREATE TEMPORARY TABLE tmpAuditoria
        SELECT
          i.nombres ,
          i.apellidos,
          i.identificacion,
          a.fecha,
          a.accion,
          a.descripcion
      FROM auditorias  as a
      INNER JOIN inversores as i ON a.usuario_id  = i.usuario_id
      LIMIT 10 OFFSET inDesde;

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
