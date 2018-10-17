import time
import logging
import os
import signal
import threading
import light_logger.io as lio
import light_logger.net as lnet


def main():
    logging.debug("Light Logger v1.0")
    logging.info("Starting...")
    pid = os.getpid()
    logging.info("Processing PID : " + str(pid))
    config = lio.load_config()

    db = lio.DBOperating(config, pid)

    mque = lio.MQue(config, pid)

    th_msg = threading.Thread(target=lnet.msg_to_database_handle, args=(mque, db,))
    th_msg.start()

    th_recv = threading.Thread(target=lnet.log_recv_handle, args=(config, mque, db,))
    th_recv.start()

    # Monitor
    while True:
        pass
