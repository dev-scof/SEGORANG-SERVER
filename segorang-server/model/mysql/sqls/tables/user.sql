SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS user;
SET FOREIGN_KEY_CHECKS=1;
CREATE TABLE IF NOT EXISTS user
(
    id          VARCHAR(20)     NOT NULL    PRIMARY KEY,
    sj_id       VARCHAR(20)     NOT NULL,
    nickname    VARCHAR(20)     NOT NULL    UNIQUE KEY,
    user_name   VARCHAR(20)     NOT NULL,
    pw          VARCHAR(16)     NOT NULL,
    major       VARCHAR(20)     NOT NULL,
    is_admin    BOOL            NOT NULL    DEFAULT 0,
    sejong_auth BOOL            NOT NULL    DEFAULT 0,
    created_at  TIMESTAMP       NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP       NOT NULL    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);