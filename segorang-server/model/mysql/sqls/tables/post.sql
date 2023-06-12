DROP TABLE IF EXISTS `post`;

CREATE TABLE `post` (
	`id`	        INTEGER	        NOT NULL    AUTO_INCREMENT      PRIMARY KEY,
	`title`	        VARCHAR(100)    NOT NULL,
	`content`	    VARCHAR(2000)	NOT NULL,
	`view_cnt`	    INTEGER	        NOT NULL	DEFAULT 0,
	`category`	    VARCHAR(10)	    NULL	    DEFAULT NULL,
	`created_at`	TIMESTAMP	    NOT NULL	DEFAULT CURRENT_TIMESTAMP,
	`updated_at`	TIMESTAMP	    NOT NULL	DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`user_id`	    VARCHAR(20)	    NOT NULL,
	`board_id`	    INTEGER	        NOT NULL,
	`is_deleted`	BOOLEAN			NOT NULL	DEFAULT false
);