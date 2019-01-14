/*
Navicat MySQL Data Transfer

Source Server         : 192.168.10.1
Source Server Version : 50712
Source Host           : 192.168.10.1:3306
Source Database       : firecloud

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2019-01-15 21:31:03
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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of webapp_level2menu
-- ----------------------------
INSERT INTO `webapp_level2menu` VALUES ('1', 'host', '主机列表', '1', '/host/list/', '1', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('2', 'hostUser', '主机帐号', '2', '/account/list/', '1', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('3', 'group', '主机组', '3', '/group/list/', '1', '0', '0', '0', '0');

INSERT INTO `webapp_level2menu` VALUES ('4', 'enterprise', '组织', '1', '/enterprise/list/', '2', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('5', 'project', '项目', '2', '/project/list/', '2', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('6', 'employee', '员工', '3', '/employee/list/', '2', '0', '0', '0', '0');

INSERT INTO `webapp_level2menu` VALUES ('7', 'optlog', '操作记录', '1', '/optlog/list/', '3', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('8', 'script', '脚本执行', '2', '/script/list/', '3', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('9', 'ansible', 'Ansible', '3', '/ansible/list/', '3', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('10', 'file', '文件分发', '4', '/file/list/', '3', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('11', 'publicFile', '公共文件', '5', '/publicFile/list', '3', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('12', 'taskTool', '快速工具', '6', '/fastTool/list/', '3', '0', '0', '0', '0');

INSERT INTO `webapp_level2menu` VALUES ('13', 'mesos', 'mesos集群', '1', '/mesos/list/', '4', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('14', 'kubernetes', 'kubernetes集群', '2', '/kubernetes/list/', '4', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('15', 'swarm', 'swarm集群', '3', '#', '4', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('16', 'network', '容器网络', '4', '/network/list/', '4', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('17', 'volume', '容器卷', '5', '/volume/list/', '4', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('18', 'repohost', '镜像仓库', '6', '/repohost/list/', '4', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('19', 'repoimage', '镜像列表', '7', '/repoimage/list/', '4', '0', '0', '0', '0');

INSERT INTO `webapp_level2menu` VALUES ('20', 'application', '应用列表', '1', '/app/list/', '5', '0', '0', '0', '0');

INSERT INTO `webapp_level2menu` VALUES ('21', 'appMonitor', '应用监控', '1', '/appMonitor/', '6', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('22', 'hostMonitor', '主机监控', '2', '/hostMonitor/', '6', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('23', 'eventList', '告警事件', '3', '/event/list/', '6', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('24', 'alertPolicy', '策略列表', '4', '/alertPolicy/list/', '6', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('25', 'receiveGroup', '接收组', '5', '/receiveGroup/list/', '6', '0', '0', '0', '0');

INSERT INTO `webapp_level2menu` VALUES ('26', 'logAnalyze', '日志分析', '1', '#', '7', '0', '0', '0', '0');

INSERT INTO `webapp_level2menu` VALUES ('27', 'web', 'web层', '1', '/web/', '8', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('28', 'logic', '逻辑层', '2', '/logic/', '8', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('29', 'storage', '存储层', '3', '/storage/', '8', '0', '0', '0', '0');

INSERT INTO `webapp_level2menu` VALUES ('30', 'UserMgt', '用户管理', '1', '/UserMgt/list/', '9', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('31', 'RoleMgt', '角色管理', '2', '/RoleMgt/list/', '9', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('32', 'globalSet', '全局设置', '3', '#', '9', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('33', 'crontab', 'Crontab调度', '1', '/crontab/list/', '10', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('34', 'interval', 'Interval调度', '2', '/interval/list/', '10', '0', '0', '0', '0');
INSERT INTO `webapp_level2menu` VALUES ('35', 'cron', '任务列表', '3', '/task/list/', '10', '0', '0', '0', '0');

