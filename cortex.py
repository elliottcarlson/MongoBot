import re
import shutil
import pkgutil
import socket
import string


from os import path
from datetime import date, timedelta, datetime
from pytz import timezone
from time import time, mktime, localtime, sleep
from random import randint
from config import load_config

#from settings import PATIENCE, SCAN, STORE_URLS, \
#    STORE_IMGS, IMGS, MULTI_PASS, HAS_CHANSERV, THUMBS, WEBSITE
#from secrets import CHANNEL, OWNER, REALNAME, MEETUP_NOTIFY, CHANNELS


from datastore import Drinker, connectdb
from util import unescape, shorten, ratelimited, postdelicious, savefromweb, \
    Browse, Butler
from autonomic import serotonin, Neurons, Synapse
from thalamus import Thalamus

import traceback


CHANNEL = '#okdrink'
MULTI_PASS = '*'

# TODO:
# remove names check, use other means
# do logging and tracebacks

# Basically all the interesting interaction with
# irc and command / content parsing happens here.
# Also connects to mongodb.
class Cortex:

    context = CHANNEL

    master = False
    sock = False
    values = False
    lastpublic = False
    replysms = False
    lastprivate = False
    lastsender = False
    gettingnames = True
    memories = False
    autobabble = False
    lastcommand = False
    joined = False
    operator = False
    bequiet = False

    butler = False

    channels = []
    public_commands = []
    members = []
    guests = []
    broken = []
    REALUSERS = []

    commands = {}
    live = {}
    helpmenu = {}

    boredom = int(mktime(localtime()))
    namecheck = int(mktime(localtime()))

    thalamus = False


    def __init__(self, master):

        print '* Initializing'
        self.master = master
        self.settings = master.settings
        self.secrets = master.secrets
        self.channels = self.secrets.channels
        self.personality = self.settings.bot

        print '* Exciting neurons'
        Neurons.cortex = self

        print '* Loading brainmeats'
        self.loadbrains()

        print '* Waking butler'
        self.butler = Butler(self)

        print '* Loading users'
        self.REALUSERS = load_config(self.settings.directory.authfile)

        print '* Connecting to datastore'
        connectdb()

        print '* Evolving thalamus'
        self.thalamus = Thalamus(self)

    # Loads up all the files in brainmeats and runs them
    # through the hookup process.
    def loadbrains(self, electroshock=False):
        self.brainmeats = {}
        brainmeats = __import__('brainmeats', fromlist=[])
        if electroshock:
            reload(brainmeats)

        areas = [name for _, name, _ in pkgutil.iter_modules(['brainmeats'])]

        for area in areas:
            print '{0: <25}'.format('  - %s' % area),

            if area not in self.master.ENABLED:
                print '[\033[93mDISABLED\033[0m]'
                continue

            try:
                mod = __import__('brainmeats', fromlist=[area])
                mod = getattr(mod, area)
                if electroshock:
                    reload(mod)
                cls = getattr(mod, area.capitalize())
                self.brainmeats[area] = cls(self)
                print '[\033[0;32mOK\033[0m]'
            except Exception as e:
                self.chat('Failed to load %s.' % area, error=str(e))
                self.broken.append(area)
                self.master.ENABLED.remove(area)
                print '[\033[0;31mFAILED\033[0m]'
                if self.settings.debug.verbose:
                    print e
                    print traceback.format_exc()


        for brainmeat in self.brainmeats:
            serotonin(self, brainmeat, electroshock)

    '''
    When you get amnesia, it's probably a good time to really
    think and try to remember who you are.
    '''
    def amnesia(self):

        # This is an easy way out for now...
        return self.personality


    # I'll be frank, I don't have that great a grasp on
    # threading, and despite working with people who do,
    # there were a number of live processes that thread
    # solutions weren't solving.
    #
    # The solution was to have everything that needs to
    # run live run on one ticker. If you need something
    # to run continuously, add this to the __init__ of
    # your brainmeat:
    #
    # self.cx.addlive(self.ticker)
    #
    # ticker being the function in the class that runs.
    # see brainmeats/sms.y for a good example of this.
    def addlive(self, func, alt=False):
        name = alt or func.__name__
        self.live[name] = func

    def droplive(self, name):
        del self.live[name]

    # Core automatic stuff. I firmly believe boredom to
    # be a fundamental process in both man and machine.
    def parietal(self, currenttime):

        # This should really just be an addlive. Maybe
        # the other two functions, too.
