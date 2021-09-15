USE inversoresnaptrading;

DROP procedure IF EXISTS SP_CONSULTAR_SOLICITUDES;

DELIMITER $$
USE inversoresnaptrading$$
    CREATE PROCEDURE SP_CONSULTAR_SOLICITUDES(IN inDesde INT)
    -- obligatorio
BEGIN
    DECLARE totalRegistros BIGINT;
    
    
    CALL SP_VERIFICA_TABLA_EXISTE('tmpSolicitudes');
	IF @table_exists = 1 THEN
		DROP TEMPORARY TABLE tmpSolicitudes;
	END IF;


    CREATE TEMPORARY TABLE tmpSolicitudes
        SELECT   h.historico_movimientos_id, 
                i.nombres, i.apellidos, 
                i.identificacion,h.email_solicitud, 
                i.telefono, h.fecha, s.descripcion,
                h.monto,h.fecha_limite_solicitud, 
                h.metodo_desembolso
        from historicomovimientos as h
        inner join inversores as i on i.usuario_id = h.usuario_id
        inner join siglasmovimientos as s on  s.siglas = h.tipo_movimiento
        where h.estado=1  order by h.fecha desc
        LIMIT 10 OFFSET inDesde;

    select count(1) into totalRegistros
    from historicomovimientos as h
    inner join inversores as i on i.usuario_id = h.usuario_id
    inner join siglasmovimientos as s on  s.siglas = h.tipo_movimiento
    where h.estado=1;

    select  *, totalRegistros AS totalRegistros
    from tmpSolicitudes 
    ;
    CALL SP_VERIFICA_TABLA_EXISTE('tmpSolicitudes');
    IF @table_exists = 1 THEN
    DROP TEMPORARY TABLE tmpSolicitudes;
    END IF;
        
END$$
DELIMITER ;

CALL  SP_CONSULTAR_SOLICITUDES(0);