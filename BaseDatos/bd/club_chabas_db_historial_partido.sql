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
-- Table structure for table `historial_partido`
--

DROP TABLE IF EXISTS `historial_partido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_partido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `tipo` varchar(1) NOT NULL,
  `goles_chabas` int unsigned NOT NULL,
  `goles_rival` int unsigned NOT NULL,
  `rival_id` bigint NOT NULL,
  `torneo_id` bigint NOT NULL,
  `arbitro` varchar(100) NOT NULL,
  `instancia` varchar(6) NOT NULL,
  `descripcion` longtext,
  PRIMARY KEY (`id`),
  KEY `historial_partido_torneo_id_38edf055_fk_historial_torneo_id` (`torneo_id`),
  KEY `historial_partido_rival_id_484714c3_fk_historial_club_id` (`rival_id`),
  CONSTRAINT `historial_partido_rival_id_484714c3_fk_historial_club_id` FOREIGN KEY (`rival_id`) REFERENCES `historial_club` (`id`),
  CONSTRAINT `historial_partido_torneo_id_38edf055_fk_historial_torneo_id` FOREIGN KEY (`torneo_id`) REFERENCES `historial_torneo` (`id`),
  CONSTRAINT `historial_partido_chk_1` CHECK ((`goles_chabas` >= 0)),
  CONSTRAINT `historial_partido_chk_2` CHECK ((`goles_rival` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_partido`
--

