import socket
import select
import threading
import time
import logging
import os
import signal
import light_logger.io as lio
import light_logger.security as lsec


class TCPHandle(object):
    def __init__(self, conf, bq: lio.MQue):
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sk.bind(conf['listen_ip'], conf['listen_port'])
        self.sk.listen(conf['sessions'])
        self.sk.setblocking(False)

        self.epo = select.epoll()
        # Register to epoll event
        self.epo.register(self.sk.fileno(), select.EPOLLIN)

        self.sk = socket.socket()
        self.epo = select.epoll()
        self.connections = {}
        self.requests = {}
        self.responses = {}

        self.pkt_decrypt = lsec.SecService(conf['key'])
        self.bq = bq

    def start(self):
        try:
            while True:
                events = self.epo.poll(0.1)
                for fno, eve in events:
                    t = threading.Thread(target=self.thread_socket(), args=(self.sk.fileno(), self.epo, fno, eve,))
                    t.start()
        except:
            logging.error("Starting TCPHandle failed")
        finally:
            self.epo.unregister(self.sk.fileno())
            self.epo.close()
            self.sk.close()

    def thread_socket(self, file_no, event):
        if file_no == self.sk.fileno():
            connection, address = self.sk.accept()
            logging.info("Received request from " + str(address))
            connection.setblocking(True)
            self.epo.register(connection.fileno(), select.EPOLLIN)
            self.connections[connection.fileno()] = connection
            self.requests[connection.fileno()] = b''
            buffer = self.connections[connection.fileno()].recv()
            timestamp, project_name, level, msg = self.pkt_decrypt.run(buffer)
            if self.bq.status() >= 0:
                logging.info("Message queue available")
                self.bq.enqueue([timestamp, project_name, level, msg])
            else:
                logging.error("Message queue unavailable")
        elif event & select.EPOLLIN:
            self.requests[file_no] += self.connections[file_no].recv()
            if not self.requests[file_no]:
                self.connections[file_no].close()
                self.epo.modify(file_no, 0)
            else:
                self.msg_queue.put(bytes(self.requests[file_no]))
                self.epo.modify(file_no, select.EPOLLIN)
        elif event & select.EPOLLHUP:
            self.epo.unregister(file_no)
            self.connections[file_no].close()
            # del connections[file_no]
            self.clean_dir(file_no)


# def log_recv_handle():

def msg_to_database_handle(mq: lio.MQue, db: lio.DBOperating):
    while True:
        signal.sigwait(signal.SIGUSR1)
        while True:
            if mq.status() > 0:
                pass
            else:
                break
