CREATE DATABASE  IF NOT EXISTS `club_chabas_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `club_chabas_db`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: club_chabas_db
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `historial_jugador`
--

DROP TABLE IF EXISTS `historial_jugador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_jugador` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `posicion` varchar(3) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `estado` varchar(1) NOT NULL,
  `goles_totales` int unsigned NOT NULL,
  `amarillas_totales` int unsigned NOT NULL,
  `rojas_totales` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `historial_jugador_chk_3` CHECK ((`goles_totales` >= 0)),
  CONSTRAINT `historial_jugador_chk_4` CHECK ((`amarillas_totales` >= 0)),
  CONSTRAINT `historial_jugador_chk_5` CHECK ((`rojas_totales` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_jugador`
--

LOCK TABLES `historial_jugador` WRITE;
/*!40000 ALTER TABLE `historial_jugador` DISABLE KEYS */;
INSERT INTO `historial_jugador` VALUES (1,'DEL','Mateo','Benincasa','','A',0,0,0),(2,'DEF','Leonel','Landaburu','','A',0,0,0),(3,'DEF','Estefano','Morresi','','A',0,0,0),(4,'DEF','Guillermo','Tell','','A',0,0,0),(5,'MED','Alen','Giuliani','','A',0,0,0),(6,'MED','Nahuel','Giuliani','','A',0,0,0),(7,'DEL','Nahuel','Bruno','','A',0,0,0),(8,'DEL','Tobias','Polverini','','A',0,0,0),(9,'DEL','Cristian','Zilli','','A',0,0,0),(10,'DEL','Dario','Gomez Cornejo','','A',0,0,0),(11,'MED','Gaspar','Raimunda','','A',0,0,0),(12,'MED','Lucas','Moulin','','A',0,0,0),(13,'DEF','Manuel','Bottoni','','A',0,0,0),(14,'DEF','Joaquin','Garcia','','A',0,0,0),(15,'DEL','Augusto','Garcia','','A',0,0,0),(16,'DEL','Vicente','Dorado','','T',0,0,0),(17,'ARQ','Alejandro','Dianda','','T',0,0,0),(19,'DEF','Manuel','Lucero','','A',0,0,0),(20,'DEF','Fernando','Sammartino','','T',0,0,0),(21,'DEF','Lucas','Diacolo','','T',0,0,0),(22,'DEF','Tomas','Ortiz','','T',0,0,0),(23,'MED','Gastón','Aquino','','T',0,0,0),(24,'MED','Simon','Verdecchia','','A',0,0,0),(25,'MED','Tomás','Moriconi','','A',0,0,0),(26,'MED','Gonzalo','Nuñez','','A',0,0,0),(27,'MED','Francisco','Garnica','','A',0,0,0),(28,'MED','Enzo','Carrizo','','T',0,0,0),(29,'DEL','Lautaro','Del Carlo','','T',0,0,0),(30,'DEL','Ivan','Squilacci','','A',0,0,0),(31,'DEF','Mariano','Celman','','A',0,0,0),(32,'MED','Diego','Medina','','A',0,0,0),(33,'DEF','David','Ramos','','A',0,0,0),(34,'DEL','Leonardo','Rolon','','A',0,0,0),(35,'DEL','Gino','Bacci','','A',0,0,0),(36,'DEL','Rodrigo','Javier','','A',0,0,0),(37,'DEL','Nahuel','Guzman','','A',0,0,0),(38,'DEF','Cristian','Gill','','A',0,0,0),(39,'DEL','Brian','Gimenez','','A',0,0,0),(40,'DEF','Facundo','Morello','','A',0,0,0),(41,'MED','Ezequiel','Messa','','A',0,0,0),(42,'DEL','Maximiliano','Rolón','','A',0,0,0),(43,'DEF','Valeriano','Artigas','','A',0,0,0),(44,'DEF','Carlos','Ruiz','','A',0,0,0),(45,'DEL','Hugo','Pirez','','A',0,0,0),(46,'DEF','Mariano','Rollo','','A',0,0,0),(47,'DEF','Franco','Jaime','','A',0,0,0),(48,'MED','Marcos','Cordoba','','A',0,0,0),(49,'DEF','Daniel','Pacheco','','A',0,0,0),(50,'ARQ','GolEnContra','.','','A',0,0,0);
/*!40000 ALTER TABLE `historial_jugador` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-06 13:48:48
