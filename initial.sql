CREATE TABLE IF NOT EXISTS `ip_list` (
  `ip` varchar(30) NOT NULL,
  `hits` int(11) NOT NULL DEFAULT '1',
  `status` text,
  `last_updated` timestamp NULL DEFAULT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `ip` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TRIGGER IF EXISTS `modified_timestamp`;
DELIMITER //
CREATE TRIGGER `modified_timestamp` BEFORE UPDATE ON `ip_list`
 FOR EACH ROW SET new.last_updated = CURRENT_TIMESTAMP
//
DELIMITER ;
DROP TRIGGER IF EXISTS `updated&status`;
DELIMITER //
CREATE TRIGGER `updated&status` BEFORE INSERT ON `ip_list`
 FOR EACH ROW set new.last_updated = new.created, new.status = 'active'
//
DELIMITER ;

