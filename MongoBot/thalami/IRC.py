# -*- coding: utf-8 -*-

import logging
import re
import socket
import ssl
import sys
import traceback

from MongoBot.synapses import Synapse

logger = logging.getLogger(__name__)

class IRC(object):

    buffer = ''
    connection = False
    name = False
    server = False
    regain_nick = False
    channels = {}

    def __init__(self):

        self.secrets_bot_ident = 'fubahder'
        self.secrets_bot_realname = 'fubahder'
        self.secrets_channels = [
            '#fubahder'
        ]

        self.settings_bot_nick = 'fubahder'
        self.settings_irc_host = 'chat.freenode.net'
        self.settings_irc_port = 6697
        self.settings_irc_ssl = True


    def connect(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        logger.info('Connect to IRC server %s:%s', self.settings_irc_host,
                self.settings_irc_port)
        sock.connect((self.settings_irc_host, self.settings_irc_port))

        #if hasattr(self_settings_irc, 'ssl') and self.settings_irc_ssl:
        self.sock = ssl.wrap_socket(sock)
        #else:
        #    self.sock = sock

        self.sock.setblocking(0)

        #if hasattr(self.secrets_irc, 'password') and self.secrets.irc.password:
        #    self.send('PASS %s' % self.secrets.irc.password)

        self.introduce()


    def introduce(self):
        
        if not self.name:
            self.name = self.settings_bot_nick

        self.send('USER %s %s %s : %s' % (
            self.secrets_bot_ident,
            self.secrets_bot_ident,
            self.secrets_bot_ident,
            self.secrets_bot_realname
        ))
        self.send('NICK %s' % self.name)


    def read(self):

        try:
            data = self.sock.recv(256)
        except Exception as e:
            return

        if data == b'':
            print 'Connection lost.'
            sys.exit()

        return data

    def send(self, data):

        data = data.rstrip('\r\n')

        self.sock.send('%s%s%s' % (data, chr(015), chr(012)))


    def process(self):

        if (self.name != self.settings_bot_nick and self.regain_nick and
            time() - self.regain_nick > 20):

            self.regain_nick = time()
            self.send('WHOIS %s' % self.settings_bot_nick)

        data = self.read()

        if not data:
            return

        self.buffer += data
        lines = self.buffer.split(chr(012))
        self.buffer = lines.pop()

        for line in lines:
            if line[-1] == chr(015):
                line = line[:-1]

            if not line:
                continue

            logger.info('[IRC] Data: %s', data)

            source = ''
            target = ''

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

        logger.info('[IRC] Connected to %s' % source)

        for channel in self.secrets_channels:

            logger.info('[IRC] Joining %s' % channel)
            self.send('JOIN %s' % channel)

    def _cmd_004(self, source, args):

        self.name = args.pop(0)
        self.server = args.pop(0)

        self.regain_nick = time()

    def _cmd_353(self, source, args):

        users = args[-1]
        channel = args[-2]

        self.channels[channel] = {
            'users': {
                re.sub('^[@+]', '', u): re.sub('^([@+])?.*', lambda m: m.group(1) or '', u)
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

    def _cmd_PING(self, source, args):

        self.send('PONG %s' % args[-1])

    def _cmd_PART(self, source, args):
        
        channel = args.pop(0)
        self.send('NAMES %s' % channel)

    def _cmd_JOIN(self, source, args):

        channel = args.pop(0)
        self.send('NAMES %s' % channel)

    def _cmd_QUIT(self, source, args):

        channel = args.pop(0)
        self.send('NAMES %s' % channel)

    @Synapse('THALAMUS_DATA')
    def _cmd_PRIVMSG(self, source, args):

        target = args[0]
        data = args[-1]

        return {
            source: source,
            target: target,
            data: data
        }
