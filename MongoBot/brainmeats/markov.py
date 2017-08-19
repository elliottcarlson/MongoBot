# -*- coding: utf-8 -*-

import re
import redis
from MongoBot.autonomic import axon
from MongoBot.synapses import Cerebellum, Receptor


@Cerebellum
class Markov(object):
    """
    MongoBot's ability to run a markov chain is a large part of the reason I
    started working on mongo in the first place.

    (cough)

    So MongoBot was made on a whim in the chatroom of his birth just because I
    wanted to know how to make a bot. Since at the time I was pretty checked
    out of my job I put an awful lot of work into him, and he eventually edged
    out ExStaffRobot as the dominant bot.

    ExStaffRobot itself was a descendent of StaffRobot, the dev irc chatbot
    that warned us about failures and stuff at OkCupid (the Staff Robot that
    pops up all over OkCupid is itself a rendering of this StaffRobot by one of
    the frontend designers. He and I never got on, but he does draw a mean
    bot). This StaffRobot had a markov chat function in it, which I didn't
    really understand at the time, as I was scared of all these awesome CS
    majors, and was, essentially, an out-of-work film student who only got the
    job because a few of the powers that were didn't think frontend programmers
    needed to be very smart. But I really wanted to put a markov chain in my
    bot, partly to understand and because I missed the old bot after one of the
    founders bitched about it being annoying until we had to turn it off, and
    another small piece of the personality that kept me at the job through the
    first year of death camp hours was wicked away.

    So three years after MongoBot made his first appearance I finally faced my
    fears of inferiority and looked up a markov chain on wikipedia, where I
    discovered it was, in fact, totally fucking trivial.

    It reminds me a bit of a video editor who was training me on an internship,
    and I asked him how to do split screen and he said he didn't think I was
    ready for that yet, so I just taught myself. When he found out, he got so
    upset he walked out of the room. Point is, Americans have some seriously
    fucked up problems with their opinions on the nature and value of
    intelligence.
    """
    chain_length = 2
    chattiness = 0.01
    max_words = 30
    message_to_generate = 5
    separator = '\x01'
    stop_word = '\02'

    def __init__(self):

        self.redis_conn = redis.Redis()

    def split_message(self, message):

        words = message.split()[1:]

        if len(words) > self.chain_length:
            words.append(self.stop_word)

            for i in range(len(words) - self.chain_length):
                print(words[i:i + self.chain_length + 1])
                return words[i:i + self.chain_length + 1]

        return words

    def sanitize_message(self, message):

        return re.sub('[\"\']', message.lower(), message)

    def make_key(self, key):
        return '-'.join(('markov', key))

    def mark(self, message):

        for words in self.split_message(self.sanitize_message(message)):

            key = self.separator.join(words[:-1])
            self.redis_conn.sadd(self.make_key(key), words[-1])

    def generate(self, seed):

        key = seed
        gen_words = []

        for i in xrange(self.max_words):
            words = key.split(self.separator)
            gen_words.append(words[0])
            next_word = self.redis_conn.srandmember(self.make_key(key))
            if not next_word:
                break

            key = self.separator.join(words[1:] + [next_word])

        return ' '.join(gen_words)

    @axon
    def babble(self):

        print('BABBLE??')

        if self.stdin:
            key = self.stdin.split()
            print('self.stdin: %s' % key)
        elif self.values:
            key = self.values
            print('self.values: %s' % key)
        if not self.values and not self.stdin:
            key = self.redis_conn.srandkey()
            print('Random key: %s' % key)

        return ' '.join(key)
        # return self.generate(['a'])

    @axon
    # @help('URL_OF_TEXT_FILE <Read something>')
    def learn(self):
        if not self.values and not self.stdin:
            return 'Learn what?'

    @Receptor('overheard')
    def markov_learn(self, incoming):

        if incoming.get('data')[0:1] is not '.':
            print('Incoming: %s' % incoming.get('data').encode('utf-8'))

            self.mark(incoming.get('data'))