LOCK TABLES `historial_partido` WRITE;
/*!40000 ALTER TABLE `historial_partido` DISABLE KEYS */;
INSERT INTO `historial_partido` VALUES (1,'2025-04-14','L',4,0,1,1,'Julian Espíndola','Fecha',NULL),(2,'2025-04-06','V',5,1,2,1,'Esteban Gómez','Fecha',NULL),(3,'2025-04-02','L',2,0,3,1,'David Espíndola','Fecha',NULL),(4,'2025-03-23','V',1,0,4,1,'Julian Espíndola','Fecha',NULL),(5,'2025-03-16','V',2,3,5,1,'Walter Flores','Fecha',NULL),(6,'2025-04-20','V',0,0,6,1,'Damian Almada','Fecha',NULL),(7,'2024-11-10','V',0,3,15,2,'','CuaVue',NULL),(8,'2024-11-03','L',3,0,15,2,'','CuaIda',NULL),(9,'2024-10-27','L',2,1,2,2,'','OctVue',NULL),(10,'2024-10-20','V',2,0,2,2,'','OctIda',''),(11,'2024-10-04','L',0,0,2,2,'','RepVue',''),(12,'2024-09-29','V',0,0,2,2,'','RepIda',''),(13,'2025-04-27','L',0,0,7,1,'Federico Valle','Fecha',NULL),(14,'2024-09-22','V',1,0,15,2,'','Fecha',NULL),(15,'2024-09-15','L',3,0,1,2,'','Fecha',NULL),(16,'2024-09-08','L',4,0,14,2,'','Fecha',NULL),(17,'2024-09-01','L',3,1,10,2,'','Fecha',NULL),(18,'2024-08-25','L',2,1,13,2,'','Fecha',NULL),(19,'2024-08-18','V',1,1,11,2,'','Fecha',NULL),(20,'2024-08-11','L',0,1,12,2,'','Fecha',NULL),(21,'2024-08-04','V',1,2,6,2,'','Fecha',NULL),(22,'2024-07-28','L',1,1,5,2,'','Fecha',NULL),(23,'2024-07-21','V',2,0,9,2,'','Fecha',NULL),(25,'2024-07-14','L',2,0,3,2,'','Fecha',NULL),(26,'2024-07-07','V',0,2,7,2,'','Fecha',NULL),(27,'2024-06-30','L',0,1,2,2,'','Fecha',NULL),(28,'2024-06-23','V',0,1,4,2,'','Fecha',NULL),(29,'2024-06-16','L',2,1,8,2,'','Fecha',NULL),(30,'2024-06-09','L',0,1,13,3,'','RepVue',NULL),(31,'2024-06-02','V',1,1,13,3,'','RepIda',NULL),(32,'2024-05-26','L',0,0,15,3,'','Fecha',NULL),(33,'2024-05-19','V',1,0,1,3,'','Fecha',NULL),(34,'2024-05-12','V',3,0,14,3,'','Fecha',NULL),(35,'2024-05-05','V',2,3,10,3,'','Fecha',NULL),(36,'2024-05-01','V',1,1,13,3,'','Fecha',NULL),(38,'2024-04-28','L',0,2,11,3,'','Fecha',NULL),(39,'2024-04-21','V',2,0,12,3,'','Fecha',NULL),(40,'2024-04-10','L',1,0,6,3,'','Fecha',NULL),(41,'2024-04-07','V',3,1,5,3,'','Fecha',NULL),(42,'2024-04-02','L',0,1,9,3,'','Fecha',NULL),(43,'2024-03-29','V',1,0,3,3,'','Fecha',NULL),(44,'2024-03-24','L',0,3,7,3,'','Fecha',NULL),(45,'2024-03-10','V',1,1,2,3,'','Fecha',NULL),(46,'2024-03-01','L',1,0,4,3,'','Fecha',NULL),(47,'2024-02-23','V',2,1,8,3,'','Fecha',NULL),(48,'2025-05-04','V',3,0,13,1,'Ivan Reina','Fecha',NULL),(49,'2025-05-08','L',3,0,12,1,'Cirilo Gómez','Fecha',NULL),(50,'2025-05-16','V',3,1,10,1,'Nahuel Franco','Fecha',NULL),(51,'2023-09-17','V',1,1,2,4,'','CuaVue',''),(52,'2023-09-06','L',1,1,2,4,'','CuaIda',''),(53,'2023-08-27','L',1,0,10,4,'','OctVue',''),(54,'2023-08-20','V',0,0,10,4,'','OctIda',''),(55,'2023-08-06','V',1,2,8,4,'','Fecha',''),(56,'2023-07-30','L',5,2,9,4,'','Fecha',''),(57,'2023-07-23','V',1,0,5,4,'','Fecha',''),(58,'2023-07-09','V',0,1,7,4,'','Fecha',''),(59,'2023-07-02','L',0,0,6,4,'','Fecha',''),(60,'2023-06-25','V',2,2,1,4,'','Fecha',''),(61,'2023-06-18','L',2,0,15,4,'','Fecha',''),(62,'2023-04-09','L',0,5,8,5,'','Fecha',''),(63,'2023-04-04','V',0,2,9,5,'','Fecha',''),(64,'2023-03-26','L',1,2,5,5,'','Fecha',''),(65,'2023-03-19','L',1,2,7,5,'','Fecha',''),(66,'2023-03-12','V',1,3,6,5,'','Fecha',''),(67,'2023-03-12','L',1,3,1,5,'','Fecha',''),(68,'2023-02-26','V',2,1,15,5,'','Fecha',''),(69,'2025-05-25','L',1,1,11,1,'Juan Criz Espip','Fecha',''),(70,'2025-06-01','V',2,2,9,1,'Daniel Pereyra','Fecha',''),(71,'2022-12-11','V',0,3,6,6,'','FinVue',''),(72,'2022-12-04','L',0,0,6,6,'','FinIda',''),(73,'2022-11-27','V',1,0,7,6,'','SemVue',''),(74,'2022-11-20','L',2,1,7,6,'','SemIda',''),(75,'2022-11-12','V',3,1,9,6,'','CuaVue',''),(76,'2022-11-06','L',1,0,9,6,'','CuaIda',''),(77,'2022-10-30','L',4,0,3,6,'','Oct','');
/*!40000 ALTER TABLE `historial_partido` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-06 13:48:49
