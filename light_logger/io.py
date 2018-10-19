import os
import logging
import json
import pymysql
import signal
import Crypto.Hash.MD5 as md5
import Crypto.Cipher.AES as aes
from multiprocessing import Process, Queue


def load_config():
    if os.path.exists('config.json'):
        logging.info("Configuration file existed")
        try:
            f = open('config.json', 'r')
            config = json.load(f)
            return config
        except json.JSONDecodeError as e:
            logging.error("Failed to load configuration : " + str(e))
            os._exit(-1)
    else:
        config = {
            'listen_ip': '0.0.0.0',
            'listen_port': 5641,
            'sessions': 5,
            'queue_depth': 65535,
            'db_ip': '127.0.0.1',
            'db_port': 3306,
            'db_user': 'root',
            'db_password': '',
            'db_name': 'light-logger',
            "key": ""
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)
        print("Succeed to create configuration file and you can modify it now")
        os._exit(0)


class DBOperating(object):
    def __init__(self, conf):
        try:
            self.db = pymysql.connect(host=conf['db_ip'], port=conf['db_port'], user=conf['db_user'], passwd=conf['db_password'], charset='utf8mb4', db=conf['db_name'])
        except pymysql.Error as e:
            logging.error("Failed to connect database : " + str(e))

    def db_insert(self, time, name, level, msg):
        try:
            with self.db.cursor() as cursor:
                sql = "INSERT INTO msg_log(client_time, name, level, message) VALUES (\"%s\", \"%s\", %s, \"%s\");" % time, name, level, msg
                cursor.execute(sql)
                self.db.commit()
        except self.db.Error as e:
            self.db.rollback()
            logging.warning("Failed to insert to database" + str(e))
        finally:
            logging.info("Succeed to insert a log to database")

    def db_close(self):
        self.db.close()
        logging.info("PyMySQL connection closed")


class MQue(object):
    def __init__(self, conf, pid):
        self.queue = Queue(int(conf['queue_depth']))
        self.pid = pid
        logging.info("Succeed to create MsgQueue, depth " + str(conf['queue_depth']))

    def enqueue(self, data_list):
        self.queue.put(data_list)
        os.kill(self.pid, signal.SIGUSR1)

    def status(self):
        if self.queue.empty():
            return 0
        if self.queue.full():
            return -1
        return self.queue.qsize()

    def deque(self):
        try:
            return self.queue.get()
        except:
            return -1


class SignalHandle(object):
    def __init__(self, mq: MQue, db: DBOperating):
        self.mq = mq
        self.db = db

    def signal_interrupt(self):
        while True:
            if self.mq.status() > 0:
                data_list = self.mq.deque()
                timestamp = data_list[0]
                project_name = data_list[1]
                level = data_list[2]
                msg = data_list[3]
                self.db.db_insert(timestamp, project_name, level, msg)
            else:
                break
