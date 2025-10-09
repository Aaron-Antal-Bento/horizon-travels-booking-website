CREATE DATABASE  IF NOT EXISTS `horizontravels2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `horizontravels2`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: horizontravels
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `BookingID` int NOT NULL AUTO_INCREMENT,
  `UserID` int DEFAULT NULL,
  `CardID` int DEFAULT NULL,
  `JourneyID` int DEFAULT NULL,
  `StandardSeats` int DEFAULT '0',
  `FirstClassSeats` int DEFAULT '0',
  `PricePaidPerSeat` int DEFAULT NULL,
  `BookingDate` datetime DEFAULT NULL,
  `JourneyDate` date DEFAULT NULL,
  `BookingRefrence` varchar(10) DEFAULT NULL,
  `Cancelled` tinyint DEFAULT '0',
  `RefundAmount` int DEFAULT NULL,
  PRIMARY KEY (`BookingID`),
  UNIQUE KEY `BookingID_UNIQUE` (`BookingID`) /*!80000 INVISIBLE */,
  UNIQUE KEY `BookingRefrence_UNIQUE` (`BookingRefrence`),
  KEY `JourneyID` (`JourneyID`),
  KEY `UserID_b` (`UserID`) /*!80000 INVISIBLE */,
  KEY `CardID_b` (`CardID`),
  CONSTRAINT `CardID_b` FOREIGN KEY (`CardID`) REFERENCES `cardinfo` (`CardID`),
  CONSTRAINT `JourneyID` FOREIGN KEY (`JourneyID`) REFERENCES `journeys` (`JourneyID`),
  CONSTRAINT `UserID_b` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (10,1,2,34,1,0,200,'2025-03-30 00:00:00','2025-03-30','T-A-BR-MA',0,NULL),(11,1,2,34,1,0,200,'2025-03-30 00:00:00','2025-03-30','T-B-BR-MA',0,NULL),(12,NULL,4,34,1,0,200,'2025-03-30 00:00:00','2025-03-30','T-0C-BR-MA',0,NULL),(13,1,4,23,1,0,225,'2025-03-30 00:00:00','2025-03-30','T-0D-BR-NC',0,NULL),(14,6,6,5,5,0,80,'2025-04-02 02:02:00','2025-04-01','T-0E-MA-BR',0,NULL),(15,1,2,15,0,1,240,'2025-04-01 00:00:00','2025-04-01','T-0F-DU-PO',0,NULL),(16,32,7,15,0,1,240,'2025-04-01 09:21:17','2025-04-01','T-10-DU-PO',0,NULL),(17,32,7,13,4,0,80,'2025-04-01 09:37:03','2025-04-10','T-11-BR-MA',0,NULL),(18,32,7,14,0,2,240,'2025-04-01 09:37:50','2025-04-01','T-12-PO-DU',0,NULL),(19,32,7,36,0,1,450,'2025-04-01 09:41:02','2025-04-01','T-13-SO-MA',0,NULL),(20,32,7,15,1,0,120,'2025-04-01 09:44:04','2025-04-01','T-14-DU-PO',0,NULL),(21,32,7,14,1,0,120,'2025-04-01 10:03:55','2025-04-01','T-15-PO-DU',0,NULL),(22,32,7,14,1,0,120,'2025-04-01 10:29:37','2025-04-01','T-16-PO-DU',0,NULL),(23,32,7,8,1,0,100,'2025-04-01 10:39:14','2025-04-01','T-17-MA-GL',0,NULL),(24,32,7,28,0,1,500,'2025-04-01 10:42:03','2025-04-01','T-18-LD-MA',0,NULL),(25,32,7,14,1,0,120,'2025-04-01 10:43:39','2025-04-01','T-19-PO-DU',0,NULL),(26,1,3,7,1,0,100,'2025-04-01 10:45:06','2025-04-01','T-1A-LD-MA',0,NULL),(27,1,1,26,0,1,400,'2025-04-01 10:45:38','2025-04-01','T-1B-MA-BR',0,NULL),(28,1,2,29,1,0,250,'2025-04-01 10:46:22','2025-04-01','T-1C-MA-GL',0,NULL),(29,NULL,2,17,1,0,90,'2025-04-01 10:47:51','2025-04-01','T-1D-SO-MA',0,NULL),(30,1,3,25,1,0,200,'2025-04-01 10:48:53','2025-04-01','T-1E-BR-MA',0,NULL),(33,1,2,31,1,0,250,'2025-04-01 13:53:56','2025-04-01','T-21-GL-NC',0,NULL),(34,1,2,31,1,0,250,'2025-04-01 13:54:44','2025-04-01','T-22-GL-NC',0,NULL),(35,1,1,19,1,0,100,'2025-04-01 13:56:47','2025-04-01','T-23-BM-NC',0,NULL),(36,1,1,31,1,0,250,'2025-04-01 13:58:03','2025-04-01','T-24-GL-NC',0,NULL),(37,34,8,10,0,1,200,'2025-04-02 13:26:27','2025-04-02','T-25-GL-NC',0,NULL),(38,6,6,10,1,0,100,'2025-04-02 13:30:28','2025-04-02','T-26-GL-NC',0,NULL),(39,NULL,1,19,1,0,100,'2025-04-02 13:55:13','2025-04-02','T-27-BM-NC',0,NULL),(40,NULL,2,38,1,0,250,'2025-04-06 16:36:17','2025-04-06','T-28-BM-NC',0,NULL),(41,NULL,2,19,1,0,100,'2025-04-07 13:26:29','2025-04-07','T-29-BM-NC',0,NULL),(42,1,2,32,8,0,250,'2025-04-07 14:45:16','2025-04-07','T-2A-NC-MA',0,NULL),(43,NULL,1,19,1,0,100,'2025-04-07 14:46:37','2025-04-07','T-2B-BM-NC',0,NULL),(44,NULL,2,14,1,0,120,'2025-04-09 11:01:56','2025-04-09','T-2C-PO-DU',0,NULL),(45,NULL,2,8,1,0,100,'2025-04-09 11:18:21','2025-04-09','T-2D-MA-GL',0,NULL),(46,NULL,2,17,1,0,90,'2025-04-09 11:18:31','2025-04-09','T-2E-SO-MA',0,NULL),(47,35,10,7,1,0,100,'2025-04-09 12:34:05','2025-04-09','T-2F-LD-MA',0,NULL),(48,1,2,26,1,0,200,'2025-04-09 12:45:55','2025-04-09','T-30-MA-BR',0,NULL),(49,1,1,19,1,0,100,'2025-04-09 13:20:36','2025-04-09','T-31-BM-NC',0,NULL),(50,1,1,13,1,0,60,'2025-04-09 14:03:20','2025-06-30','T-32-BR-MA',1,60),(51,1,1,10,1,0,100,'2025-04-09 14:13:41','2025-05-14','T-33-GL-NC',0,NULL),(52,1,2,11,0,2,200,'2025-04-09 15:10:41','2025-04-09','T-34-NC-MA',0,NULL),(53,1,2,1,1,0,90,'2025-04-17 14:19:54','2025-04-17','T-35-NC-BR',0,NULL),(55,NULL,12,18,1,0,90,'2025-04-17 17:57:19','2025-04-17','T-37-MA-SO',1,90),(56,NULL,13,12,1,0,80,'2025-04-17 18:03:12','2025-04-17','T-38-MA-BR',1,48),(59,1,1,27,1,0,200,'2025-04-18 12:18:39','2025-04-19','T-3B-BR-LD',0,NULL),(60,1,2,23,0,3,450,'2025-04-18 12:19:28','2025-04-19','T-3C-BR-NC',0,NULL),(61,1,2,4,1,0,80,'2025-04-18 12:25:39','2025-04-18','T-3D-BR-MA',0,NULL),(62,1,2,4,1,0,80,'2025-04-18 12:27:50','2025-04-18','T-3E-BR-MA',0,NULL),(63,1,2,4,1,0,80,'2025-04-18 12:28:40','2025-04-18','T-3F-BR-MA',0,NULL),(64,1,2,15,1,0,120,'2025-04-18 12:29:52','2025-04-22','T-40-DU-PO',0,NULL),(65,1,1,13,8,0,80,'2025-04-21 00:41:53','2025-04-21','T-41-BR-MA',0,NULL),(66,1,2,4,0,1,160,'2025-04-23 12:20:46','2025-04-23','T-42-BR-MA',0,NULL),(67,1,1,19,0,5,200,'2025-04-25 01:48:06','2025-05-08','T-43-BM-NC',0,NULL),(68,1,1,24,0,3,405,'2025-04-25 01:48:34','2025-06-19','T-44-CF-ED',0,NULL),(69,1,2,13,1,0,80,'2025-04-28 21:31:47','2025-05-29','T-45-BR-MA',1,48),(70,1,1,15,1,0,120,'2025-04-29 09:08:20','2025-04-29','T-46-DU-PO',0,NULL),(71,1,2,14,1,0,120,'2025-04-29 09:10:00','2025-04-29','T-47-PO-DU',0,NULL),(72,1,1,19,1,0,100,'2025-04-30 12:49:12','2025-04-30','T-48-BM-NC',0,NULL),(73,17,14,5,1,0,80,'2025-04-10 13:19:20','2025-04-10','T-49-MA-BR',0,NULL),(74,17,15,32,0,1,500,'2025-04-20 13:21:06','2025-04-20','T-4A-NC-MA',0,NULL),(75,17,16,34,1,0,200,'2025-04-30 13:22:28','2025-05-01','T-4B-BR-MA',0,NULL),(76,17,15,30,1,0,275,'2025-04-30 13:23:42','2025-05-31','T-4C-BR-GL',0,NULL),(77,17,14,24,4,0,191,'2025-04-30 13:24:19','2025-07-01','T-4D-CF-ED',1,191),(78,NULL,17,6,0,1,160,'2025-04-30 15:49:13','2025-05-01','T-4E-BR-LD',1,0),(80,17,15,22,1,0,225,'2025-04-30 17:25:29','2025-04-30','T-50-NC-BR',0,NULL),(81,17,15,22,1,0,225,'2025-04-30 17:28:29','2025-04-30','T-51-NC-BR',0,NULL);
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cardinfo`
--

