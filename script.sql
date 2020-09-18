-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: qlsotietkiemdb
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Table structure for table `passbook`
--

DROP TABLE IF EXISTS `passbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passbook` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `created_date` datetime NOT NULL,
  `money` float NOT NULL,
  `phone` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `id_number` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `passbook_type_id` int NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `passbook_type_id` (`passbook_type_id`),
  CONSTRAINT `passbook_ibfk_1` FOREIGN KEY (`passbook_type_id`) REFERENCES `passbook_type` (`id`),
  CONSTRAINT `passbook_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passbook`
--

LOCK TABLES `passbook` WRITE;
/*!40000 ALTER TABLE `passbook` DISABLE KEYS */;
INSERT INTO `passbook` VALUES (1,'Meo meo meo ~~~~','abc dsaa ckasdjak','2020-09-01 10:13:00',1400000,'0941735205','123123',1,1),(2,'test','abc dsaa ckasdjak','2020-06-12 00:00:00',0,'0941735205','123123',2,0),(3,'Khanh Vo Pham Huyen','abc','2020-07-12 00:00:00',500000,'0941735205','123123',3,1),(4,'Võ Phạm Huyền Khanh','abc','2020-09-01 00:00:00',600000,'0941735205','1231231231',2,1),(5,'hiuhiuhiuh','abc dsaa ckasdjak','2020-09-12 00:00:00',700000,'0941735205','1231321',2,1),(6,'hihi','abc','2020-09-01 00:00:00',800000,'0941735205','09887776666',3,1),(7,'bbbbbbbbbbbbbbbbb','abc','2020-08-12 00:00:00',300000,'0941735205','1231231231',1,1),(8,'test','12','2020-09-13 00:00:00',200000,'0941735205','123112',2,1),(9,'tesst2','a','2020-09-01 00:00:00',350000,'0941735205','1',4,1),(10,'bui duc tien','nguyen thai son','2020-09-16 09:51:12',300000,'0941735205','ai bieet',1,1),(11,'tien','371 nguyen kiem','2020-09-16 12:09:50',200000,'0941735205','123123',3,1),(12,'tien no.2','nguyen kiem','2020-09-16 12:12:31',300000,'0941735205','09090909',4,1);
/*!40000 ALTER TABLE `passbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passbook_type`
--

DROP TABLE IF EXISTS `passbook_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passbook_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `interest_rate` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passbook_type`
--

LOCK TABLES `passbook_type` WRITE;
/*!40000 ALTER TABLE `passbook_type` DISABLE KEYS */;
INSERT INTO `passbook_type` VALUES (1,'Không kỳ hạn',0.2),(2,'3 tháng',0.3),(3,'4 tháng',0.4),(4,'5 tháng',0.5);
/*!40000 ALTER TABLE `passbook_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt`
--

DROP TABLE IF EXISTS `receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt` (
  `id` int NOT NULL AUTO_INCREMENT,
  `passbook_id` int NOT NULL,
  `customer_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `created_date` datetime NOT NULL,
  `money` float NOT NULL,
  `receipt_type_id` int NOT NULL,
  `creator_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `passbook_id` (`passbook_id`),
  KEY `receipt_type_id` (`receipt_type_id`),
  KEY `creator_id` (`creator_id`),
  CONSTRAINT `receipt_ibfk_1` FOREIGN KEY (`passbook_id`) REFERENCES `passbook` (`id`),
  CONSTRAINT `receipt_ibfk_2` FOREIGN KEY (`receipt_type_id`) REFERENCES `receipt_type` (`id`),
  CONSTRAINT `receipt_ibfk_3` FOREIGN KEY (`creator_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt`
--

LOCK TABLES `receipt` WRITE;
/*!40000 ALTER TABLE `receipt` DISABLE KEYS */;
INSERT INTO `receipt` VALUES (1,7,'bbbbbbbbbbbbbbbbb','2020-09-12 23:14:00',1231230000,2,3),(2,2,'Meo meo meo','2020-09-14 00:00:00',1000000,1,2),(3,3,'meo','2020-09-14 00:00:00',100002,1,3),(5,1,'test','2020-09-14 00:00:00',100049,1,5),(6,2,'Meo meo meo','2020-09-14 00:00:00',1231230000,2,3),(7,1,'Meo meo meo','2020-09-15 11:33:37',989898,1,1),(8,1,'Meo meo meo','2020-09-15 11:34:06',999999,1,1),(9,1,'Meo meo meo','2020-09-15 11:35:20',999999,1,1),(10,1,'Meo meo meo','2020-09-15 11:35:57',100090,1,1),(11,1,'Meo meo meo','2020-09-15 12:04:06',2000000000,1,4),(12,2,'Meo meo meo','2020-09-15 21:48:46',22222200000000,1,3),(13,1,'Meo meo meo','2020-09-15 21:56:27',200000,1,1),(14,1,'Meo meo meo','2020-09-16 00:05:09',100000,1,1),(15,7,'bbbbbbbbbbbbbbbbb','2020-09-16 02:20:43',200000,2,5),(16,1,'Meo meo meo','2020-09-16 02:33:35',100000,1,1),(17,7,'bbbbbbbbbbbbbbbbb','2020-09-16 11:07:20',700000,2,3),(18,7,'bbbbbbbbbbbbbbbbb','2020-09-16 11:22:53',200000,1,1),(19,7,'bbbbbbbbbbbbbbbbb','2020-09-16 12:07:56',200000,1,3),(20,7,'bbbbbbbbbbbbbbbbb','2020-09-16 12:12:52',100000,1,1),(21,7,'bbbbbbbbbbbbbbbbb','2020-09-16 12:15:33',300000,2,1),(22,7,'bbbbbbbbbbbbbbbbb','2020-09-16 12:20:33',100000,2,1),(23,7,'bbbbbbbbbbbbbbbbb','2020-09-17 09:08:28',500000,1,4),(24,7,'bbbbbbbbbbbbbbbbb','2020-09-17 09:12:16',300000,2,1),(25,2,'test','2020-09-17 09:18:30',400000,2,4),(26,1,'Meo meo meo ~~~~','2020-09-18 00:58:00',200000,1,1),(27,1,'Meo meo meo ~~~~','2020-09-18 01:00:18',200000,1,1),(28,1,'Meo meo meo ~~~~','2020-09-18 01:01:12',200000,1,1),(29,1,'Meo meo meo ~~~~','2020-09-18 01:03:50',200000,1,1),(30,1,'Meo meo meo ~~~~','2020-09-18 01:14:56',500000,1,1),(31,1,'Meo meo meo ~~~~','2020-09-18 01:16:56',200000,1,1),(32,1,'Meo meo meo ~~~~','2020-09-18 01:18:12',200000,1,5),(33,1,'Meo meo meo ~~~~','2020-09-18 01:19:10',200000,1,5),(34,1,'Meo meo meo ~~~~','2020-09-18 01:33:08',2000000,2,4),(35,2,'test','2020-09-18 15:36:22',300227,2,4),(36,2,'test','2020-09-18 15:46:25',500378,2,5),(37,1,'Meo meo meo ~~~~','2020-09-18 15:49:45',200000,1,3),(38,1,'Meo meo meo ~~~~','2020-09-18 15:50:46',200000,1,1),(39,1,'Meo meo meo ~~~~','2020-09-18 15:54:03',200000,1,4),(40,1,'Meo meo meo ~~~~','2020-09-18 15:54:27',200000,1,4),(41,2,'test','2020-09-18 15:56:28',500378,2,4);
/*!40000 ALTER TABLE `receipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt_type`
--

DROP TABLE IF EXISTS `receipt_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt_type`
--

LOCK TABLES `receipt_type` WRITE;
/*!40000 ALTER TABLE `receipt_type` DISABLE KEYS */;
INSERT INTO `receipt_type` VALUES (1,'Phiếu gửi tiền'),(2,'Phiếu rút tiền');
/*!40000 ALTER TABLE `receipt_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'admin'),(2,'user');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `username` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `user_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin',1,'admin','e10adc3949ba59abbe56e057f20f883e',1),(2,'nhanvien 1',1,'test1','25f9e794323b453885f5181f1b624d0b',1),(3,'nhanvien 2',1,'test2','e10adc3949ba59abbe56e057f20f883e',2),(4,'nhanvien 3',1,'test3','e10adc3949ba59abbe56e057f20f883e',1),(5,'nhanvien 4',1,'test4','25f9e794323b453885f5181f1b624d0b',1),(7,'nhanvien 2',0,'test1','e10adc3949ba59abbe56e057f20f883e',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-18 22:10:55
