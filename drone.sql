-- MySQL dump 10.13  Distrib 9.6.0, for macos15 (arm64)
--
-- Host: localhost    Database: drone
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '1999501c-04a3-11f1-bbf9-e63e85e0d383:1-36';

--
-- Table structure for table `active_drones`
--

DROP TABLE IF EXISTS `active_drones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `active_drones` (
  `drone_name` varchar(30) NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`drone_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `active_drones`
--

LOCK TABLES `active_drones` WRITE;
/*!40000 ALTER TABLE `active_drones` DISABLE KEYS */;
/*!40000 ALTER TABLE `active_drones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drone_info`
--

DROP TABLE IF EXISTS `drone_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drone_info` (
  `drone_name` varchar(30) NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  `firmware` varchar(7) DEFAULT NULL,
  `ip_addr` varchar(40) DEFAULT NULL,
  `port` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`drone_name`),
  UNIQUE KEY `drone_name` (`drone_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drone_info`
--

LOCK TABLES `drone_info` WRITE;
/*!40000 ALTER TABLE `drone_info` DISABLE KEYS */;
INSERT INTO `drone_info` VALUES ('dron','sitl','ARD','127.0.0.1','433'),('drona','SITL','ARD',NULL,NULL),('drone','SITL','PX',NULL,NULL),('dronea','SITL','PX',NULL,NULL),('kk','sitl','ARD','128.0.1.2','2'),('savah','sitl','ARD','127.0.0.1','14540'),('suhaan','sitl','ARD','127.0.0.1','433');
/*!40000 ALTER TABLE `drone_info` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-18 11:44:09
