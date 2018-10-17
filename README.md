# Light Logger

An open source log collecting system.

## Usage

```bash
python server.py
```

## Installation Guide

### Install dependence

This system need to run with some pip modules,and you can use nether commands to
 install it.
 
 ```bash
python -m pip install pymysql
python -m pip install pycrypto
```

### Initiate database

You can execute nether sql script to initiate database in mysql
```sql
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
```
or you also can flow nether shell script to import **resource/light-logger.sql**
```bash
cd resource
mysql -u root -p
create database light-logger;
use light-logger;
source light-logger.sql;
```

### Configuration File

```json
{
    "listen_ip": "0.0.0.0",
    "listen_port": 5641,
    "sessions": 5,
    "queue_depth": 65535,
    "db_ip": "127.0.0.1",
    "db_port": 3306,
    "db_user": "root",
    "db_password": "",
    "db_name": "light-logger",
    "key": ""
}
```

In this configuration:

1. **listen_ip** : 
2. **listen_port**
3. **sessions** : Max allowed sessions of TCP
4. **queue_depth** : Size of message queue, and it will used to be store the data which is received by TCP handle
5. **db_ip**
5. **db_port**
5. **db_user**
5. **db_password**
5. **db_name**