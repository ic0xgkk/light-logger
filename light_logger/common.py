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

    db = lio.DBOperating(config)

    mque = lio.MQue(config, pid)

    sigh = lio.SignalHandle(mque, db)
    signal.signal(signal.SIGUSR1, sigh.signal_interrupt)

    th_recv = threading.Thread(target=lnet.log_recv_handle, args=(config, mque,))
    th_recv.start()

    # Monitor
    while True:
        pass
