/*
Navicat MySQL Data Transfer

Source Server         : 192.168.10.1
Source Server Version : 50712
Source Host           : 192.168.10.1:3306
Source Database       : firecloud

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2019-01-15 21:30:49
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for webapp_level1menu
-- ----------------------------
DROP TABLE IF EXISTS `webapp_level1menu`;
CREATE TABLE `webapp_level1menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `description` varchar(32) NOT NULL,
  `priority` int(11) NOT NULL,
  `url` varchar(64) NOT NULL,
  `menu_icon` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of webapp_level1menu
-- ----------------------------
INSERT INTO `webapp_level1menu` VALUES ('1', 'asset', '资产管理', '2', '#', 'fa-desktop');
INSERT INTO `webapp_level1menu` VALUES ('2', 'enterprise', '组织管理', '3', '#', 'fa-align-justify');
INSERT INTO `webapp_level1menu` VALUES ('3', 'task', '作业中心', '4', '#', 'fa-coffee');
INSERT INTO `webapp_level1menu` VALUES ('4', 'paas', 'PAAS中心', '5', '#', 'fa-cloud');
INSERT INTO `webapp_level1menu` VALUES ('5', 'application', '应用管理', '6', '#', 'fa-cube');
INSERT INTO `webapp_level1menu` VALUES ('6', 'monitor', '监控告警', '7', '#', 'fa-bar-chart');
INSERT INTO `webapp_level1menu` VALUES ('7', 'log', '日志中心', '8', '#', 'fa-file-o');
INSERT INTO `webapp_level1menu` VALUES ('8', 'store', '应用商店', '9', '#', 'fa-shopping-cart');
INSERT INTO `webapp_level1menu` VALUES ('9', 'sysmgt', '系统管理', '10', '#', 'fa-cog');
INSERT INTO `webapp_level1menu` VALUES ('10', 'celery_task', '任务调度', '1', '#', 'fa-cogs');
