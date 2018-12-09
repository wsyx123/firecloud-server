/*
Navicat MySQL Data Transfer

Source Server         : 192.168.10.1
Source Server Version : 50712
Source Host           : 192.168.10.1:3306
Source Database       : firecloud

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2018-10-30 23:42:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for webapp_level2menu
-- ----------------------------
DROP TABLE IF EXISTS `webapp_level2menu`;
CREATE TABLE `webapp_level2menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `description` varchar(32) NOT NULL,
  `priority` int(11) NOT NULL,
  `url` varchar(64) NOT NULL,
  `parent_name_id` int(11) NOT NULL,
  `create` tinyint(1) NOT NULL,
  `delete` tinyint(1) NOT NULL,
  `update` tinyint(1) NOT NULL,
  `view` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `webapp_level2menu_parent_name_id_c1b94b22_fk_webapp_le` (`parent_name_id`),
  CONSTRAINT `webapp_level2menu_parent_name_id_c1b94b22_fk_webapp_le` FOREIGN KEY (`parent_name_id`) REFERENCES `webapp_level1menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of webapp_level2menu
-- ----------------------------
INSERT INTO `webapp_level2menu` VALUES ('1', 'host', '主机', '1', '/host/list/', '2', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('2', 'group', '主机组', '2', '/hostGroup/list/', '2', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('3', 'enterprise', '组织', '1', '/enterprise/list/', '3', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('4', 'project', '项目', '2', '/project/list/', '3', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('5', 'employee', '员工', '3', '/employee/list/', '3', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('6', 'optlog', '操作记录', '1', '/optlog/', '4', '0', '0', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('7', 'command', '命令执行', '2', '/command/', '4', '1', '0', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('8', 'file', '文件分发', '3', '/file/', '4', '1', '0', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('9', 'cron', '定时任务', '4', '/cron/list/', '4', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('10', 'template', '模版管理', '5', '/template/list/', '4', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('11', 'mesos', 'mesos', '1', '/mesos/list/', '5', '1', '1', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('12', 'kubernetes', 'kubernetes', '2', '/kubernetes/list/', '5', '1', '1', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('13', 'swarm', 'swarm', '3', '#', '5', '1', '1', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('14', 'network', 'network', '4', '/network/list/', '5', '1', '1', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('15', 'volume', 'volume', '5', '/volume/list/', '5', '1', '1', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('16', 'repohost', 'repository', '6', '/repohost/list/', '5', '1', '1', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('17', 'repoimage', 'images', '7', '/repoimage/list/', '5', '0', '0', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('18', 'application', '应用列表', '1', '/app/list/', '6', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('19', 'appMonitor', '应用监控', '1', '/appMonitor/', '7', '0', '0', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('20', 'hostMonitor', '主机监控', '2', '/hostMonitor/', '7', '0', '0', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('21', 'eventList', '告警事件', '3', '/event/list/', '7', '0', '0', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('22', 'alertPolicy', '策略列表', '4', '/alertPolicy/list/', '7', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('23', 'receiveGroup', '接收组', '5', '/receiveGroup/list/', '7', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('24', 'logAnalyze', '日志分析', '1', '#', '8', '0', '0', '0', '1');
INSERT INTO `webapp_level2menu` VALUES ('25', 'web', 'web层', '1', '/web/', '9', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('26', 'logic', '逻辑层', '2', '/logic/', '9', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('27', 'storage', '存储层', '3', '/storage/', '9', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('28', 'UserMgt', '用户管理', '1', '/UserMgt/list/', '10', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('29', 'RoleMgt', '角色管理', '2', '/RoleMgt/list/', '10', '1', '1', '1', '1');
INSERT INTO `webapp_level2menu` VALUES ('30', 'dashboard', '-', '1', '#', '1', '0', '0', '0', '1');
