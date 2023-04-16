ALTER TABLE `comment` 
    ADD CONSTRAINT `FK_comment_TO_comment_1` FOREIGN KEY (`parrent_comment_id`)
    REFERENCES `comment` (`id`);

ALTER TABLE `comment`
    ADD CONSTRAINT `FK_user_TO_comment_1` FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`);

ALTER TABLE `comment`
    ADD CONSTRAINT `FK_post_TO_comment_1` FOREIGN KEY (`post_id`)
    REFERENCES `post` (`id`);

ALTER TABLE `post`
    ADD CONSTRAINT `FK_user_TO_post_1` FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`);

ALTER TABLE `post`
    ADD CONSTRAINT `FK_board_TO_post_1` FOREIGN KEY (`board_id`)
    REFERENCES `board` (`id`);

ALTER TABLE `post_like`
    ADD CONSTRAINT `FK_user_TO_post_like_1` FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`);

ALTER TABLE `post_like`
    ADD CONSTRAINT `FK_post_TO_post_like_1` FOREIGN KEY (`post_id`)
    REFERENCES `post` (`id`);

ALTER TABLE `user_image`
    ADD CONSTRAINT `FK_user_TO_user_image_1` FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`);

ALTER TABLE `comment_like`
    ADD CONSTRAINT `FK_user_TO_comment_like_1` FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`);

ALTER TABLE `comment_like`
    ADD CONSTRAINT `FK_comment_TO_comment_like_1` FOREIGN KEY (`comment_id`)
    REFERENCES `comment` (`id`);

ALTER TABLE `post_image`
    ADD CONSTRAINT `FK_post_TO_post_image_1` FOREIGN KEY (`post_id`)
    REFERENCES `post` (`id`)
    ON DELETE CASCADE;

ALTER TABLE `bookmark`
    ADD CONSTRAINT `FK_user_TO_bookmark_1` FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`);

ALTER TABLE `bookmark`
    ADD CONSTRAINT `FK_post_TO_bookmark_1` FOREIGN KEY (`post_id`)
    REFERENCES `post` (`id`);

ALTER TABLE `post_report`
    ADD CONSTRAINT `FK_user_TO_post_report_1` FOREIGN KEY (`report_user_id`)
    REFERENCES `user` (`id`);

ALTER TABLE `post_report`
    ADD CONSTRAINT `FK_post_TO_post_report_1` FOREIGN KEY (`post_id`)
    REFERENCES `post` (`id`);

ALTER TABLE `comment_report`
    ADD CONSTRAINT `FK_user_TO_comment_report_1` FOREIGN KEY (`report_user_id`)
    REFERENCES `user` (`id`);

ALTER TABLE `comment_report`
    ADD CONSTRAINT `FK_comment_TO_comment_report_1` FOREIGN KEY (`comment_id`)
    REFERENCES `comment` (`id`);

ALTER TABLE `post_like` ADD UNIQUE KEY (`user_id`, `post_id`);
ALTER TABLE `comment_like` ADD UNIQUE KEY (`user_id`, `comment_id`);