DROP TABLE IF EXISTS `cardinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cardinfo` (
  `CardID` int NOT NULL AUTO_INCREMENT,
  `UserID` int DEFAULT NULL,
  `CardNumber` varchar(20) DEFAULT NULL,
  `ExpDate` varchar(5) DEFAULT NULL,
  `CVV` varchar(3) DEFAULT NULL,
  `NameOnCard` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`CardID`),
  UNIQUE KEY `CardID_UNIQUE` (`CardID`),
  KEY `UserID_c` (`UserID`),
  CONSTRAINT `UserID_c` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cardinfo`
--

LOCK TABLES `cardinfo` WRITE;
/*!40000 ALTER TABLE `cardinfo` DISABLE KEYS */;
INSERT INTO `cardinfo` VALUES (1,1,'9876 5432 1098 7654','03/27','987','Aaron A-B'),(2,1,'1234 5678 9012 3456','02/26','123','Aaron Antal-Bento'),(3,NULL,'0000 0000 0000 0000','01/26','123','Aaron Agoas Antal-bento'),(4,NULL,'1111 1111 1111 1111','12/27','888','AB'),(5,NULL,'3333 3333 3333 3333','01/30','000','Charles'),(6,6,'4444 4444 4567 8888','02/29','555','HT Business'),(7,32,'1234 5676 5432 3456','02/27','444','James Waters'),(8,NULL,'8125 3198 9279 2762','01/34','324','Reggi tomas'),(9,1,'2134 4345 3322 3456','01/23','111','Old card'),(10,35,'1257 8941 5413 8514','12/34','134','booker belt'),(12,NULL,'0000 0000 0000 0000','10/27','123','myCard'),(13,NULL,'2134 5617 2389 6214','12/29','321','grey al'),(14,17,'2187 5327 8927 5328','05/26','000','Admin card'),(15,17,'0931 4816 4973 0569','07/27','342','HT company'),(16,17,'3027 8329 6592 5623','02/25','432','Old card'),(17,NULL,'1243 9547 8963 0233','06/29','124','Aaron Antal-bento');
/*!40000 ALTER TABLE `cardinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company` (
  `CompanyID` int NOT NULL AUTO_INCREMENT,
  `CompanyName` varchar(45) DEFAULT NULL,
  `CompanyAddress` varchar(100) DEFAULT NULL,
  `BusinessSeats` int DEFAULT NULL,
  `EconomySeats` int DEFAULT NULL,
  PRIMARY KEY (`CompanyID`),
  UNIQUE KEY `CompanyID_UNIQUE` (`CompanyID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (1,'UKAir','Bassingbourn Road, London Stansted Airport, Stansted, England, CM24 1QW',26,104),(2,'BritishTrains','Milford House, 1 Milford Street, Swindon, SN1 1HL',50,200),(3,'GBBusses','Templeback, 10 Temple Back, Bristol, United Kingdom, BS1 6FL',9,36);
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journeys`
--

DROP TABLE IF EXISTS `journeys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `journeys` (
  `JourneyID` int NOT NULL AUTO_INCREMENT,
  `CompanyID` int DEFAULT NULL,
  `Origin` varchar(45) DEFAULT NULL,
  `DepartureTime` time DEFAULT NULL,
  `Destination` varchar(45) DEFAULT NULL,
  `ArrivalTime` time DEFAULT NULL,
  `Price` int DEFAULT NULL,
  PRIMARY KEY (`JourneyID`),
  UNIQUE KEY `JourneyID_UNIQUE` (`JourneyID`),
  KEY `CompanyID` (`CompanyID`),
  CONSTRAINT `CompanyID` FOREIGN KEY (`CompanyID`) REFERENCES `company` (`CompanyID`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journeys`
--

LOCK TABLES `journeys` WRITE;
/*!40000 ALTER TABLE `journeys` DISABLE KEYS */;
INSERT INTO `journeys` VALUES (1,1,'Newcastle','17:45:00','Bristol','19:00:00',9000),(2,1,'Bristol','09:00:00','Newcastle','10:15:00',9000),(3,1,'Cardiff','07:00:00','Edinburgh','08:30:00',9000),(4,1,'Bristol','12:30:00','Manchester','13:30:00',8000),(5,1,'Manchester','13:20:00','Bristol','14:20:00',8000),(6,1,'Bristol','07:40:00','London','08:20:00',8000),(7,1,'London','13:00:00','Manchester','14:00:00',10000),(8,1,'Manchester','12:20:00','Glasgow','13:30:00',10000),(9,1,'Bristol','08:40:00','Glasgow','09:45:00',11000),(10,1,'Glasgow','14:30:00','Newcastle','15:45:00',10000),(11,1,'Newcastle','16:15:00','Manchester','17:05:00',10000),(12,1,'Manchester','18:25:00','Bristol','19:30:00',8000),(13,1,'Bristol','06:20:00','Manchester','07:20:00',8000),(14,1,'Portsmouth','12:00:00','Dundee','14:00:00',12000),(15,1,'Dundee','10:00:00','Portsmouth','12:00:00',12000),(16,1,'Edinburgh','18:30:00','Cardiff','20:00:00',9000),(17,1,'Southampton','12:00:00','Manchester','13:30:00',9000),(18,1,'Manchester','19:00:00','Southampton','20:30:00',9000),(19,1,'Birmingham','17:00:00','Newcastle','17:45:00',10000),(20,1,'Newcastle','07:00:00','Birmingham','07:45:00',10000),(21,1,'Aberdeen','08:00:00','Portsmouth','09:30:00',10000),(22,2,'Newcastle','17:45:00','Bristol','24:00:00',22500),(23,2,'Bristol','09:00:00','Newcastle','15:15:00',22500),(24,2,'Cardiff','07:00:00','Edinburgh','14:30:00',22500),(25,2,'Bristol','12:30:00','Manchester','17:30:00',20000),(26,2,'Manchester','13:20:00','Bristol','18:20:00',20000),(27,2,'Bristol','07:40:00','London','10:20:00',20000),(28,2,'London','13:00:00','Manchester','18:00:00',25000),(29,2,'Manchester','12:20:00','Glasgow','18:10:00',25000),(30,2,'Bristol','08:40:00','Glasgow','13:25:00',27500),(31,2,'Glasgow','14:30:00','Newcastle','20:45:00',25000),(32,2,'Newcastle','16:15:00','Manchester','20:25:00',25000),(33,2,'Manchester','18:25:00','Bristol','23:50:00',20000),(34,2,'Bristol','06:20:00','Manchester','11:20:00',20000),(35,2,'Edinburgh','18:30:00','Cardiff','26:00:00',22500),(36,2,'Southampton','12:00:00','Manchester','19:30:00',22500),(37,2,'Manchester','19:00:00','Southampton','26:30:00',22500),(38,2,'Birmingham','17:00:00','Newcastle','20:45:00',25000),(39,2,'Newcastle','07:00:00','Birmingham','10:45:00',25000);
/*!40000 ALTER TABLE `journeys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `traveldays`
--

DROP TABLE IF EXISTS `traveldays`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `traveldays` (
  `TravelDayID` int NOT NULL AUTO_INCREMENT,
  `CompanyID` int DEFAULT NULL,
  `Weekday` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`TravelDayID`),
  UNIQUE KEY `idtraveldays_UNIQUE` (`TravelDayID`),
  KEY `CompanyID` (`CompanyID`),
  CONSTRAINT `Company_ID` FOREIGN KEY (`CompanyID`) REFERENCES `company` (`CompanyID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `traveldays`
--

LOCK TABLES `traveldays` WRITE;
/*!40000 ALTER TABLE `traveldays` DISABLE KEYS */;
INSERT INTO `traveldays` VALUES (1,1,'Monday'),(2,2,'Monday'),(3,1,'Tuesday'),(4,2,'Tuesday'),(5,1,'Wednesday'),(6,2,'Wednesday'),(7,1,'Thursday'),(8,2,'Thursday'),(9,1,'Friday'),(10,2,'Friday'),(11,2,'Saturday'),(12,2,'Sunday');
/*!40000 ALTER TABLE `traveldays` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(45) NOT NULL,
  `Last_Name` varchar(45) DEFAULT NULL,
  `Email` varchar(45) NOT NULL,
  `Password` varchar(128) NOT NULL,
  `RegDate` date DEFAULT NULL,
  `RegTime` time DEFAULT NULL,
  `UserType` varchar(45) DEFAULT 'Standard',
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `UserID_UNIQUE` (`UserID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Aaron','Antal-bento','aaron.antalbento@gmail.com','$5$rounds=535000$MZVPpQBpIrxKQGK2$NlMZreCFmYL8HXwum9I.MESkTp8uK9xScv878ko56b5','2025-03-23',NULL,'Admin'),(6,'Horizon','','ht@horizon.com','$5$rounds=535000$zSvWNiU1PN6nhjI0$X0fFiHkIn0OWva6J5BbiWJOwIrWhuKdbySFSQsjwjrA',NULL,NULL,'Standard'),(7,'Freddy','James','freddyj@gmail.com','$5$rounds=535000$PaJph5xrcQ2.LrFY$LEBd3rS.A9v1Zc67ke6/oXAyz3/WzA18oF1Z8oLvix0',NULL,NULL,'Standard'),(8,'Kayleigh','Bell','kayleigh.bell2006@icloud.com','$5$rounds=535000$w5yUk06vTVvMkG4I$sjUDgg2kKkAXpImaJXZsn2fNMsjQ7MVKjfw/0bh.E32',NULL,NULL,'Admin'),(9,'Michael','','michael@yahoo.com','$5$rounds=535000$a3sFxpQNy6y.gH/W$pBTYfkSCt5Onq7wZaEp/ZVxMqs8NtdATKWyczukuCI.',NULL,NULL,'Standard'),(10,'Alexander','','a@gmail.co.uk','$5$rounds=535000$MoavECOIBwy1enpR$Im9E1Fqfm1ecPLB/Q0v4rphzWuMeLqkbiwxScK.d3M1',NULL,NULL,'Standard'),(12,'Alphie','','alph@icloud.com','$5$rounds=535000$9i9utyD.D86beXys$n6aS9tT5OEQfSo99EUYNcHNRpqAZxaQ7CQBEJR94PJ9',NULL,NULL,'Standard'),(16,'Zander','Sugar','z@gmail.com','$5$rounds=535000$qRqlZJixpFtHbCln$fy7RjQfsnOOI5OiPe7J020XKXNYUoYt6RB2J.imgrL3','2025-03-12','16:19:24','Standard'),(17,'Admin1','','admin@horizon.com','$5$rounds=535000$TRl9Xlro1ysouJQs$dfq94Ihla7urjlu1rtatc7o4oLPvxqasYJLwJlNv4gB','2025-03-12','16:50:44','Admin'),(23,'Henry','James-Lee','h@horizon.com','$5$rounds=535000$Q7Ov0dcVgWpOaV19$.ah2jneLSW/kQG4LyV60LvLYxpGBWLkHrzQ680s05l0','2025-03-23','12:45:57','Standard'),(30,'Nuno','Bento','osteopathy@nunobento.co.uk','$5$rounds=535000$OtVH04E3dnxJ4M0R$u/UuFXAOpcnRyX9YmyuREQMd77Rg2R3d8PcMFj0Hmy/','2025-03-29','15:28:40','Standard'),(31,'Harriett','','hb@gmail.com','$5$rounds=535000$mGX3l9qmiRtuYdTU$zZ6KTAV53/aqHPgkWl6cNDqfZcTkA346dE4cEu2FylD','2025-03-29','22:51:58','Standard'),(32,'James','','j@icloud.com','$5$rounds=535000$WRkkFZNwdSp/EDzZ$L5Oe4MmMjbVSWio76fnYflNbzeBhfJpJ8lUUwRLafy8','2025-04-01','09:09:08','Standard'),(33,'Jeremy','','ja@gmail.com','$5$rounds=535000$Bf.tEXdfLedBz2By$THwlEAZxPfzmn2pCXiaAHft6I8cJBF0gQ0uXD/sim18','2025-04-01','15:27:49','Standard'),(34,'Reggi','','r@icloud.com','$5$rounds=535000$ScZfcXduEdKPn4BK$sVXO0U18YmieH7ai7aIqPNFsSpKrSOQnEBcRVeS9RhC','2025-04-02','13:18:45','Standard'),(35,'Booker','','b@gmail.com','$5$rounds=535000$Gh9QYKIJ5dakki8Z$TSjrm9zl83VxBSq.eMH0G5bkVAF1EZx/U5FIpGeQcnA','2025-04-09','12:31:30','Standard'),(39,'Peter','Walker','p@icloud.com','$5$rounds=535000$5aXC4/HfW7w1/6XS$n2Qnh.YWd1CtiyUL32lqIFqVARQmaC6U4QuT4Qp/my5','2025-04-20','23:56:44','Standard'),(40,'Juliet','Sim','js@gmail.com','$5$rounds=535000$tiH3Jc3ypDfeK8wq$Yp6yVj6XtcYLEUgKBEkaumdlBNLeYUDcAHuoGjNxvv3','2025-04-21','00:00:47','Standard'),(41,'Aaron','','test2@gmail.com','$5$rounds=535000$UQ.gstmONzrgFDi2$TSgeT8PyPrZmQSp8.QhwGdKHkYRILRTPuYYWSkEz1yD','2025-04-30','14:57:06','Standard');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-30 21:31:28
