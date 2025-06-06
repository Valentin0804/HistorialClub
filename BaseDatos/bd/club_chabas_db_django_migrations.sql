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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-16 23:45:51.909708'),(2,'auth','0001_initial','2025-04-16 23:45:52.427937'),(3,'admin','0001_initial','2025-04-16 23:45:52.633124'),(4,'admin','0002_logentry_remove_auto_add','2025-04-16 23:45:52.647169'),(5,'admin','0003_logentry_add_action_flag_choices','2025-04-16 23:45:52.658712'),(6,'contenttypes','0002_remove_content_type_name','2025-04-16 23:45:52.813729'),(7,'auth','0002_alter_permission_name_max_length','2025-04-16 23:45:52.909046'),(8,'auth','0003_alter_user_email_max_length','2025-04-16 23:45:52.940147'),(9,'auth','0004_alter_user_username_opts','2025-04-16 23:45:52.953192'),(10,'auth','0005_alter_user_last_login_null','2025-04-16 23:45:53.038976'),(11,'auth','0006_require_contenttypes_0002','2025-04-16 23:45:53.041985'),(12,'auth','0007_alter_validators_add_error_messages','2025-04-16 23:45:53.053023'),(13,'auth','0008_alter_user_username_max_length','2025-04-16 23:45:53.138813'),(14,'auth','0009_alter_user_last_name_max_length','2025-04-16 23:45:53.203023'),(15,'auth','0010_alter_group_name_max_length','2025-04-16 23:45:53.224093'),(16,'auth','0011_update_proxy_permissions','2025-04-16 23:45:53.236133'),(17,'auth','0012_alter_user_first_name_max_length','2025-04-16 23:45:53.295835'),(18,'historial','0001_initial','2025-04-16 23:45:53.954029'),(19,'sessions','0001_initial','2025-04-16 23:45:54.010717'),(20,'historial','0002_partido_arbitro_partido_instancia','2025-04-21 16:08:32.895552'),(21,'historial','0003_remove_jugador_fecha_ingreso_and_more','2025-05-20 20:44:11.167061'),(22,'historial','0004_partido_descripcion','2025-05-22 22:58:55.515263');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
