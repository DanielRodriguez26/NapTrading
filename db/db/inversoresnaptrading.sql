-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: inversoresnaptrading
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `inversoresnaptrading`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `inversoresnaptrading` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `inversoresnaptrading`;

--
-- Table structure for table `administrativos`
--

DROP TABLE IF EXISTS `administrativos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrativos`
--

LOCK TABLES `administrativos` WRITE;
/*!40000 ALTER TABLE `administrativos` DISABLE KEYS */;
INSERT INTO `administrativos` VALUES (23,44,2647898,'Daniel','Rodriguez','3016115627','darc2611@gmail.com','Colombia'),(24,54,2647898,'Daniel','Carvajal','3016115627','darc2611@gmail.com','Colombia'),(25,55,2647898,'Daniel','Carvajal','3016115627','darc2611@gmail.com','Colombia'),(26,56,2647898,'Daniel','Carvajal','3016115627','darc2611@gmail.com','Colombia'),(27,57,2647898,'Daniel','Carvajal','3016115627','darc2611@gmail.com','Colombia'),(28,58,2647898,'Daniel','Carvajal','3016115627','darc2611@gmail.com','Colombia'),(29,59,2647898,'Daniel','Carvajal','3016115627','darc2611@gmail.com','Colombia'),(30,60,2647898,'Daniel','Carvajal','3016115627','darc2611@gmail.com','Colombia'),(31,61,264789812,'Daniel','Cortez','3016115627','darc2611@gmail.com','Colombia');
/*!40000 ALTER TABLE `administrativos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auditorias`
--

DROP TABLE IF EXISTS `auditorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditorias`
--

LOCK TABLES `auditorias` WRITE;
/*!40000 ALTER TABLE `auditorias` DISABLE KEYS */;
INSERT INTO `auditorias` VALUES (1,27,'2021-09-13 12:53:11','Ticket fin','e dio por finalizado el ticket 3 Retiro de Ganancias y Capital del inversor Marcial Mejias de identificacion 587439 con fecha limite de None por un monto de 1200 a los siguientes datos None Skrill','127.0.0.1','Colombia'),(2,27,'2021-09-13 22:06:23','Ticket fin','Se dio por finalizado el ticket 4 Retiro de Ganancias del inversor Fabio Carbonell de identificacion 456218 con fecha limite de None por un monto de 100 a los siguientes datos None Skrill','127.0.0.1','Colombia'),(3,27,'2021-09-13 22:06:38','Ticket fin','Se dio por finalizado el ticket 1 Retiro de Ganancias del inversor Sarah Barrios de identificacion 845123 con fecha limite de None por un monto de 1000 a los siguientes datos None Skrill','127.0.0.1','Colombia'),(4,27,'2021-09-13 22:06:39','Ticket fin','Se dio por finalizado el ticket 2 Retiro de Ganancias del inversor Sarah Barrios de identificacion 845123 con fecha limite de None por un monto de 800 a los siguientes datos None Binance','127.0.0.1','Colombia'),(5,27,'2021-09-13 22:07:36','Ticket fin','Se dio por finalizado el ticket 3 Retiro de Ganancias y Capital del inversor Marcial Mejias de identificacion 587439 con fecha limite de None por un monto de 1200 a los siguientes datos None Skrill','127.0.0.1','Colombia'),(6,28,'2021-09-13 22:08:01','Ticket fin','Se dio por finalizado el ticket 1 Retiro de Ganancias del inversor Sarah Barrios de identificacion 845123 con fecha limite de None por un monto de 1000 a los siguientes datos None Skrill','127.0.0.1','Colombia'),(7,27,'2021-09-13 22:08:03','Ticket fin','Se dio por finalizado el ticket 2 Retiro de Ganancias del inversor Sarah Barrios de identificacion 845123 con fecha limite de None por un monto de 800 a los siguientes datos None Binance','127.0.0.1','Colombia'),(8,27,'2021-09-13 22:09:46','Ticket fin','Se dio por finalizado el ticket 1 Retiro de Ganancias del inversor Sarah Barrios de identificacion 845123 con fecha limite de None por un monto de 1000 a los siguientes datos None Skrill','127.0.0.1','Colombia'),(9,27,'2021-09-13 22:09:47','Ticket fin','Se dio por finalizado el ticket 2 Retiro de Ganancias del inversor Sarah Barrios de identificacion 845123 con fecha limite de None por un monto de 800 a los siguientes datos None Binance','127.0.0.1','Colombia'),(10,27,'2021-09-13 23:24:15','Ticket fin','Se dio por finalizado el ticket 8 Retiro de Ganancias del inversor Lara Salvador de identificacion 764135 con fecha limite de None por un monto de 200 a los siguientes datos None None','127.0.0.1','Colombia'),(11,44,'2021-09-13 12:53:11','Ticket fin','Se dio por finalizado el ticket 3 Retiro de Ganancias y Capital del inversor Marcial Mejias de identificacion 587439 con fecha limite de None por un monto de 1200 a los siguientes datos None Skrill','127.0.0.1','Colombia'),(32,44,'2021-09-17 00:44:57','Crear Administrador','Se creo el administrador con los siguientes datos: Nombre 6, Apellidos 4, email 7,  identificación: 2','127.0.0.1',NULL),(33,44,'2021-09-17 19:11:57','Cambiar contraseña','Se cambio la contraseña del usuario 1035860037','127.0.0.1',NULL),(34,44,'2021-09-17 19:35:36','Ticket finalizado','Se dio por finalizado el ticket 38 Ingreso de Capital del inversor Daniel Rodriguez4 de identificacion 1035860037 con fecha limite de 2021-10-08 00:00:00 por un monto de 2000 a los siguientes datos darc2611@gmail.com None','127.0.0.1',NULL);
/*!40000 ALTER TABLE `auditorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `capital`
--

DROP TABLE IF EXISTS `capital`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `capital`
--

LOCK TABLES `capital` WRITE;
/*!40000 ALTER TABLE `capital` DISABLE KEYS */;
INSERT INTO `capital` VALUES (1,34,1000,'2021-08-12 00:00:00',1000),(2,35,1200,'2021-08-12 00:00:00',1200),(3,37,100,'2021-08-12 00:00:00',100),(7,41,256000,'2021-09-17 00:07:06',256000),(8,42,52000,'2021-09-17 00:09:21',308000);
/*!40000 ALTER TABLE `capital` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ganancias`
--

DROP TABLE IF EXISTS `ganancias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ganancias`
--

LOCK TABLES `ganancias` WRITE;
/*!40000 ALTER TABLE `ganancias` DISABLE KEYS */;
INSERT INTO `ganancias` VALUES (1,34,1000,'2021-08-12 00:00:00',1000),(2,38,1200,'2021-08-12 00:00:00',1200),(3,40,100,'2021-08-12 00:00:00',100);
/*!40000 ALTER TABLE `ganancias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historicomovimientos`
--

DROP TABLE IF EXISTS `historicomovimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historicomovimientos`
--

LOCK TABLES `historicomovimientos` WRITE;
/*!40000 ALTER TABLE `historicomovimientos` DISABLE KEYS */;
INSERT INTO `historicomovimientos` VALUES (34,27,'2021-09-11 15:54:17','RG',1000,0,NULL,NULL,NULL),(35,27,'2021-09-11 15:54:18','RG',1200,0,NULL,NULL,NULL),(36,29,'2021-09-11 15:54:19','RG',100,0,NULL,NULL,NULL),(37,30,'2021-09-11 15:54:20','RG',170,0,NULL,NULL,NULL),(38,30,'2021-09-07 00:00:00','IC',2000,0,'2021-10-08 00:00:00','darc2611@gmail.com',NULL),(40,27,'2021-09-14 12:03:07','IC',52000,0,'2021-09-14 12:03:07','darc2611@gmail.com',NULL),(41,53,'2021-09-17 00:07:04','IC',256000,0,'2021-09-17 00:07:04','darc2611@gmail.com',NULL),(42,53,'2021-09-17 00:09:17','IC',52000,0,'2021-09-17 00:09:17','darc2611@gmail.com',NULL);
/*!40000 ALTER TABLE `historicomovimientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inversores`
--

DROP TABLE IF EXISTS `inversores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inversores`
--

LOCK TABLES `inversores` WRITE;
/*!40000 ALTER TABLE `inversores` DISABLE KEYS */;
INSERT INTO `inversores` VALUES (26,27,1035860037,'Daniel','Rodriguez1','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(27,28,1035860037,'Daniel','Rodriguez2','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(28,29,1035860037,'Daniel','Rodriguez4','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(29,30,1035860037,'Daniel','Rodriguez4','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(30,31,1035860037,'Daniel','Rodriguez5','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(31,32,1035860031,'Daniel','Rodriguez6','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(32,33,1035860137,'Daniel','Rodriguez7','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(33,34,1035860237,'Daniel','Rodriguez8','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(34,37,1035860024,'Daniel','Rodriguez9','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(35,38,854795178,'Daniel','Rodriguez10','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(36,40,565441154,'Daniel','Rodriguez011','3016115627','darc2611@gmail.com',NULL,NULL,NULL),(43,53,264789877,'Carlos','Tirado','3016115627','darc2611@gmail.com','Colombia',NULL,NULL);
/*!40000 ALTER TABLE `inversores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permisos`
--

DROP TABLE IF EXISTS `permisos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permisos` (
  `permiso_id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` tinyint NOT NULL,
  `inversor` tinyint NOT NULL,
  PRIMARY KEY (`permiso_id`),
  UNIQUE KEY `uk_permisos_permiso_id` (`permiso_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permisos`
--

LOCK TABLES `permisos` WRITE;
/*!40000 ALTER TABLE `permisos` DISABLE KEYS */;
INSERT INTO `permisos` VALUES (1,0,1),(2,1,0);
/*!40000 ALTER TABLE `permisos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `siglasmovimientos`
--

DROP TABLE IF EXISTS `siglasmovimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `siglasmovimientos` (
  `sigla_id` int NOT NULL AUTO_INCREMENT,
  `siglas` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `descripcion` varchar(200) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `tipo_siglas` varchar(45) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`sigla_id`),
  UNIQUE KEY `uk_siglasmovimientos_sigla_id` (`sigla_id`),
  KEY `sigla_id` (`sigla_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `siglasmovimientos`
--

LOCK TABLES `siglasmovimientos` WRITE;
/*!40000 ALTER TABLE `siglasmovimientos` DISABLE KEYS */;
INSERT INTO `siglasmovimientos` VALUES (1,'RG','Retiro de Ganancias','R'),(2,'RGC','Retiro de Ganancias y Capital','R'),(3,'IC','Ingreso de Capital','I'),(31,'RIG','Reinvertir Ganancias','I');
/*!40000 ALTER TABLE `siglasmovimientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (21,'sbarrios','1234',1,NULL,0,0),(22,'mmejias','1234',1,NULL,0,0),(23,'fcarbonell','1234',1,NULL,0,0),(24,'lsalvador','1234',1,NULL,0,0),(25,'hfuertes','1234',1,NULL,0,0),(26,'jporras','0541d88f283bbae2d55e24c05a49a95c031affc3b4580ad566d19e67b417a60d8a857297c8eab290d3effd989256c2326c723cc2673937b913c07bf8c4f98236',1,NULL,0,0),(27,'drodriguez037','7d4fe68cba0f6216f2ff937148dc6512df44fe08c9227fe0075dcff468e2a29acb18756e610ec5b00b4f16c6d93f19782dd7f5f423937f5e127413996f471522',2,NULL,0,0),(28,'drodriguez036','3bda2aaa8b44dbdd28157fda4bac0f2d3784048967545ba804dbaaae37d046c10941e67192de31209d47ade0580e974c2ef36f978352106b9aa7b215a247957c',1,NULL,0,0),(29,'drodriguez038','805d76d54792960d481bd03bf7fe474a8f8c1271659cb1bcff60bd0a93ef4e09dfc3060631cb32329497521f9d84bda354f8157fe548780461fc2a5258948318',1,NULL,0,0),(30,'drodriguez037','cbc12512f9f379c9b811f4e357c49caf4142db4e7c4975fe64d836821faad540305bfba0255138c05c261898759e2a5237266e8776319ccf8cbabf935029b30f',2,NULL,0,0),(31,'drodriguez0037','aa39285766f91bd85572fc5ce9d31b14362120175811831737358ff19f085c45973d5c8a9c57625526fc5677f02ed6c0456ee1786b198de0b04783ec23a1bc43',1,NULL,0,0),(32,'drodriguez031','c1f0e810eab0f5dff9a18e659a7a993588807350a9136600a520f0ed5d2790d5faa26d6313be762c53128bfce50e9eaeb90726446630c17946fef2d8a5c187ca',1,NULL,0,0),(33,'drodriguez137','f531d8f0b684172b22c7067f9a3a950714a24b76bed07219c5535bdffe8fa5a2b37a4ba9454d060ee7f62e655a761a7b747c0ae89ad3b72de7a47825778de4a3',1,NULL,0,0),(34,'drodriguez237','a54eb1583015747bf74dacbb3dfd8d64d43ecb23ff7671e81a8128bb4fc922005a2754f7276c0cb7afd5a3b41e44aed02357037a98eb69d9763243750f8eb045',1,NULL,0,0),(35,'drodriguez374','ae00f5873143e2a975ee41f2c34cbf8b3c633b47c20c04621a8130d3dbc32e23f346496f9e11c71645ec98ff5884b4917ca33bf3ab0972650f2b7d09979d5a14',1,NULL,0,0),(36,'drodriguez0374','8d90bb5a7aecfc56acf7990a9c5b240a98c333d1bb315be5cd76fed554ead7c4749eca97599c1873b86a360a6f038a5d73e17db00ed2cfa877877b1bcd2f9cb1',1,NULL,0,0),(37,'drodriguez024','253f80e14598f34ed73064495a1483a34954d7ef36d259a06374b6f6ce38bd123fdad1063a2ed1b54e064c68291fe1a3f64dbe6bf68d51d72d8ccf4d555f3d4d',1,NULL,0,0),(38,'drodriguez178','05187b2a1e4c3437ad8ab4541776d2bd1b0c6cfd638ef6976e5cb70409d4e2dd52ff5cb3b64ce3a3471a86a5a82ac2d45670791ef8a763eb069a7c450b06b901',1,NULL,0,0),(40,'drodriguez154','578995',1,NULL,0,0),(43,'drodriguez777','af7057ef837f1ff111d684d5cea3b8b951661293a415ae72d71651d29356adbe7caf3735815b259c7f689e6fe775ccac2d4d412960710784fa796548dcb4c4b2',1,NULL,0,0),(44,'drodriguez898','537ef00f8950996f0494ab297ee12006cae1e2d371b6037c4cb95bbe9cb23d65f1ea00e15abb49902b464c4db81bf474f41dbc18c9fd8d1704389138da82c6e0',1,NULL,0,0),(48,'ctirado877','fb10dd683a44a2e0a1b4c83fae2f0621afce06a35a847a57b1259e12c50422ce61f9e687e248269cbb41de7818fbf96f2cae9ff15a5ea98c2f362de9c1a3344e',2,NULL,0,0),(49,'ctirado9877','9e87934375452624043d7837856f1b6ce7d971dc8a8fac01b25987aadf67ef2177e9b011441b5bb0a9af9500ba2ab7a7bb75d7baa468a8029d6d1a036b02403c',2,NULL,0,0),(50,'ctirado9877','dcacc3a5482e6d92e133ce10c3f6ed47fb3d3ff014a58aa6e4c60b2c412f313fb75894cca42b65430badaf015e2678cef621e3a80eaeb1397f0cadd3505f3c50',2,NULL,0,0),(51,'ctirado9877','f2c57f38c0620e41e8043343297d17fa19b06389ad35981ee922f76f059be3205b23895ed34a65b3dba83c1b2e744037c73fb142b772391e301b01d17b7f6c32',2,NULL,0,0),(52,'ctirado9877','88178a1d2e1801d4a1d7ed4456ab04d3cd303f719678387273fa439d952a24dc16dbf70e8620bf19dff3cecf4f228c13daa4fb284ca361a2335f691d175ba011',2,NULL,0,0),(53,'ctirado9877','e6d87d9a7695aa588b50602cf9121750dd4d27228746ef4dfb6db1f67242e616f33836f29d3e9b102d3893530ee7f7dd25d6db6ec5f74fa40a3588cf4bb865fa',2,NULL,0,0),(54,'dcarvajal898','dbbe492998eee8222960d29850d8c2a5136549517c4f70a2de10f7ad67c039580e57f01a0a002bcfef7e6ab3271f70629aa246988cbb72b2693870685b657b0b',1,NULL,0,0),(55,'dcarvajal7898','c65b58a8cd5bb9b085baa942d2bffff043d73a64be8363ec7a1589611436feb179181cd5f5cd0114e439833c0d36fd7604b3da07e5ecc5b0d0aea05d7c5dde61',1,NULL,0,0),(56,'dcarvajal7898','a4876f9a4d8dc2f9b4c47dab8a9ababb47adcfc9fd34e15b0b6549d6b59c33dc3fd3bfc2eaacbcc76bf4b392ba22ba8bf1156fec2f4d027d96d1586a474d532a',1,NULL,0,0),(57,'dcarvajal7898','47278d89335a71312dbbdf39c8801f41e3071e00b7ef7eb4e3bf495ab5699f870c83e8c7d551ac62e4158c828eedd59bbedac000cd266eaee32b25739df82b36',1,NULL,0,0),(58,'dcarvajal7898','002718a5942f8f3707f0f005ab03113da8db26c38fe9a692e864d381d449492607f156c18fb07768f1b5dc381d004462d3ff9b2b56f1b7cef2a7e2c3eef82d04',1,NULL,0,0),(59,'dcarvajal7898','bc29d40055ba8eb8c79448ca44b4e6c843c0dbbe35db90eb10fd204251bd415c1a0e91123c2183ad6dfba21315ff6cd893d93b4d646693c0666fea1b92ca095c',2,NULL,0,0),(60,'dcarvajal7898','d4d28d9e6e0f0a40cabfbec57d5146a87956091ca7b266dc3abd0fafd4076192abfcab4ef1ec76ce0b4e0d2724b7385042bee9bf091e3e512d01bfa037a2059e',2,NULL,0,0),(61,'dcortez812','b9ee938e24c450b7e73c3318df1f07ae04d9e4b33f8ed5513ee6a0690da57bdfbc54cb75a18e2ab503b4210349724e294490f26120260d04b8fdd60234e31725',2,NULL,0,0);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'inversoresnaptrading'
--
/*!50003 DROP PROCEDURE IF EXISTS `SP_CONSULTAR_AUDITORIAS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `SP_CONSULTAR_AUDITORIAS`(IN inDesde INT)
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
        
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CONSULTAR_HISTORICOS_CAPITAL` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `SP_CONSULTAR_HISTORICOS_CAPITAL`(IN inDesde INT,
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
        
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CONSULTAR_HISTORICOS_GANANCIA` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `SP_CONSULTAR_HISTORICOS_GANANCIA`(
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
        
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CONSULTAR_INVERSORES` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `SP_CONSULTAR_INVERSORES`(
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
        
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CONSULTAR_SOLICITUDES` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `SP_CONSULTAR_SOLICITUDES`(IN inDesde INT)
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
        
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_VERIFICA_TABLA_EXISTE` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
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
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-09-17 19:48:18
