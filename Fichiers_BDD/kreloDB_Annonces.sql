-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: localhost    Database: kreloDB
-- ------------------------------------------------------
-- Server version	8.0.32-0ubuntu0.22.10.2

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
-- Table structure for table `Annonces`
--

DROP TABLE IF EXISTS `Annonces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Annonces` (
  `id` int NOT NULL AUTO_INCREMENT,
  `utilisateur_id` int DEFAULT NULL,
  `titre` text,
  `description` text,
  `categorie` int NOT NULL,
  `type` int NOT NULL,
  `surface` decimal(10,0) NOT NULL,
  `prix` decimal(10,0) NOT NULL,
  `wilaya` int NOT NULL,
  `commune` varchar(30) NOT NULL,
  `adresse` varchar(30) NOT NULL,
  `photos` text NOT NULL,
  `isScraped` tinyint(1) DEFAULT NULL,
  `datePub` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `utilisateur_id` (`utilisateur_id`),
  CONSTRAINT `Annonces_ibfk_1` FOREIGN KEY (`utilisateur_id`) REFERENCES `Utilisateurs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Annonces`
--

LOCK TABLES `Annonces` WRITE;
/*!40000 ALTER TABLE `Annonces` DISABLE KEYS */;
INSERT INTO `Annonces` VALUES (1,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','1_0.png',0,'2023-02-04'),(2,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','test1.jpeg;test2.jpeg;test3.jpeg',0,'2023-02-04'),(3,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','test1.jpeg;test2.jpeg;test3.jpeg',0,'2023-02-04'),(4,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','test1.jpeg;test2.jpeg;test3.jpeg',0,'2023-02-04'),(5,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','test1.jpeg;test2.jpeg;test3.jpeg',0,'2023-02-04'),(6,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','test1.jpeg;test2.jpeg;test3.jpeg',0,'2023-02-04'),(7,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','test1.jpeg;test2.jpeg;test3.jpeg',0,'2023-02-04'),(8,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','test1.jpeg;test2.jpeg;test3.jpeg',0,'2023-02-04'),(9,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','test1.jpeg;test2.jpeg;test3.jpeg',0,'2023-02-04'),(10,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','test1.jpeg;test2.jpeg;test3.jpeg',0,'2023-02-04'),(11,1,'This is a titles','Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum .',1,1,80,700000,17,'This is a city','This is an adresse','test1.jpeg;test2.jpeg;test3.jpeg',0,'2023-02-04');
/*!40000 ALTER TABLE `Annonces` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-04 23:52:54
