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
-- Table structure for table `historial_club`
--

DROP TABLE IF EXISTS `historial_club`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_club` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `localidad` varchar(100) NOT NULL,
  `fundacion` date NOT NULL,
  `escudo` varchar(100) DEFAULT NULL,
  `campeonatos` int unsigned NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `historial_club_chk_1` CHECK ((`campeonatos` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_club`
--

LOCK TABLES `historial_club` WRITE;
/*!40000 ALTER TABLE `historial_club` DISABLE KEYS */;
INSERT INTO `historial_club` VALUES (1,'Club Atlético Sportivo Matienzo','Pujato','1994-09-29','escudos/MatienzoPNG.png',0,1),(2,'Club Atlético Sanford','Sanford','1926-05-15','escudos/SanfordPNG.png',3,1),(3,'Casilda Club','Casilda','1994-09-29','escudos/CasildaClubPNG.png',0,1),(4,'Unión Casildense','Casilda','1986-06-29','escudos/UnionCasildensePNG.png',2,1),(5,'Racing de Villada','Villada','1950-02-19','escudos/RacingPNG.png',0,1),(6,'Belgrano','Arequito','1923-03-23','escudos/BelgranoPNG.png',12,1),(7,'Huracán','Chabás','1930-07-05','escudos/HuracanPNG.png',7,1),(8,'9 de Julio','Arequito','1918-06-18','escudos/9deJulioPNG.png',10,1),(9,'Atlético Pujato','Pujato','1934-01-31','escudos/PujatoPNG.png',8,1),(10,'Aprendices Casildenses','Casilda','1917-07-17','escudos/AprendicesPNG.png',15,1),(11,'Unión Deportiva','Los Molinos','1938-07-09','escudos/UnionDeportivaPNG.png',6,1),(12,'Alumni','Casilda','1907-08-04','escudos/AlumniPNG.png',18,1),(13,'Unidos Atlético Club','Zavalla','1981-06-16','escudos/UnidosPNG.png',0,1),(14,'Arnold Futbol Club','Coronel Arnold','1940-06-02','escudos/ArnoldPNG.png',0,0),(15,'Alianza Deportiva','Fuentes','2018-01-08','escudos/AlianzaPNG.png',0,1);
/*!40000 ALTER TABLE `historial_club` ENABLE KEYS */;
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
