DROP TABLE IF EXISTS user;
CREATE TABLE `user` (
	`id`	        VARCHAR(20) NOT NULL    PRIMARY KEY,
	`sj_id`	        VARCHAR(20)	NOT NULL	UNIQUE KEY,
	`nickname`	    VARCHAR(15)	NOT NULL,
	`user_name`	    VARCHAR(20)	NOT NULL,
	`pw`	        VARCHAR(20)	NOT NULL,
	`major`	        VARCHAR(20)	NOT NULL,
	`is_deleted`	BOOLEAN		NOT NULL	DEFAULT false,
	`created_at`	TIMESTAMP	NOT NULL	DEFAULT CURRENT_TIMESTAMP,
	`updated_at`	TIMESTAMP	NOT NULL	DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);