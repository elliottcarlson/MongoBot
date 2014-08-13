from math import *
from secrets import CHANNEL

# Connection Settings
HOST = 'chat.freenode.net'
PORT = 6667
NICK = 'MongoBot'
USE_SSL = False

# ChanServ/NickServ availability
HAS_CHANSERV = True
HAS_NICKSERV = True

# Used to filter out pings and server responses from
# logs and live checks. Obviously if you're not on
# freenode, you'll need to update this.
SCAN = '^:\w+\.freenode\.net'

# TODO: Normalize dir pattern endings ('/' or not)
# Directory settings
STORAGE = 'hippocampus'
LOGDIR = STORAGE + '/log'
ERRORLOG = STORAGE + '/log/error.log'
LOG = LOGDIR + '/chat.log'
BOOKS = 'booklearnin/'
DISTASTE = STORAGE + '/distaste'
ACROSCORE = STORAGE + '/acro/'
DOWNLOADS = STORAGE + '/downloads/'
IMGS = STORAGE + '/downloads/imgs/'
VIDS = STORAGE + '/downloads/videos/'
GIFS = '/static/gifs/'
THUMBS = '/static/thumbs/'
THUMB_SIZE = 40
REGISTERED = STORAGE + '/allowed'
POEMS = STORAGE + '/poems/'

# Enabled libraries. These are the default brainmeats
# that load up on start or reboot. You can enable and
# disable them with -enable and -disable while the bots
# running. Comment out anything you don't want to load
# here.
ENABLED = [
    'acro',
    'alien',
    'artsy',
    'broca',
    'chess',
    'channeling',
    'diplomacy',
    'facebook',
    'finance',
    'hangman',
    'holdem',
    'memory',
    'nonsense',
    'peeps',
    'quotes',
    'reference',
    'sms',
    'stockgame',
    'system',
    'twitting',
    'turing',
    'webserver',
]

# Misc
CONTROL_KEY = '-' # All commands are preceded by this. It can be whatever you want.
MULTI_PASS = '*'
CKEYS = [CONTROL_KEY, MULTI_PASS]
SHORTENER = 'http://roa.st/api.php'
PATIENCE = 7000
REPO = 'https://github.com/huntwelch/MongoBot' # Used by the -source command.
SMS_LOCKFILE = '/tmp/sms.lock'
REDIS_SOCK = '/tmp/redis.sock'
PULSE = '/tmp/bot.pulse'
PULSE_RATE = 25
STORE_URLS = True
STORE_IMGS = True
BABBLE_LIMIT = 100
TIMEZONE = 'EST'

# Web server
WEBSITE = 'http://mongobot.com'
SERVER_RELOAD = '/tmp/mongo.reload'

# Stock game
VALID_EXCHANGES = frozenset(['NYSE', 'NYSEARCA', 'NYSEAMEX', 'NASDAQ'])
STARTING_CASH = 100000

# Acro
ACROLIB = 'natwords'
MINLEN = 5
MAXLEN = 7
ROUNDS = 5
ROUNDTIME = 120
WARNING = 30
VOTETIME = 30
MIN_PLAYERS = 3
TIME_FACTOR = 2
NO_ACRO_PENALTY = 2
NO_VOTE_PENALTY = 5
BREAK = 15
BOTPLAY = True

# These are settings that can be changed during
# runtime with the -update command. Note that
# update actually rewrites this file; changes are
# permanent. You can also add a setting here if
# you want to make it available.
SAFESET = [
    ('Bot settings', ':'),
    ('CONTROL_KEY', '"' + CONTROL_KEY + '"'),
    ('SHORTENER', '"' + SHORTENER + '"'),
    ('PATIENCE', PATIENCE),
    ('NICK', '"' + NICK + '"'),
    ('HOST', '"' + HOST + '"'),
    ('PORT', PORT),

    ('Acro settings', ':'),
    ('ACROLIB', ACROLIB),
    ('MINLEN', MINLEN),
    ('MAXLEN', MAXLEN),
    ('ROUNDS', ROUNDS),
    ('ROUNDTIME', ROUNDTIME),
    ('WARNING', WARNING),
    ('VOTETIME', VOTETIME),
    ('MIN_PLAYERS', MIN_PLAYERS),
    ('NO_ACRO_PENALTY', NO_ACRO_PENALTY),
    ('NO_VOTE_PENALTY', NO_VOTE_PENALTY),
    ('BREAK', BREAK),
    ('BOTPLAY', BOTPLAY),
]

# If you want an obnoxious bot. INSULT/INSULTS
# are just used by the acro. game.
INSULTS = [
    'are little bitches',
    'are chumps',
    'are cunt knockers',
    'are lazy bastards',
    "are busy with dcross's mom",
]
INSULT = [
    'is a little bitch',
    'is a chump',
    'is a cunt knocker',
    'is a lazy bastard',
    "is busy with dcross's mom",
]
BOREDOM = [
    'kicks',
    'slaps',
    'throws feces at',
    "offers dcross's mom to",
]


# For James's excellent tourettes feature
SMARTASS = True
TECH_QUESTIONS = [
    'how do i',
    'how do you',
    'how does one',
    'how would i',
    'how would you',
    'how would one',
    'does anyone know how',
    'do you know how',
]
IT_HELP = [
    'Have you tried turning it off an on again?',
    'Have you tried forcing an unexpected reboot?',
    'Are you sure your computer is on?',
    'Have your tried connecting the computer directly to the modem?',
    'Have you power-cycled it?',
]

# Table tossers
FRUSTRATION = [
    'fuck',
    'shit',
    'dammit',
    'goddammit',
    'wtf',
    'the hell',
]

# Math functions available to the -hack command.
SAFE = [
    ('abs', abs),
    ('acos', acos),
    ('asin', asin),
    ('atan', atan),
    ('atan2', atan2),
    ('ceil', ceil),
    ('cos', cos),
    ('cosh', cosh),
    ('degrees', degrees),
    ('e', e),
    ('exp', exp),
    ('fabs', fabs),
    ('floor', floor),
    ('fmod', fmod),
    ('frexp', frexp),
    ('hypot', hypot),
    ('ldexp', ldexp),
    ('log', log),
    ('log10', log10),
    ('modf', modf),
    ('pi', pi),
    ('pow', pow),
    ('radians', radians),
    ('sin', sin),
    ('sinh', sinh),
    ('sqrt', sqrt),
    ('tan', tan),
    ('tanh', tanh),
]
