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
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('bsclb6tw514y3r44xdy7f09pr6nxl0o4','.eJxVjMsOgjAUBf-la9O0taUXl-75BnJfFdRAQmFl_HclYaHbMzPnZXrc1qHfqi79KOZivDn9boT80GkHcsfpNluep3UZye6KPWi13Sz6vB7u38GAdfjWIUfA6AWoUWk4R05U2uIKZGCHGpIHyGfygq0mCEAcJVChFKLjHMz7A-pCOA0:1u5CT2:cKIG2GqLDc9P0wH-q9WykjTMkDIebrTyNQWf3QhankU','2025-04-30 23:46:56.581250'),('hvov6zer151w3atw9hm839dp5oyqhdsd','.eJxVjEEOwiAQRe_C2pAOlQFcuu8ZmoEZpGpoUtqV8e7apAvd_vfef6mRtrWMW5NlnFhdFKjT7xYpPaTugO9Ub7NOc12XKepd0QdtephZntfD_Tso1Mq3DpRsRo_CCVlSipJdADQUs-nsGQwIZI7o0LpARMyxox6wh8553wf1_gATCThh:1uBxWI:E7ZjnZZjv7ivRnx5mR-rQScOwrl6vpmPzR72Sq8S8UE','2025-05-19 15:14:14.645933'),('ruixvyte2acktag3y4bkpv4xg2frhjmt','.eJxVjEEOwiAQRe_C2pAOlQFcuu8ZmoEZpGpoUtqV8e7apAvd_vfef6mRtrWMW5NlnFhdFKjT7xYpPaTugO9Ub7NOc12XKepd0QdtephZntfD_Tso1Mq3DpRsRo_CCVlSipJdADQUs-nsGQwIZI7o0LpARMyxox6wh8553wf1_gATCThh:1uHT8Q:H9D2zfSgPyXti3q3XSSTG-NbPEHaOPczbbsQTFsNqUk','2025-06-03 20:00:22.144930'),('x160ag0nrhscss04lyr6l568zw5s8qi5','.eJxVjEEOwiAQRe_C2pAOlQFcuu8ZmoEZpGpoUtqV8e7apAvd_vfef6mRtrWMW5NlnFhdFKjT7xYpPaTugO9Ub7NOc12XKepd0QdtephZntfD_Tso1Mq3DpRsRo_CCVlSipJdADQUs-nsGQwIZI7o0LpARMyxox6wh8553wf1_gATCThh:1uNAmo:PI75hMNHx1Z7ysDoC_F-iCUPSAWti2BsiS7qGxQ2ofs','2025-06-19 13:37:38.770346');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
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
