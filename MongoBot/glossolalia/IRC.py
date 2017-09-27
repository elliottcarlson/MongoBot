# -*- coding: utf-8 -*-
import gevent
import gevent.monkey
import logging
import re
import time

gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
gevent.monkey.patch_dns()

from base64 import b64encode
from gevent import socket
from gevent import queue
from gevent.select import select as gselect
from ssl import SSLSocket
from eventemitter import EventEmitter
from collections import namedtuple
from pyparsing import printables, Suppress, Literal, Optional, Word, \
    ZeroOrMore, restOfLine, Combine, srange
from MongoBot.synapses import Synapse
from MongoBot.utils import ratelimited

logger = logging.getLogger(__name__)
RawCmd = namedtuple('RawCmd', 'cmd arg prefix tags')


class IRCMessage(object):

    def __init__(self):
        """
        <message>  ::= [':' <prefix> <SPACE> ] <command> <params> <crlf>
        <prefix>   ::= <servername> | <nick> [ '!' <user> ] [ '@' <host> ]
        <command>  ::= <letter> { <letter> } | <number> <number> <number>
        <SPACE>    ::= ' ' { ' ' }
        <params>   ::= <SPACE> [ ':' <trailing> | <middle> <params> ]
        <middle>   ::= <Any *non-empty* sequence of octets not including SPACE
                       or NUL or CR or LF, the first of which may not be ':'>
        <trailing> ::= <Any, possibly *empty*, sequence of octets not including
                       NUL or CR or LF>
        <crlf>     ::= CR LF
        """
        colon = Suppress(Literal(':'))
        nick = Word(printables, excludeChars='!@')('nick')
        user = Literal('!') + Word(printables, excludeChars='!@')('user')
        host = Literal('@') + Word(printables)('host')
        server = Word(printables)('server')
        source = Combine(nick + user + host | server)('source')
        action = Word(printables)('action')
        target = Optional(Word(printables)('target'))
        trailing_items = Word(printables, excludeChars=':')
        trailing = Optional(ZeroOrMore(trailing_items)('trailing'))
        params = (Optional(colon) + Optional(restOfLine('params')))

        rfc1459 = colon + source + action + target + trailing + params
        raw = Word(srange('[A-Z]'))('action') + params

        self.EBNF = (rfc1459 | raw)

    def parse(self, line):
        parsed = self.EBNF.parseString(line)
        return parsed.asDict()


