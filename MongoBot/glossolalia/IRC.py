# -*- coding: utf-8 -*-

import logging
import re
import socket
import ssl
import time
import traceback
from base64 import b64encode
from MongoBot.synapses import Synapse
from MongoBot.utils import ratelimited

logger = logging.getLogger(__name__)


class IRC(object):

    buffer = ''
    connection = False
    name = False
    server = False
    regain_nick = False
    channels = {}

    def __init__(self, settings):

        self.provider = settings.__name__

        self.ident = settings.ident
        self.realname = settings.realname
        self.load_channels = settings.channels

        self.nick = settings.nick
        self.host = settings.host
        self.port = settings.port
        self.ssl = settings.ssl
        self.password = settings.password
        self.sasl = settings.get('sasl')

    def connect(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        logger.info('Connect to IRC server %s:%s', self.host, self.port)
        sock.connect((self.host, self.port))

        if hasattr(self, 'ssl') and self.ssl:
            self.sock = ssl.wrap_socket(sock)
        else:
            self.sock = sock

        self.sock.setblocking(0)

        self.introduce()

    def introduce(self):

        if not self.name:
            self.name = self.nick

        self.send('CAP REQ :sasl')

        self.send('PASS %s' % self.password)
        self.send('NICK %s' % self.name)
        self.send('USER %s %s %s : %s' % (
            self.ident,
            self.ident,
            self.ident,
            self.realname
        ))

    def read(self):

        try:
            data = self.sock.recv(256)
        except Exception:
            return

        if data == b'':
            pass
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.connect()

        return data

    def send(self, data):

        data = data.rstrip('\r\n')

        logger.debug('CLIENT: %s', data)
        self.sock.send(('%s\r\n' % data).encode('utf-8'))

    @ratelimited(2)
    def chat(self, message, target=None, error=False):

        if not message:
            return

        self.send('PRIVMSG %s :%s' % (
            target,
            message.decode('utf-8')
        ))

    def colorize(self, text, color):

        colors = {
            'white': 0,
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

        if (self.name != self.nick and self.regain_nick and
                time() - self.regain_nick > 20):

            self.regain_nick = time()
            self.send('WHOIS %s' % self.nick)

        data = self.read()

        if not data:
            return

        self.buffer += data.decode('utf-8')
        lines = self.buffer.split('\n')
        self.buffer = lines.pop()

        for line in lines:
            if line[-1] == '\n':
                line = line[:-1]

            if not line:
                continue

            logger.debug('SERVER: %s', line)

            source = ''

            if line[0] == ':':
                source, line = line[1:].split(' ', 1)

            if line.find(' :') != -1:
                line, trailing = line.split(' :', 1)
                args = line.split()
                args.append(trailing)
            else:
                args = line.split()

            command = args.pop(0)

            method = getattr(self, '_cmd_%s' % command, None)

            try:
                if method is not None:
                    method(source, args)

            except Exception as e:

                print("%s" % e)
                print(traceback.format_exc())
                continue

    def _cmd_001(self, source, args):

        logger.info('Connected to %s' % source)

        for channel in self.load_channels:

            logger.info('Joining %s' % channel)
            self.send('JOIN %s' % channel)

    def _cmd_004(self, source, args):

        self.name = args.pop(0)
        self.server = args.pop(0)

        self.regain_nick = time.time()

    def _cmd_353(self, source, args):

        users = args[-1]
        channel = args[-2]

        self.channels[channel] = {
            'users': {
                re.sub('^[@+]', '', u):
                re.sub('^([@+])?.*', lambda m: m.group(1) or '', u)
                for u in users.split()
            }
        }

    def _cmd_401(self, source, args):

        if self.regain_nick and time() - self.regain_nick < 20:
            self.name = None
            self.introduce()

    def _cmd_433(self, source, args):

        self.name += '_'
        self.introduce()

    def _cmd_903(self, source, args):

        self.send('CAP END')

    def _cmd_AUTHENTICATE(self, source, args):

        if args[0] == '+':
            p = b64encode('{u}\0{u}\0{p}'.format(u=self.nick,
                          p=self.password).encode('ascii'))
            self.send('AUTHENTICATE %s' % p.decode('utf-8'))

    def _cmd_CAP(self, source, args):

        if args[1] == 'ACK':
            self.send('AUTHENTICATE PLAIN')

    def _cmd_JOIN(self, source, args):

        channel = args.pop(0)
        self.send('NAMES %s' % channel)

    def _cmd_PART(self, source, args):

        channel = args.pop(0)
        self.send('NAMES %s' % channel)

    def _cmd_PING(self, source, args):

        self.send('PONG %s' % args[-1])

    @Synapse('MONGO_INCOMING_DATA')
    def _cmd_PRIVMSG(self, source, args):

        target = args[0]
        data = args[-1]

        if target == self.name:
            target = source.split('!', 1)[0]

        return {
            'provider': self.provider,
            'service': self.__class__.__name__,
            'module': self.__module__,
            'source': source,
            'target': target,
            'data': data
        }

    def _cmd_QUIT(self, source, args):

        channel = args.pop(0)
        self.send('NAMES %s' % channel)
