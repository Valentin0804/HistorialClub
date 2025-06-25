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
-- Table structure for table `historial_tarjetaroja`
--

DROP TABLE IF EXISTS `historial_tarjetaroja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_tarjetaroja` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `minuto` int unsigned NOT NULL,
  `jugador_id` bigint NOT NULL,
  `partido_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `historial_tarjetaroj_jugador_id_c641714a_fk_historial` (`jugador_id`),
  KEY `historial_tarjetaroj_partido_id_d4f93b8e_fk_historial` (`partido_id`),
  CONSTRAINT `historial_tarjetaroj_jugador_id_c641714a_fk_historial` FOREIGN KEY (`jugador_id`) REFERENCES `historial_jugador` (`id`),
  CONSTRAINT `historial_tarjetaroj_partido_id_d4f93b8e_fk_historial` FOREIGN KEY (`partido_id`) REFERENCES `historial_partido` (`id`),
  CONSTRAINT `historial_tarjetaroja_chk_1` CHECK ((`minuto` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_tarjetaroja`
--

LOCK TABLES `historial_tarjetaroja` WRITE;
/*!40000 ALTER TABLE `historial_tarjetaroja` DISABLE KEYS */;
INSERT INTO `historial_tarjetaroja` VALUES (1,0,4,4),(2,0,7,5),(3,0,7,7),(4,0,27,14),(5,0,23,16),(6,0,15,18),(7,0,30,22),(8,0,28,26),(9,0,16,26),(10,0,15,30),(11,0,23,47),(12,0,5,50),(13,0,13,50),(14,0,5,51),(15,0,38,54),(16,0,40,54),(17,0,10,58),(18,0,6,62),(19,0,10,65),(20,0,46,71),(21,0,41,71),(22,0,47,71),(23,0,28,74);
/*!40000 ALTER TABLE `historial_tarjetaroja` ENABLE KEYS */;
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
