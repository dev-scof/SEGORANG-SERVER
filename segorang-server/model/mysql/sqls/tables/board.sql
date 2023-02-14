CREATE TABLE IF NOT EXISTS board
(
    id              VARCHAR(20)     NOT NULL    PRIMARY KEY,
    user_id         VARCHAR(20)     NOT NULL,
    user_nickname   VARCHAR(20)     NOT NULL    UNIQUE KEY,
    category        VARCHAR(20)     NOT NULL,
    title           VARCHAR(20)     NOT NULL,
    content         VARCHAR(1000)   NOT NULL,
    created_at      TIMESTAMP       NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP       NOT NULL    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);