class IRC(EventEmitter):

    EConnected = 'gconnected'
    EDisconnected = 'gdisconnected'
    EChanMsg = 'gchannel_message'
    EPrivMsg = 'gprivate_message'
    EChanNotice = 'gchannel_notice'
    EPrivNotice = 'gprivate_notice'

    buffer = b''
    connected = False
    name = False
    server = False
    regain_nick = False
    channels = {}
    auto_reconnect = True

    def __init__(self, settings):
        self.provider = 'irc'

        self.ident = settings.get('ident')
        self.realname = settings.get('realname')
        self.load_channels = settings.get('channels')

        self.nick = settings.get('nick')
        self.host = settings.get('host')
        self.port = settings.get('port')
        self.ssl = settings.get('ssl')
        self.password = settings.get('password')
        self.sasl = settings.get('sasl')

        self._reader = None
        self._writer = None
        self.send_queue = queue.Queue()

        self._register_handlers()

    def connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if hasattr(self, 'ssl') and self.ssl:
            self._sock = SSLSocket(self._sock)

        logger.info('Connect to IRC server %s:%s', self.host, self.port)

        try:
            self._sock.connect((self.host, self.port))
        except socket.error:
            return False

        self._sock_file = self._sock.makefile('r')
        self._reader = gevent.spawn(self._reader_loop)
        self._writer = gevent.spawn(self._writer_loop)

        self.connected = True
        self.emit(self.EConnected)

        return True

    def reconnect(self, maxdelay=30):
        gevent.sleep(30)

        return self.connect()

    def disconnect(self):
        self.buffer = b''

        if self._reader:
            self._reader.kill(block=False)

        if self._writer:
            self._writer.kill(block=False)

        self.send_queue.queue.clear()

        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        self._sock.close()
        self.connected = False
        self.emit(self.EDisconnected)

    def _reader_loop(self):
        misses = 0

        while True:
            gselect([self._sock], [], [])

            try:
                chunk = self._sock.recv(16384)
            except socket.error:
                chunk = b''

            if not chunk:
                misses += 1
                if misses > 3:
                    logger.info('Connection reset by peer (reader)')
                    self.disconnect()
                    return
                break
            misses = 0

            self.buffer += chunk
            chunks = self.buffer.split(b'\r\n')
            parser = IRCMessage()

            if len(chunks) > 1:
                self.buffer = chunks[-1]

                for line in chunks[:-1]:
                    logger.debug('SERVER: %s', repr(line))

                    try:
                        message = parser.parse(line)
                    except:
                        message = None

                    if not message:
                        continue

                    self.emit(message.get('action', None), message)

    def _writer_loop(self):
        while True:
            line = self.send_queue.get()

            try:
                self._sock.send(line)
            except socket.error:
                logger.debug('Connection reset by peer (writer)')
                self.disconnect()
                return

    def send_raw(self, line):
        logger.debug('CLIENT: %s', repr(line))

        if not self.connected:
            logger.debug('Not connected!')
            return

        # if isinstance(line, str):
        line = line.encode('utf-8')

        # self.send_queue.put_nowait(line.rstrip(b'\r\n ') + b'\r\n')
        self._sock.send(line.rstrip(b'\r\n ') + b'\r\n')

    @ratelimited(2)
    def chat(self, message, target=None, error=False):
        if not message:
            return

        self.send_raw(u'PRIVMSG %s :%s' % (
            target,
            message
        ))

    def colorize(self, text, color):

        colors = {
            'white': 0,
            'bold': 0,
            'black': 1,
            'blue': 2,
            'green': 3,
            'red': 4,
            'brown': 5,
            'purple': 6,
            'orange': 7,
            'yellow': 8,
            'lightgreen': 9,
            'teal': 10,
            'lightcyan': 11,
            'lightblue': 12,
            'pink': 13,
            'grey': 14,
            'lightgrey': 15,
        }

        if color in colors:
            color = colors[color]

        return '\x03%s\x02%s\x02\x03\x0f' % (str(color), text)

    def process(self):
        if self.connected:
            self.wait_event(self.EDisconnected, timeout=0.2)
        else:
            while not self.reconnect():
                pass

    def run_forever(self):
        while True:
            self.run_once()
            while not self.reconnect():
                pass

    def _register_handlers(self):
        self.on(self.EConnected, self._introduce)
        self.on('001', self._cmd_001)
        self.on('004', self._cmd_004)
        self.on('353', self._cmd_353)
        self.on('401', self._cmd_401)
        self.on('433', self._cmd_433)
        self.on('903', self._cmd_903)
        self.on('AUTHENTICATE', self._cmd_AUTHENTICATE)
        self.on('CAP', self._cmd_CAP)
        self.on('JOIN', self._cmd_JOIN)
        self.on('PART', self._cmd_PART)
        self.on('PING', self._cmd_PING)
        self.on('PRIVMSG', self._cmd_PRIVMSG)
        self.on('QUIT', self._cmd_QUIT)

    def _introduce(self):
        if not self.name:
            self.name = self.nick

        self.send_raw('CAP REQ :sasl')
        if self.password:
            self.send_raw('PASS %s' % self.password)

        self.send_raw('NICK %s' % self.name)
        self.send_raw('USER %s %s %s : %s' % (
            self.ident,
            self.ident,
            self.ident,
            self.realname
        ))

    def _cmd_001(self, msg):
        logger.info('Connected to %s' % msg.get('source', {}).get('server'))

        for channel in self.load_channels:
            logger.info('Joining %s' % channel)
            self.send_raw('JOIN %s' % channel)

    def _cmd_004(self, msg):
        self.name = msg.get('target')
        self.server = msg.get('source', {}).get('server')

        self.regain_nick = time.time()

    def _cmd_353(self, msg):
        channel = msg.get('trailing')[1]
        users = msg.get('params')

        self.channels[channel] = {
            'users': {
                re.sub('^[@+]', '', u):
                re.sub('^([@+])?.*', lambda m: m.group(1) or '', u)
                for u in users.split()
            }
        }

    def _cmd_401(self, msg):
        if self.regain_nick and time.time() - self.regain_nick < 20:
            self.name = None
            self.introduce()

    def _cmd_433(self, msg):
        self.name += '_'
        self._introduce()

    def _cmd_903(self, msg):
        self.send_raw('CAP END')

    def _cmd_AUTHENTICATE(self, msg):
        if msg.get('params') == '+':
            p = b64encode('{u}\0{u}\0{p}'.format(u=self.nick,
                          p=self.password).encode('ascii'))
            self.send_raw('AUTHENTICATE %s' % p.decode('utf-8'))

    def _cmd_CAP(self, msg):
        if 'ACK' in msg.get('trailing', []):
            self.send_raw('AUTHENTICATE PLAIN')

    def _cmd_JOIN(self, msg):
        self.send_raw('NAMES %s' % msg.get('target'))

    def _cmd_PART(self, msg):
        self.send_raw('NAMES %s' % msg.get('target'))

    def _cmd_PING(self, msg):
        self.send_raw('PONG %s' % msg.get('params'))

    @Synapse('__data')
    def _cmd_PRIVMSG(self, msg):
        return {
            'provider': self.provider,
            'service': self.__class__.__name__,
            'module': self.__module__,
            'source': msg.get('source'),
            'target': msg.get('target'),
            'data': msg.get('params')
        }

    def _cmd_QUIT(self, msg):
        self.send_raw('NAMES %s' % msg.get('target'))
