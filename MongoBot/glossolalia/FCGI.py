#!/usr/bin/env python
import gevent.monkey

gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
gevent.monkey.patch_dns()

import errno
import logging
import signal
import sys

# from flup.server.fcgi import WSGIServer
from flup.server.fcgi_base import BaseFCGIServer, FCGI_RESPONDER
from flup.server.threadpool import ThreadPool
# from flup.server.threadedserver import ThreadedServer, setCloseOnExec
from flup.server.threadedserver import setCloseOnExec
from gevent import socket
from gevent.select import select as gselect
from MongoBot.cortex import Cortex
from MongoBot.dendrite import dendrate, Dendrite
from pyparsing import Suppress, Literal, Optional, Word, Group, \
    OneOrMore, alphanums

logger = logging.getLogger(__name__)


class FCGIRouter(object):
    def __init__(self):
        """
        /api/<command>[/<params>...]
        """
        slash = Suppress(Literal('/'))
        prefix = slash + Suppress(Literal('api'))
        component = slash + Word(alphanums + '_.')
        command = Group(prefix + component)('command')
        parameters = Optional(OneOrMore(component))('params')

        self.EBNF = command + parameters

    def parse(self, line):
        parsed = self.EBNF.parseString(line)
        return parsed.asDict()


class RequestHandler(object):
    def __call__(self, env, response):
        logger.info(env.get('PATH_INFO'))

        try:
            router = FCGIRouter()
            route = router.parse(env.get('PATH_INFO'))
        except:
            response('404 Not Found', [('Content-Type', 'text/plain')])
            return ['404 Not Found.']

        command = Cortex.cortical_map.get(route.get('command')[0])

        if not command:
            response('501 Not Implemented', [('Content-Type', 'text/plain')])
            return ['501 Method Not Implemented.']

        request = {
            'target': 'web',
            'service': 'FCGI',
            'stdin': ' '.join(route.get('params', [])),
            'module': __name__,
            'source': {},
            'provider': 'fcgi',
            'data': env.get('PATH_INFO')
        }

        env = Dendrite(request, route.get('params', []), Cortex.thalamus)
        instance = dendrate(env, command[0])()
        mod = getattr(instance, command[1])
        res = mod()

        print(str(res))

        response('200 OK', [('Content-Type', 'text/plain')])
        return [str(res)]


class MyThreadedServer(object):
    def __init__(self, jobClass=None, jobArgs=(), **kw):
        self._jobClass = jobClass
        self._jobArgs = jobArgs

        self._threadPool = ThreadPool(**kw)

    def run(self, sock, timeout=1.0):
        self._keepGoing = True
        self._hupReceived = False

        if not sys.platform.startswith('win'):
            self._installSignalHandlers()

        setCloseOnExec(sock)

        while self._keepGoing:
            try:
                r, w, e = gselect([sock], [], [], timeout)
            except gselect.error as e:
                if e.args[0] == errno.EINTR:
                    continue

            if r:
                try:
                    clientSock, addr = sock.accept()
                except socket.error as e:
                    if e.args[0] in (errno.EINTR, errno.EAGAIN):
                        continue
                    raise

                setCloseOnExec(clientSock)

                conn = self._jobClass(clientSock, addr, *self._jobArgs)
                if not self._threadPool.addJob(conn, allowQueuing=False):
                    clientSock.close()

            self._mainloopPeriodic()

        if not sys.platform.startswith('win'):
            self._restoreSignalHandlers()

        return self._hupReceived

    def shutdown(self):
        # self._threadPool.shutdown()
        pass

    def _mainloopPeriodic(self):
        pass

    def _exit(self, reload=False):
        if self._keepGoing:
            self._keepGoing = False
            self._hupReceived = reload

    def _hupHandler(self, signum, frame):
        self._hupReceived = True
        self._keepGoing = False

    def _intHandler(self, signum, frame):
        self._keepGoing = False

    def _installSignalHandlers(self):
        supportedSignals = [signal.SIGINT, signal.SIGTERM]
        if hasattr(signal, 'SIGHUP'):
            supportedSignals.append(signal.SIGHUP)

        self._oldSIGs = [(x, signal.getsignal(x)) for x in supportedSignals]

        for sig in supportedSignals:
            if hasattr(signal, 'SIGHUP') and sig == signal.SIGHUP:
                signal.signal(sig, self._hupHandler)
            else:
                signal.signal(sig, self._intHandler)

    def _restoreSignalHandlers(self):
        for signum, handler in self._oldSIGs:
            signal.signal(signum, handler)


class FCGI(BaseFCGIServer, MyThreadedServer):
    sockfile = '/tmp/auth.unorignl.sock'

    def __init__(self, environ=None, multithreaded=True, multiprocess=False,
                 bindAddress=None, umask=0, multiplexed=False, debug=False,
                 roles=(FCGI_RESPONDER,), forceCGI=False, **kwargs):

        opts = {
            'environ': environ,
            'multithreaded': multithreaded,
            'multiprocess': multiprocess,
            'bindAddress': self.sockfile,
            'umask': umask,
            'multiplexed': multiplexed,
            'debug': True,
            'roles': roles,
            'forceCGI': False,
        }

        if kwargs:
            opts.update(kwargs)

        BaseFCGIServer.__init__(self, RequestHandler(), **opts)

        for key in ('jobClass', 'jobArgs'):
            if key in kwargs:
                del kwargs[key]

        MyThreadedServer.__init__(self, jobClass=self._connectionClass,
                                  jobArgs=(self,), **kwargs)

        self.connected = True

    def connect(self):
        self.sock = self._setupSocket()

        ret = MyThreadedServer.run(self, self.sock)
        self._cleanupSocket(self.sock)
        self.shutdown()

        return ret

    def process(self):
        gevent.sleep(0.2)
        pass

    def disconnect(self):
        pass

if __name__ == '__main__':
    # WSGIServer(RequestHandler(), bindAddress=FCGI.sock, umask=0).run()
    FCGI().connect()
