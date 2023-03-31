DROP TABLE IF EXISTS `comment_report`;

CREATE TABLE `comment_report` (
	`id`	            INTEGER	        NOT NULL    AUTO_INCREMENT      PRIMARY KEY,
	`content`	        VARCHAR(500)	NOT NULL,
	`created_at`	    TIMESTAMP	    NOT NULL	DEFAULT CURRENT_TIMESTAMP,
	`updated_at`	    TIMESTAMP	    NOT NULL	DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`report_user_id`	VARCHAR(20)	    NOT NULL,
	`comment_id`	    INTEGER	        NOT NULL
);
