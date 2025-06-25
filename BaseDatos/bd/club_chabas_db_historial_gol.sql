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
-- Table structure for table `historial_gol`
--

DROP TABLE IF EXISTS `historial_gol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_gol` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `minuto` int unsigned NOT NULL,
  `jugador_id` bigint NOT NULL,
  `partido_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `historial_gol_partido_id_21a7780c_fk_historial_partido_id` (`partido_id`),
  KEY `historial_gol_jugador_id_36118bc4_fk_historial_jugador_id` (`jugador_id`),
  CONSTRAINT `historial_gol_jugador_id_36118bc4_fk_historial_jugador_id` FOREIGN KEY (`jugador_id`) REFERENCES `historial_jugador` (`id`),
  CONSTRAINT `historial_gol_partido_id_21a7780c_fk_historial_partido_id` FOREIGN KEY (`partido_id`) REFERENCES `historial_partido` (`id`),
  CONSTRAINT `historial_gol_chk_1` CHECK ((`minuto` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_gol`
--

LOCK TABLES `historial_gol` WRITE;
/*!40000 ALTER TABLE `historial_gol` DISABLE KEYS */;
INSERT INTO `historial_gol` VALUES (1,5,9,1),(2,19,8,1),(3,52,1,1),(4,89,3,1),(5,0,8,2),(6,0,2,2),(7,0,8,2),(8,0,8,2),(9,0,1,2),(10,61,10,3),(11,1,5,3),(12,39,11,4),(13,0,1,5),(14,0,5,5),(15,0,28,8),(16,0,7,8),(17,0,23,8),(18,0,28,9),(19,0,20,9),(20,0,11,10),(21,0,28,10),(22,0,15,14),(23,0,30,15),(24,0,29,15),(25,0,11,15),(26,0,11,16),(27,0,30,16),(28,0,30,16),(29,0,1,16),(30,0,1,17),(31,0,7,17),(32,0,30,17),(33,0,11,18),(34,0,30,18),(35,0,11,19),(36,0,28,21),(37,0,28,22),(38,0,31,23),(39,0,1,23),(41,0,30,25),(42,0,1,25),(43,0,20,29),(44,0,29,29),(45,0,15,31),(46,0,3,33),(47,0,28,34),(48,0,28,34),(49,0,30,34),(50,0,21,35),(51,0,15,35),(52,0,24,36),(56,0,30,39),(57,0,33,39),(58,0,30,40),(59,0,30,41),(60,0,28,41),(61,0,20,41),(62,0,15,43),(63,0,28,45),(64,0,30,46),(65,0,29,47),(66,0,7,47),(67,0,1,48),(68,0,9,48),(69,0,34,48),(70,18,9,49),(71,23,9,49),(72,85,8,49),(73,14,11,50),(74,76,9,50),(75,88,35,50),(76,0,36,51),(77,0,37,52),(78,0,37,53),(79,0,39,54),(80,0,11,54),(81,0,28,55),(82,0,38,56),(83,0,6,56),(84,0,28,56),(85,0,10,56),(86,0,37,56),(87,0,31,57),(88,0,36,60),(89,0,41,60),(90,0,28,61),(91,0,36,61),(92,0,31,64),(93,0,31,65),(94,0,6,66),(95,0,28,67),(96,0,6,68),(97,0,31,68),(98,85,9,69),(99,50,1,70),(100,86,1,70),(101,0,11,73),(102,0,45,74),(103,0,49,74),(104,0,48,75),(105,0,39,75),(106,0,39,75),(107,0,39,76),(108,0,38,77),(109,0,41,77),(110,0,28,77),(111,0,50,77);
/*!40000 ALTER TABLE `historial_gol` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-06 13:48:50
