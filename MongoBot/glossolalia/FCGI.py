# -*- coding: utf-8 -*-
import logging
import os
import select
import socket

from hexdump import hexdump
from time import time

logger = logging.getLogger(__name__)


class FCGI(object):

    server = False
    sockets = []

    def __init__(self, settings):

        self.provider = settings.__name__
        self.sockfile = settings.get('sockfile', '/tmp/MongoBot.sock')

        if os.path.exists(self.sockfile):
            os.remove(self.sockfile)

    def connect(self):

        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setblocking(0)
        self.server.bind(self.sockfile)
        os.chmod(self.sockfile, 0o777)
        self.server.listen(5)

        FCGI.sockets.append(self.server)

        logger.info('FCGI Server listening at %s', self.sockfile)

    def process(self):
        readable, writable, errored = select.select(self.sockets, [], [], 0)

        for s in readable:
            if s in readable:
                if s is self.server:
                    conn, addr = self.server.accept()
                    FCGI.sockets.append(conn)
                    logger.info('FCGI Connection from %s', addr)
                else:
                    timeout = time() + 15  # 15 second timeout

                    while True:
                        print('!')
                        data = s.recv(1024)

                        if not data:
                            FCGI.sockets.remove(s)
                            break
                        else:
                            print(hexdump(data))
                            FCGI.sockets.remove(s)
                            break

                        if time() > timeout:
                            logger.info('Breaking out of FCGI process loop due to timeout')
                            FCGI.sockets.remove(s)
                            break
