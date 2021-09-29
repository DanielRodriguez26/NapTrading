/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
DROP TABLE IF EXISTS tipousuario;
CREATE TABLE `tipousuario` (
  `tipoUsuarioID` int NOT NULL COMMENT 'Identificador de la tabla tipoUsuario',
  `nombre` varchar(1000) DEFAULT NULL COMMENT 'DescripciÃ³n del tipo de usuario',
  PRIMARY KEY (`tipoUsuarioID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Tabla para la gestiÃ³n de los tipos de usuario de la aplicaciÃ³n';
INSERT INTO tipousuario(tipoUsuarioID,nombre) VALUES(1,'OPERADOR'),(2,'BENEFICIARIO'),(3,'ENTIDAD');