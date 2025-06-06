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
-- Table structure for table `historial_participacionjugador`
--

DROP TABLE IF EXISTS `historial_participacionjugador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_participacionjugador` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `jugador_id` bigint NOT NULL,
  `torneo_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `historial_participacionj_jugador_id_torneo_id_c920ae7f_uniq` (`jugador_id`,`torneo_id`),
  KEY `historial_participac_torneo_id_4fa0711b_fk_historial` (`torneo_id`),
  CONSTRAINT `historial_participac_jugador_id_dfa84e1f_fk_historial` FOREIGN KEY (`jugador_id`) REFERENCES `historial_jugador` (`id`),
  CONSTRAINT `historial_participac_torneo_id_4fa0711b_fk_historial` FOREIGN KEY (`torneo_id`) REFERENCES `historial_torneo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_participacionjugador`
--

LOCK TABLES `historial_participacionjugador` WRITE;
/*!40000 ALTER TABLE `historial_participacionjugador` DISABLE KEYS */;
INSERT INTO `historial_participacionjugador` VALUES (4,1,1),(3,1,2),(5,2,1),(7,3,1),(6,3,2),(8,3,3),(9,4,1),(10,5,1),(11,7,1),(12,7,2),(13,7,3),(23,8,1),(22,9,1),(24,12,1),(21,16,2),(27,17,2),(28,17,3),(25,20,2),(26,20,3),(19,23,2),(20,23,3),(17,29,2),(18,29,3),(15,30,2),(16,30,3),(14,33,2),(2,34,1),(1,35,1),(30,36,4),(29,36,5),(32,37,4),(31,37,5),(33,38,4),(34,38,5),(35,39,4),(36,39,5),(37,40,4),(38,40,5),(40,41,4),(39,41,5),(42,42,4),(41,42,5),(44,43,4),(43,43,5),(46,44,4),(45,44,5),(47,45,6),(48,46,6),(49,47,6),(50,48,6),(51,49,6),(52,50,1);
/*!40000 ALTER TABLE `historial_participacionjugador` ENABLE KEYS */;
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
