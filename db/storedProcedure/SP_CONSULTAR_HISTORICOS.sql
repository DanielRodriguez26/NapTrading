
USE inversoresnaptrading;

DROP procedure IF EXISTS SP_CONSULTAR_HISTORICOS;

DELIMITER $$
USE dibanka$$
CREATE PROCEDURE SP_CONSULTAR_HISTORICOS(
  IN inDesde INT, -- obligatorio
BEGIN
  DECLARE totalRegistros BIGINT;
  
  
  CALL SP_VERIFICA_TABLA_EXISTE('tmpHistoricos');
	IF @table_exists = 1 THEN
		DROP TEMPORARY TABLE tmpHistoricos;
	END IF;

  CREATE TEMPORARY TABLE tmpHistoricos
    SELECT 
    CONCAT( i.nombres +' '+ i.apellido) ,
    i.identificacion,
    i.email,
    i.telefono,
    h.historico_movimientos_id,
    h.fecha,
    h.tipo_movimiento,
    h.monto,
    h.estado
    FROM inversores  i
    INNER JOIN historicomovimientos  h ON i.usuario_id = h.usuario_id
 
    LIMIT 20 OFFSET inDesde;
  
  
  select count(1) into totalRegistros
  from tmpHistoricos
  ;
  CALL SP_VERIFICA_TABLA_EXISTE('tmpHistoricos');
  IF @table_exists = 1 THEN
    DROP TEMPORARY TABLE tmpHistoricos;
  END IF;
        
END$$
DELIMITER ;

call SP_ABC(0, '860050750', null, 0);