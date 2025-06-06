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
-- Table structure for table `historial_tarjetaamarilla`
--

DROP TABLE IF EXISTS `historial_tarjetaamarilla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_tarjetaamarilla` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `minuto` int unsigned NOT NULL,
  `jugador_id` bigint NOT NULL,
  `partido_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `historial_tarjetaama_jugador_id_2021a215_fk_historial` (`jugador_id`),
  KEY `historial_tarjetaama_partido_id_0458f3a3_fk_historial` (`partido_id`),
  CONSTRAINT `historial_tarjetaama_jugador_id_2021a215_fk_historial` FOREIGN KEY (`jugador_id`) REFERENCES `historial_jugador` (`id`),
  CONSTRAINT `historial_tarjetaama_partido_id_0458f3a3_fk_historial` FOREIGN KEY (`partido_id`) REFERENCES `historial_partido` (`id`),
  CONSTRAINT `historial_tarjetaamarilla_chk_1` CHECK ((`minuto` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=177 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_tarjetaamarilla`
--

LOCK TABLES `historial_tarjetaamarilla` WRITE;
/*!40000 ALTER TABLE `historial_tarjetaamarilla` DISABLE KEYS */;
INSERT INTO `historial_tarjetaamarilla` VALUES (1,0,6,2),(2,0,5,2),(3,0,6,3),(5,0,12,5),(6,0,5,5),(7,0,13,5),(8,0,14,5),(9,0,8,4),(10,0,10,3),(11,0,15,3),(12,0,5,1),(13,0,23,7),(14,0,21,7),(15,0,29,7),(16,0,28,7),(17,0,11,7),(18,0,24,7),(19,0,17,7),(20,0,20,8),(21,0,3,8),(22,0,21,9),(23,0,28,10),(24,0,11,10),(25,0,21,10),(26,0,17,10),(27,0,3,11),(28,0,20,11),(29,0,7,11),(30,0,11,11),(31,0,3,12),(32,0,7,12),(33,0,12,13),(34,0,11,13),(35,0,5,13),(36,0,31,14),(37,0,15,14),(38,0,13,15),(39,0,28,17),(40,0,7,17),(41,0,30,18),(42,0,13,18),(43,0,27,18),(44,0,23,19),(45,0,30,19),(46,0,15,19),(47,0,20,20),(48,0,14,20),(49,0,23,20),(50,0,16,20),(51,0,28,21),(52,0,20,21),(53,0,23,21),(54,0,3,22),(55,0,32,22),(56,0,29,23),(57,0,21,23),(58,0,28,23),(59,0,17,23),(63,0,21,25),(64,0,14,25),(65,0,23,25),(66,0,24,26),(67,0,15,27),(68,0,16,27),(69,0,7,27),(70,0,28,28),(71,0,16,28),(72,0,21,28),(73,0,20,29),(74,0,28,29),(75,0,16,29),(76,0,21,30),(77,0,14,31),(78,0,30,31),(79,0,13,31),(80,0,11,32),(81,0,24,33),(82,0,28,33),(83,0,23,33),(84,0,20,34),(85,0,25,35),(86,0,20,35),(87,0,25,36),(88,0,33,36),(89,0,25,38),(90,0,26,38),(91,0,31,38),(92,0,23,40),(93,0,23,41),(94,0,28,41),(95,0,13,42),(96,0,19,42),(97,0,21,42),(98,0,20,43),(99,0,13,43),(100,0,19,44),(101,0,21,44),(102,0,23,44),(103,0,24,44),(104,0,3,45),(105,0,11,46),(106,0,20,46),(107,0,21,46),(108,0,26,46),(109,0,17,46),(110,0,14,47),(111,0,15,47),(112,0,28,47),(113,0,11,50),(114,0,9,50),(115,0,36,51),(116,0,14,52),(117,0,38,52),(118,0,14,53),(119,0,11,54),(120,0,13,54),(121,0,32,54),(122,0,38,55),(123,0,31,56),(124,0,41,56),(125,0,42,57),(126,0,37,57),(127,0,6,57),(128,0,28,57),(129,0,36,57),(130,0,43,58),(131,0,5,58),(132,0,39,58),(133,0,43,59),(134,0,43,60),(135,0,13,60),(136,0,41,60),(137,0,14,61),(138,0,39,61),(139,0,5,61),(140,0,44,61),(141,0,31,62),(142,0,41,62),(143,0,6,63),(144,0,31,63),(145,0,41,64),(146,0,32,64),(147,0,38,64),(148,0,15,64),(149,0,13,65),(150,0,31,65),(151,0,38,66),(152,0,41,66),(153,0,10,66),(154,0,6,68),(155,0,31,68),(156,0,12,69),(157,0,12,70),(158,0,6,70),(159,0,44,71),(160,0,45,71),(161,0,47,72),(162,0,28,72),(163,0,48,72),(164,0,47,73),(165,0,14,73),(166,0,46,74),(167,0,45,74),(168,0,31,76),(169,0,46,76),(170,0,11,76),(171,0,48,76),(172,0,39,76),(173,0,6,76),(174,0,38,77),(175,0,41,77),(176,0,46,77);
/*!40000 ALTER TABLE `historial_tarjetaamarilla` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-06 13:48:51
