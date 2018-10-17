-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2018-10-15 12:58:02
-- 服务器版本： 10.2.14-MariaDB-log
-- PHP 版本： 7.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `light-logger`
--
CREATE DATABASE IF NOT EXISTS `light-logger` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `light-logger`;

-- --------------------------------------------------------

--
-- 表的结构 `device_log`
--

CREATE TABLE `device_log` (
  `id` bigint(20) NOT NULL,
  `time_t` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `dev_name` varchar(32) NOT NULL,
  `level` tinyint(4) NOT NULL,
  `message` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `msg_log`
--

CREATE TABLE `msg_log` (
  `id` bigint(20) NOT NULL,
  `insert_time` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `client_time` datetime NOT NULL,
  `name` varchar(32) NOT NULL,
  `level` tinyint(4) NOT NULL,
  `message` varchar(512) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转储表的索引
--

--
-- 表的索引 `device_log`
--
ALTER TABLE `device_log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `msg_log`
--
ALTER TABLE `msg_log`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `device_log`
--
ALTER TABLE `device_log`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `msg_log`
--
ALTER TABLE `msg_log`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
