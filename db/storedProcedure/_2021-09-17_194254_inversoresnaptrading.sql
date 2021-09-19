/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ inversoresnaptrading /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE inversoresnaptrading;

DROP TABLE IF EXISTS administrativos;
CREATE TABLE `administrativos` (
  `administrativo_id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `identificacion` int NOT NULL,
  `nombre` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `apellido` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `telefono` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `email` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `pais` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`administrativo_id`),
  UNIQUE KEY `uk_administrativos_administrativo_id` (`administrativo_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `administrativos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

DROP TABLE IF EXISTS auditorias;
CREATE TABLE `auditorias` (
  `auditoria_id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `accion` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `descripcion` varchar(500) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `usuario_ip` varchar(45) COLLATE latin1_spanish_ci DEFAULT NULL,
  `pais` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`auditoria_id`),
  UNIQUE KEY `uk_auditorias_auditoria_id` (`auditoria_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `auditorias1_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

DROP TABLE IF EXISTS capital;
CREATE TABLE `capital` (
  `capital_id` int NOT NULL AUTO_INCREMENT,
  `historico_movimiento_id` int DEFAULT NULL,
  `monto` double DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `disponibilidad` int DEFAULT NULL,
  PRIMARY KEY (`capital_id`),
  UNIQUE KEY `uk_capital_capital_id` (`capital_id`),
  KEY `capital_id` (`capital_id`),
  KEY `capital_ibfk_1` (`historico_movimiento_id`),
  CONSTRAINT `capital_ibfk_1` FOREIGN KEY (`historico_movimiento_id`) REFERENCES `historicomovimientos` (`historico_movimientos_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS ganancias;
CREATE TABLE `ganancias` (
  `ganancia_id` int NOT NULL AUTO_INCREMENT,
  `historico_movimiento_id` int DEFAULT NULL,
  `monto` double DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `disponibilidad` int DEFAULT NULL,
  PRIMARY KEY (`ganancia_id`),
  UNIQUE KEY `uk_ganancias_ganancia_id` (`ganancia_id`),
  KEY `ganancia_id` (`ganancia_id`),
  KEY `ganancias_ibfk_1` (`historico_movimiento_id`),
  CONSTRAINT `ganancias_ibfk_1` FOREIGN KEY (`historico_movimiento_id`) REFERENCES `historicomovimientos` (`historico_movimientos_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS historicomovimientos;
CREATE TABLE `historicomovimientos` (
  `historico_movimientos_id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `tipo_movimiento` varchar(20) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `monto` int DEFAULT NULL,
  `estado` tinyint DEFAULT NULL,
  `fecha_limite_solicitud` datetime DEFAULT NULL,
  `email_solicitud` varchar(200) COLLATE latin1_spanish_ci DEFAULT NULL,
  `metodo_desembolso` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`historico_movimientos_id`),
  UNIQUE KEY `uk_historicoMovimientos_historico_movimientos_id` (`historico_movimientos_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `historicoMovimientos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

DROP TABLE IF EXISTS inversores;
CREATE TABLE `inversores` (
  `inversor_id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `identificacion` int NOT NULL,
  `nombres` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `apellidos` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `telefono` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `email` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `pais` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `fecha_inicio_pool` datetime DEFAULT NULL,
  `reinvertir_ganancias` int DEFAULT NULL,
  PRIMARY KEY (`inversor_id`),
  UNIQUE KEY `uk_inversores_inversor_id` (`inversor_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `inversores_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

DROP TABLE IF EXISTS permisos;
CREATE TABLE `permisos` (
  `permiso_id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` tinyint NOT NULL,
  `inversor` tinyint NOT NULL,
  PRIMARY KEY (`permiso_id`),
  UNIQUE KEY `uk_permisos_permiso_id` (`permiso_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

DROP TABLE IF EXISTS siglasmovimientos;
CREATE TABLE `siglasmovimientos` (
  `sigla_id` int NOT NULL AUTO_INCREMENT,
  `siglas` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `descripcion` varchar(200) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `tipo_siglas` varchar(45) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`sigla_id`),
  UNIQUE KEY `uk_siglasmovimientos_sigla_id` (`sigla_id`),
  KEY `sigla_id` (`sigla_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

DROP TABLE IF EXISTS usuarios;
CREATE TABLE `usuarios` (
  `usuario_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) COLLATE latin1_spanish_ci NOT NULL,
  `contrasenia` varchar(255) COLLATE latin1_spanish_ci NOT NULL,
  `rol` tinyint NOT NULL,
  `pais` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `bloqueo_intentos` int DEFAULT '0',
  `usuario_bloqueado` int DEFAULT '0',
  PRIMARY KEY (`usuario_id`),
  UNIQUE KEY `uk_usuarios_usuario_id` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;DROP PROCEDURE IF EXISTS SP_CONSULTAR_AUDITORIAS;
CREATE PROCEDURE `SP_CONSULTAR_AUDITORIAS`(IN inDesde INT)
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
        
END;

DROP PROCEDURE IF EXISTS SP_CONSULTAR_HISTORICOS_CAPITAL;
CREATE PROCEDURE `SP_CONSULTAR_HISTORICOS_CAPITAL`(IN inDesde INT,
	IN inFiltro NVARCHAR(100))
BEGIN
    DECLARE totalRegistros BIGINT;
    
    
    CALL SP_VERIFICA_TABLA_EXISTE('tmpHistoricoCapital');
	IF @table_exists = 1 THEN
		DROP TEMPORARY TABLE tmpHistoricoCapital;
	END IF;


    CREATE TEMPORARY TABLE tmpHistoricoCapital
        SELECT 
            sum(c.monto ) Capital
        FROM historicomovimientos h 
        INNER JOIN inversores i ON h.usuario_id = i.usuario_id 
        INNER JOIN  capital c on h.historico_movimientos_id = c.historico_movimiento_id
        WHERE h.usuario_id = inFiltro
        and h.tipo_movimiento = 'IC'
        LIMIT 20 OFFSET inDesde
        ;

    select count(1) into totalRegistros
    from auditorias
    ;

    select  *, totalRegistros AS totalRegistros
    from tmpHistoricoCapital 
    ;
    CALL SP_VERIFICA_TABLA_EXISTE('tmpHistoricoCapital');
    IF @table_exists = 1 THEN
    DROP TEMPORARY TABLE tmpHistoricoCapital;
    END IF;
        
END;

DROP PROCEDURE IF EXISTS SP_CONSULTAR_HISTORICOS_GANANCIA;
CREATE PROCEDURE `SP_CONSULTAR_HISTORICOS_GANANCIA`(
        IN inDesde INT,
	    IN inFiltro NVARCHAR(100))
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
            and h.tipo_movimiento = 'IC'
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
        
END;

DROP PROCEDURE IF EXISTS SP_CONSULTAR_INVERSORES;
CREATE PROCEDURE `SP_CONSULTAR_INVERSORES`(
	IN `inDesde` INT
)
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
        LIMIT 10 OFFSET inDesde;

    select count(1) into totalRegistros
    from inversores
    ;

    select  *, totalRegistros AS totalRegistros
    from tmpInversores 
    ;
    CALL SP_VERIFICA_TABLA_EXISTE('tmpInversores');
    IF @table_exists = 1 THEN
    DROP TEMPORARY TABLE tmpInversores;
    END IF;
        
END;

DROP PROCEDURE IF EXISTS SP_CONSULTAR_SOLICITUDES;
CREATE PROCEDURE `SP_CONSULTAR_SOLICITUDES`(IN inDesde INT)
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
        
END;

DROP PROCEDURE IF EXISTS SP_VERIFICA_TABLA_EXISTE;
CREATE PROCEDURE `SP_VERIFICA_TABLA_EXISTE`(table_name VARCHAR(100))
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
END;