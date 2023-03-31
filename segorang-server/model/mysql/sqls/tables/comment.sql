DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
	`id`	                INTEGER	        NOT NULL	AUTO_INCREMENT  PRIMARY KEY,
	`content`	            VARCHAR(300)	NOT NULL,
	`created_at`	        TIMESTAMP	    NOT NULL	DEFAULT CURRENT_TIMESTAMP,
	`updated_at`	        TIMESTAMP	    NOT NULL	DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`parrent_comment_id`	INTEGER     	NULL	    DEFAULT NULL,
	`user_id`	            VARCHAR(20)	    NOT NULL,
	`post_id`	            INTEGER	NOT     NULL
);