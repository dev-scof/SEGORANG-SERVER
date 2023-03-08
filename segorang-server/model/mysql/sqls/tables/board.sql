DROP TABLE IF EXISTS board;
CREATE TABLE IF NOT EXISTS board
(
    id              INTEGER         NOT NULL    AUTO_INCREMENT      PRIMARY KEY,
    user_id         VARCHAR(20)     NOT NULL,
    nickname        VARCHAR(20)     NOT NULL,
    category        VARCHAR(20)     NOT NULL,
    title           VARCHAR(20)     NOT NULL,
    content         VARCHAR(1000)   NOT NULL,
    created_at      TIMESTAMP       NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP       NOT NULL    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);