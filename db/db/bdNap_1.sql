
CREATE DATABASE /*!32312 IF NOT EXISTS*/ `inversoresnaptrading` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `inversoresnaptrading`;

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `usuario_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `contrasenia` varchar(100) NOT NULL,
  `rol` tinyint NOT NULL,
  PRIMARY KEY (`usuario_id`),
  UNIQUE KEY `uk_usuarios_usuario_id` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `permisos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permisos` (
  `permiso_id` int(11) NOT NULL AUTO_INCREMENT,
  `administrativo` tinyint NOT NULL,
  `inversor` tinyint NOT NULL,
  PRIMARY KEY (`permiso_id`),
  UNIQUE KEY `uk_permisos_permiso_id` (`permiso_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `inversores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inversores` (
  `inversor_id` int(100) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(100) NOT NULL,
  `identificacion` int(20) NOT NULL,
  `nombres` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `apellidos` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `telefono` int(20) COLLATE latin1_spanish_ci DEFAULT NULL,
  `email` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`inversor_id`),
  UNIQUE KEY `uk_inversores_inversor_id` (`inversor_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `inversores_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `administrativos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administrativos` (
  `administrativo_id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(20) NOT NULL,
  `identificacion` int(20) NOT NULL,
  `nombre` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `apellido` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `telefono` int(20) COLLATE latin1_spanish_ci DEFAULT NULL,
  `email` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`administrativo_id`),
  UNIQUE KEY `uk_administrativos_administrativo_id` (`administrativo_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `administrativos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `historicoMovimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historicoMovimientos` (
  `historico_movimientos_id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP, 
  `tipo_movimiento` varchar(20) COLLATE latin1_spanish_ci DEFAULT NULL,
  `monto` int(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `estado` tinyint COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`historico_movimientos_id`),
  UNIQUE KEY `uk_historicoMovimientos_historico_movimientos_id` (`historico_movimientos_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `historicoMovimientos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `auditorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auditorias` (
  `auditoria_id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,  
  `accion` varchar(10) COLLATE latin1_spanish_ci DEFAULT NULL,
  `descripcion` varchar(500) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`auditoria_id`),
  UNIQUE KEY `uk_auditorias_auditoria_id` (`auditoria_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `auditorias1_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


