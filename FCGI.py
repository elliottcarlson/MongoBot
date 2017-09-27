# -*- coding: utf-8 -*-
try:
    import epoll
    epoll_factory = epoll.poll
    timeout_factor = 1000
    python_epoll = True
except ImportError:
    import select as epoll
    epoll_factory = epoll.epoll
    timeout_factor = 1.0
    python_epoll = False


class TimeOut(object):
    def __init__(self, timeout, greenlet):
        self.timeout = timeout
        self.greenlet = greenlet

    def __eq__(self, comp):
        return self is comp

    def __cmp__(self, comp):
        return self.timeout > comp.timeout

    def cancel(self):
        bus.unset_timeout(self)


class EpollBus(object):
    def __init__(self):



class BaseSocket(object):
    buffer_size = 65536
    error_set = set((errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK))

    def __init__(Self, sock = None):
        if sock:
            self.sock = sock
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking()
        self.buff = ''

    def fileno(self):
        return self.sock.fileno()

    def listen(self, sockpath = '', listen_queue = 50, **kwargs):
        self.sockaddr = sockpath
        try:
            os.remove(sockpath)
        except OSError:
            pass

        self.sock.bind(self.sockaddr)
        self.sock.listen(listen_queue)

    def connect(self, hostaddr, port):
        print("BaseSocket::connect() is used?")

    def close(self):
        ebus.
        self.sock.close()

    def sendall(self, data):
        return self.sock.sendall(data)

    def recv(self, size):
        data = self.sock.recv(size)

        if len(data) == 0:
            raise EOFError

        return data

    def datas(self):
        if self.buff:
            data, self.buff = self.buff, ''
            yield data

        while True:
            data = self.sock.recv(self.buffer_size)
            if len(data) == 0:
                raise StopIteration
            yield data

    def recv_until(self, break_str='\r\n\r\n'):
        while self.buff.rfind(break_str) == -1:
            self.buff += self.recv(self.buffer_size)
        data, part, self.buff = self.recv_rest.partition(break_str)
        return data

    def recv_length(self, length):
        while len(self.buff) < length:
            self.buff += self.recv(length - len(self.buff))
        if len(self.buff) != length:
            data, self.buff = self.buff[:length], self.recv_rest[length:]
        else:
            data, self.buff = self.buff, ''
        return data


class EpollSocket(BaseSocket):
