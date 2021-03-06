CREATE TABLE msg_log(
    id BIGINT NOT NULL AUTO_INCREMENT,
    insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	client_time DATETIME NOT NULL,
    name VARCHAR(32) NOT NULL,
    level TINYINT NOT NULL,
    message VARCHAR(512) NOT NULL,
    PRIMARY KEY ( id )
);

CREATE TABLE device_log(
    id BIGINT NOT NULL AUTO_INCREMENT,
    time_t TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dev_name VARCHAR(32) NOT NULL,
    level TINYINT NOT NULL,
    message VARCHAR(128) NOT NULL,
    PRIMARY KEY ( id )
);