#        calendar = datetime.now(timezone(self.settings.general.timezone))
#        if calendar.hour in MEETUP_NOTIFY and 'peeps' in self.brainmeats:
#            self.brainmeats['peeps'].meetup(calendar.hour)

#        if currenttime - self.boredom > PATIENCE:
#            self.boredom = int(mktime(localtime()))
#            if randint(1, 10) == 7:
#                self.bored()

        for func in self.live:
            self.live[func]()

    # And this is basic function that runs all the time.
    # The razor qualia edge of consciousness, if you will
    # (though you shouldn't). It susses out the important
    # info, logs the chat, sends PONG, finds commands, and
    # decides whether to send new information to the parser.
    def monitor(self):

        currenttime = int(mktime(localtime()))
        self.parietal(currenttime)

        self.thalamus.process()

# Synapse this shit so chanserv/nickserv happens on connect
#        if HAS_CHANSERV and self.joined and not self.operator:
#            self.sock.send('PRIVMSG ChanServ :op %s %s\n' % (CHANNEL, self.personality.nick))
#            self.operator = True

#                self.logit(line + '\n')

#            elif line.find('PRIVMSG') != -1:
#                self.boredom = currenttime
#                content = line.split(' ', 3)


    # Le parser. This used to be a very busy function before
    # most of its actions got moved to the nonsense and
    # broca brainmeats.
    def parse(self, msg):

        print "!!! In cortex.parse(%s)" % msg

        pwd = re.search(':-passwd', msg)
        if not pwd:
            print msg

        try:
            info, content = msg[1:].split(' :', 1)
            sender, type, room = info.strip().split()
        except:
            return

        try:
            nick, data = sender.split('!')
            realname, ip = data.split('@')
            realname = realname.strip('~')
        except Exception as e:
            print str(e)
            return

        # SPY
        if room in self.channels \
        and 'spy' in self.channels[room] \
        and self.channels[room].spy:
            self.context = CHANNEL
            report = '%s %s: %s' % (room, nick, content)
            self.announce(report)
            return

        try:
            ip = socket.gethostbyname_ex(ip.strip())[2][0]
            self.lastrealsender = '%s@%s' % (realname, ip)
        except:
            self.lastrealsender = False
            pass

        if nick not in self.members:
            self.members.append(nick)

        self.lastsender = nick
        self.lastip = ip
        self.lastchat = content


        # Determine if the action is a command and the user is
        # approved.
        if content[:1] == self.personality.command_prefix or content[:1] == MULTI_PASS:

            # Tack on last command if it's just the control
            if content == self.personality.command_prefix or content[:2] == self.personality.command_prefix + ' ':
                if not self.lastcommand:
                    return

                content = '%s%s %s' % (self.personality.command_prefix, self.lastcommand, content[2:])


            if self.lastrealsender not in self.REALUSERS \
            and content[1:].split()[0] not in self.public_commands \
            and nick not in self.guests:
                self.chat('My daddy says not to listen to you.')
                return

            # A hack to maintain reboot until I figure
            # our something better.
            if content.find('%sreboot' % self.personality.command_prefix) == 0:
                self.command(nick, content)
                return

            self.butler.do(self.command, (nick, content))
            return

        # This is a special case for giving people meaningless
        # points so you can feel like you're in grade school
        # again.
        if content[:-2] in self.members and content[-2:] in ['--', '++']:
            self.values = [content[:-2]]
            if content[-2:] == '++':
                self.chat(self.commands.get('increment')())
            if content[-2:] == '--':
                self.chat(self.commands.get('decrement')())
            return

        # Grab urls. Mongo automatically tries to get the title
        # and create a short link.
        ur = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        match_urls = re.compile(ur)
        urls = match_urls.findall(content)
        if len(urls):
            self.linker(urls)
            return

        # Been messing around with NLTK without much success,
        # but there's a lot of experimenting in the broca
        # meat. At time of writing, it does Mongo's auto responses
        # in tourettes and adds to the markov chain.
        if 'broca' in self.brainmeats:
            self.brainmeats['broca'].tourettes(content, nick)
            self.brainmeats['broca'].mark(content)
            if self.autobabble and content.find(self.personality.nick) > 0:
                self.brainmeats['broca'].babble()


    # If it is indeed a command, the cortex stores who sent it,
    # and any words after the command are split in a values array,
    # accessible by the brainmeats as self.values.
    multis = 0
    def command(self, sender, cmd, piped=False):

        print "!!! In cortex.command(%s, %s, %s)" % (sender, cmd, piped)
        print '] self.context = %s' % self.context

        if self.context in self.channels \
        and 'command' not in self.channels[self.context]:
            return

        chain = cmd.split('|', 1)
        pipe = False

        if len(chain) is 2:
            cmd = chain[0].strip()
            pipe = chain[1].strip()

        if piped:
            cmd = '%s %s' % (cmd, piped)

        components = cmd.split()

        _what = components.pop(0)

        what = _what[1:]
        means = _what[:1]

        is_nums = re.search("^[0-9]+", what)
        is_breaky = re.search("^" + self.personality.command_prefix + "|[^\w]+", what)
        if is_nums or is_breaky or not what:
            return

        if components:
            self.values = components
        else:
            self.values = False

        self.logit('%s sent command: %s\n' % (sender, what))
        self.lastsender = sender
        self.lastcommand = what

        result = None

        # So you'll notice that some commands return
        # values that this function sorts out into chats,
        # while other commands directly run the self.chat,
        # ._act, and .announce functions attached by the
        # Dendrite class. Well, it used to be just those
        # self.chat(whatever) and return, because it's a bot,
        # right? It's final output is a chat, otherwise it's
        # not much of a chatbot.
        #
        # Then some asshole in our chatroom said something
        # like "it'd be cool if we could pipe commands, like
        # -tweet|babble or something."
        #
        # So THAT got stuck in my head even though it's
        # totally ridiculous, but I won't be able to sleep
        # until it's fully implemented, and the first step
        # in that is the ability to do something besides
        # just chat out at the end of the function. If it's
        # being piped, the best way to do that is reset
        # self.values to the result of the command if it's
        # piped from or to a pipeable function (I know
        # 'from or to' should be one or the other, but it's
        # 1am and I'm drunkenly listening to the Nye vs.
        # Ham debate over youtube and it's almost as
        # upsetting as realizing I'm going to have to comb
        # over every goddamn function in this bot to
        # determine what's pipeable and change its output).
        #
        # Point is, you can return a list or a string at
        # the end of a brainmeat command, or just use chat.
        # I probably won't worry about act and announce.
        if means == MULTI_PASS:

            # All this multi checking had to be put in
            # after Eli decided to enter this:
            # -babble fork | *babble | *babble | *babble
            # ... which of course spiked the redis server
            # to 100% CPU and eventually flooded the chat
            # room with n^4 chats until the bot had to be
            # kicked. This is what happens when you try
            # to give nice things to hackers.
            self.multis += 1
            if self.multis > 1:
                self.chat('This look like fork bomb. You kick puppies too?')
                self.multis = 0
                return

            result = []

            if not components:
                self.chat("No args to iter. Bitch.")
                self.multis = 0
                return

            for item in components:
                self.values = [item]
                _result = self.commands.get(what, self.default)()
                result.append(_result)
        else:
            try:
                result = self.commands.get(what, self.default)()
            except Exception as e:
                # proper logging here

                self.chat(str(e))
                print traceback.format_exc()

        if not result:
            return

        if pipe:
            # Piped output must be string!
            if type(result) is list:
                result = ' '.join(result)
            self.command(sender, pipe, result)
            return

        if type(result) in [str, unicode]:
            self.chat(result)

        if type(result) is list:
            if len(result) > 20:
                result = result[:20]
                result.append("Such result. So self throttle. Much erotic. Wow.")

            for line in result:
                self.chat(line)

        self.multis = 0

    # If you want to restrict a command to the bot admin.
    def validate(self):

        print "!!! In cortex.validate"

        if not self.values:
            return False
        if self.lastsender != OWNER:
            return False
        return True


    # Careful with this one.
    def bored(self):
        if not self.members:
            return

        self.announce('Chirp chirp. Chirp Chirp.')

        # The behavior below is known to be highly obnoxious
        # self.act("is bored.")
        # self.act(choice(BOREDOM) + " " + choice(self.members))

    # Simple logging.
    # TODO: chenge to normal python logging
    def logit(self, what):
        with open(self.settings.directory.log, 'a') as f:
            f.write('TS:%s;%s' % (time(), what))

        now = date.today()
        if now.day != 1:
            return

        prev = date.today() - timedelta(days=1)
        backlog = '%s/%s-mongo.log' % (self.settings.directory.log, prev.strftime('%Y%m'))

        if path.isfile(backlog):
            return

        shutil.move(self.settings.directory.log, backlog)

    # Sort out urls.
    @Synapse('url')
    def linker(self, urls):

        return urls

        for url in urls:
            # Special behaviour for Twitter URLs
            match_twitter_urls = re.compile('http[s]?://(www.)?twitter.com/.+/status/([0-9]+)')

            twitter_urls = match_twitter_urls.findall(url)
            if len(twitter_urls):
                self.tweet(twitter_urls)
                return

            if url.find('gist.github') != -1:
                return

            if randint(1, 5) == 1:
                try:
                    self.commands.get('tweet', self.default)(url)
                except:
                    pass

            fubs = 0
            title = "Couldn't get title"

            site = Browse(url)

            if site.error:
                self.chat('Total fail: %s' % site.error)
                continue

            roasted = shorten(url)
            if not roasted:
                roasted = "Couldn't roast"
                fubs += 1

            try:
                ext = site.headers()['content-type'].split('/')[1]
            except:
                ext = False

            images = [
                'gif',
                'png',
                'jpg',
                'jpeg',
            ]

            if ext in images:
                title = 'Image'
                # Switch this to a Browse method
                if STORE_IMGS:
                    fname = url.split('/').pop()
                    path = IMGS + fname
                    self.butler.do(savefromweb, (url, path, self.lastsender), 'Thumb @ %s')

            elif ext == 'pdf':
                title = 'PDF Document'

            else:
                title = site.title()

            # If you have a delicious account set up. Yes, delicious
            # still exists. Could be updated to a cooler link
            # collecting service.
            if STORE_URLS:
                postdelicious(url, title, self.lastsender)

            if fubs == 2:
                self.chat("Total fail")
            else:
                self.chat("%s @ %s" % (unescape(title), roasted))

    # This shows tweet content if a url is to a tweet.
    def tweet(self, urls):
        if 'twitting' not in self.brainmeats:
            return

        for url in urls:
            self.chat(self.brainmeats['twitting'].get_tweet(url[1]))

    # Announce means the chat is always sent to the channel,
    # never back as a private response.
    @ratelimited(2)
    def announce(self, message):
        self.chat(message, target=CHANNEL)

    # Since chat is mongo's only means of communicating with
    # a room, the ratelimiting here should prevent any overflow
    # violations.
    # NOTE: 'and not target' may be a sketchy override; test it
    @ratelimited(2)
    def chat(self, message, target=False, error=False):

        if self.context in self.channels \
        and not target \
        and not self.channels[self.context].speak:
            return

        if self.bequiet:
            return

        if not message:
            return

        if target:
            whom = target
        elif self.context in self.channels:
            whom = self.context
        else:
            whom = self.lastsender

        filter(lambda x: x in string.printable, message)
        try:
            message = message.encode('utf-8')
            self.logit('___%s: %s\n' % (self.personality.nick, str(message)))
            m = str(message)
            if randint(1, 170) == 23:
                i = m.split()
                pos = randint(0, len(i))
                i.insert(pos, 'fnord')
                m = ' '.join(i)

            if error:
                m += ' ' + str(error)
            self.thalamus.send('PRIVMSG %s :%s' % (whom,m))
            if self.replysms:
                to = self.replysms
                self.replysms = False
                self.values = [to, str(m)]
                self.commands.get('sms')()
        except:
            try:
                self.thalamus.send('PRIVMSG %s :Having trouble saying that for some reason' % whom)
            except:
                pass
                 #print "Unable to say: %s" % message

    def act(self, message, public=False, target=False):
        message = '\001ACTION %s\001' % message
        if public:
            self.announce(message)
        elif target:
            self.chat(message, target)
        else:
            self.chat(message)
            if self.replysms:
                to = self.replysms
                self.replysms = False
                self.values = [to, str(message)]
                self.commands.get('sms')()

    # When all else fails.
    def default(self):
        self.act(" cannot do this thing :'(")
