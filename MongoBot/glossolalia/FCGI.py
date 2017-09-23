# -*- coding: utf-8 -*-
import logging
import os
import select
import socket

from hexdump import hexdump

logger = logging.getLogger(__name__)


FCGI_MAX_REQS = 1
FCGI_MAX_CONNS = 1
FCGI_VERSION = 1
FCGI_MPXS_CONNS = 0

FCGI_BEGIN_REQUEST = 1
FCGI_ABORT_REQUEST = 2
FCGI_END_REQUEST = 3
FCGI_PARAMS = 4
FCGI_STDIN = 5
FCGI_STDOUT = 6
FCGI_STDERR = 7
FCGI_DATA = 8
FCGI_GET_VALUES = 9
FCGI_GET_VALUES_RESULT = 10
FCGI_UNKNOWN_TYPE = 11
FCGI_MAXTYPE = FCGI_UNKNOWN_TYPE


class FCGI_Socket(object):

    buffer_size = 65536

    def __init__(self, sock=None):
        self.sock = sock or socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_buffer = ''

    def listen(self, sockpath='', queue=5):
        self.sockaddr = sockpath
        if os.path.exists(sockpath):
            os.remove(sockpath)
        self.sock.bind(sockpath)
        os.chmod(sockpath, 0o777)
        self.sock.listen(5)

    def close(self):
        self.sock.close()

    def recv(self, size):
        data = self.sock.recv(size)
        if len(data) == 0:
            raise EOFError

        return data

    def recv_until(self, boundary='\r\n\r\n'):
        while self.recv_buffer.rfind(boundary) == -1:
            self.recv_buffer += self.recv(self.buffer_size)
        data, part, self.recv_buffer = self.recv_buffer.partition(boundary)

        return data

    def recv_length(self, length):
        while len(self.recv_buffer) < length:
            self.recv_buffer += self.recv(length - len(self.recv_buffer))

        if len(self.recv_buffer) != length:
            data = self.recv_bugger[:length]
            self.recv_buffer = self.recv_buffer[length:]
        else:
            data, self.recv_buffer = self.recv_buffer, ''

        return data


class FCGI(object):

    server = False
    sockets = []
    connected = True

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

        for sock in readable:
            if sock in readable:
                if sock is self.server:
                    conn, addr = self.server.accept()
                    FCGI.sockets.append(conn)
                    logger.info('FCGI Connection from %s', addr)
                else:
                    # timeout = time() + 15  # 15 second timeout

                    data = sock.recv(8)
                    print(hexdump(data))
                    header = FCGI_Header(data)
                    content = ''

                    while len(content) < header.contentLength:
                        data = sock.recv(10)  # header.contentLength - len(content))
                        content = content + data

                    if header.paddingLength != 0:
                        padding = sock.recv(header.paddingLength)

                    FCGI.sockets.remove(sock)
                    """
                    while True:
                        try:
                            chunk = s.recv(1024)
                        except:
                            FCGI.sockets.remove(s)
                            break

                        if not chunk:
                            FCGI.sockets.remove(s)
                            break

                        if time() > timeout:
                            logger.info('Breaking out of FCGI process loop due to timeout')
                            FCGI.sockets.remove(s)
                            break

                        data.append(chunk)
                    """
                    print(hexdump(content))
                    print(hexdump(padding))
                    # FCGI_Record(''.join(data))


class FCGI_Header(object):
    def __init__(self, data):
        header = map(ord, data)
        self.version = header[0]
        self.type = header[1]
        self.requestIdB1 = header[2]
        self.requestIdB0 = header[3]
        self.requestId = (header[2] << 8) + header[3]
        self.contentLengthB1 = header[4]
        self.contentLengthB0 = header[5]
        self.contentLength = (header[4] << 8) + header[5]
        self.paddingLength = header[6]
        self.reserved = None

        print('Version:', self.version)
        print('Type:', self.type)
        print('RequestId:', self.requestId)
        print('Content Length:', self.contentLength)
        print('Padding Length:', self.paddingLength)


class FCGI_Record(object):
    """
    http://www.mit.edu/~yandros/doc/specs/fcgi-spec.html 3.3 Records

    All data that flows over the transport connection is carried in FastCGI
    records. FastCGI records accomplish two things. First, records multiplex
    the transport connection between several independent FastCGI requests. This
    multiplexing supports applications that are able to process concurrent
    requests using event-driven or multi-threaded programming techniques.
    Second, records provide several independent data streams in each direction
    within a single request. This way, for instance, both stdout and stderr
    data can pass over a single transport connection from the application to
    the Web server, rather than requiring separate connections.
    """
    def __init__(self, record):
        self.version = FCGI_VERSION
        self.type = FCGI_UNKNOWN_TYPE
        self.requestId = 0
        self.contentLength = 0
        self.paddingLength = 0
        self.contentData = ''
        self.paddingData = ''

        self.parse(record)

    def parse(self, record):
        print(hexdump(record[0:8]))
        header = map(ord, record[0:8])

        self.version = header[0]
        self.type = header[1]
        self.requestId = (header[2] << 8) + header[3]
        self.contentLength = (header[4] << 8) + header[5]
        self.paddingLength = header[6]

        print('Version:', self.version)
        print('Type:', self.type)
        print('Request ID:', self.requestId)
        print('Length of record: ', len(record))
        print('Content Length: ', self.contentLength)
        print('Padding Length: ', self.paddingLength)
#        while len(self.contentData) < self.contentLength:
