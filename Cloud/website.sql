-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 28, 2022 at 05:24 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `website`
--

-- --------------------------------------------------------

--
-- Table structure for table `db_cache`
--

CREATE TABLE `db_cache` (
  `Algorithm_Chosen` int(1) NOT NULL DEFAULT 0,
  `Mem_size` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `db_cache`
--

INSERT INTO `db_cache` (`Algorithm_Chosen`, `Mem_size`) VALUES
(0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `db_cache_statistic`
--

CREATE TABLE `db_cache_statistic` (
  `No_of_items` int(100) NOT NULL,
  `No_of_requests` int(100) NOT NULL,
  `TotalSize_of_items` int(100) NOT NULL,
  `Miss_rate` int(100) NOT NULL,
  `Hit_rate` int(100) NOT NULL,
  `TimeStamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `Image_key` text NOT NULL,
  `image_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `images`
--

INSERT INTO `images` (`Image_key`, `image_path`) VALUES
('12', 'map.png'),
('1', 'abod.jpg'),
('2', 'bruh.gif'),
('3', 'images1.jpg'),
('4', 'abod.jpg'),
('7', 'stars.jpg'),
('test1', 'meme.PNG'),
('6', '17cc6cc86047f75ebcee6cd5fa097b42.jpg'),
('5', '1b94ca3b3a96903f92659ff09d612f0a.jpg'),
('10', 'image-20161123-19696-4zwj9p-3412441021.jpg'),
('15', '0500da35104fc560bb25c01906b84708.jpg'),
('13', 'f3ae364fa1fb467afc9f37a10e94bebb.png'),
('66', 'boss.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `policy`
--

CREATE TABLE `policy` (
  `id` int(1) NOT NULL,
  `policy_name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `policy`
--

INSERT INTO `policy` (`id`, `policy_name`) VALUES
(0, 'Random Replacement'),
(1, 'Least Recently Used');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `db_cache`
--
ALTER TABLE `db_cache`
  ADD UNIQUE KEY `Algorithm_Chosen` (`Algorithm_Chosen`);

--
-- Indexes for table `db_cache_statistic`
--
ALTER TABLE `db_cache_statistic`
  ADD UNIQUE KEY `TimeStamp` (`TimeStamp`);

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD UNIQUE KEY `image_key` (`Image_key`) USING HASH;

--
-- Indexes for table `policy`
--
ALTER TABLE `policy`
  ADD UNIQUE KEY `id` (`id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `db_cache`
--
ALTER TABLE `db_cache`
  ADD CONSTRAINT `db_cache_ibfk_1` FOREIGN KEY (`Algorithm_Chosen`) REFERENCES `policy` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
