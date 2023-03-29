SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS post;
SET FOREIGN_KEY_CHECKS=1;
CREATE TABLE IF NOT EXISTS post
(
    id              INTEGER         NOT NULL    AUTO_INCREMENT      PRIMARY KEY,
    user_id         VARCHAR(20)     NOT NULL,
    board_id        INTEGER         NOT NULL,
    title           VARCHAR(20)     NOT NULL,
    content         VARCHAR(2000)   NOT NULL,
    images          VARCHAR(2000)   NULL        DEFAULT NULL,
    like_cnt        INTEGER         NOT NULL    DEFAULT 0,
    view_cnt        INTEGER         NOT NULL    DEFAULT 0,
    category        VARCHAR(15)     NULL        DEFAULT NULL,
    created_at      TIMESTAMP       NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP       NOT NULL    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (board_id) REFERENCES board(id) ON UPDATE CASCADE ON DELETE CASCADE
);