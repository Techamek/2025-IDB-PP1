CREATE TABLE IF NOT EXISTS `accounts` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `role` VARCHAR(50) NOT NULL,
    `user_ref` VARCHAR(50) NOT NULL,   -- NEW column referencing student/instructor ID
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
