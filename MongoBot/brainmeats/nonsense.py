# -*- coding: utf-8 -*-
import logging
import re
import yaml

from MongoBot.autonomic import axon, help
from MongoBot.staff.browser import Browser
from random import choice

logger = logging.getLogger(__name__)


class Nonsense(object):
    """
    #TODO list
    munroesecurity
    reward:
    mom
    say -- because of self.announce
    """
    @axon
    @help('<yeah let\'s do this>')
    def raincheck(self):
        """
        This used to be 'my girl call your girl' which was probably funnier,
        but lost on the current generation, and the irony of this obscure
        casual sexism from the past would be missed, leaving it to just be
        another minor degredation of women. Is it such a small thing everyone
        should probably suck it up? Probably, yeah. But it's easier to tell
        everyone to suck it up when you've never had to, and especially in the
        programming world, we shouldn't do it in the first place, because it's
        trivial not to, and anybody who can't make miniscule changes to the
        dialogue in the name of others' comfort is an asshole.
        """
        return ('Lemme just stick a pin in that and I\'ll have my people'
                'call your people to pencil in a lunch some time.')

    @axon
    @help('<bounce>')
    def bounce(self):
        """
        Because Busta Motherfuckin Rhymes
        """
        return 'https://www.youtube.com/watch?v=c1d0UyovSN8'

    @axon
    @help('<get cat fact>')
    def catfact(self):
        """
        This is almost exclusively used to troll people in conjunction with the
        sms command. Should hook that shit up.
        """
        url = 'https://catfact.ninja/fact'

        try:
            json = Browser(url).json()
        except:
            return 'No meow facts.'

        return json['fact']

    @axon
    @help('<generate bullshit>')
    def buzz(self):
        """
        Excellent antidote for a long meeting.
        """
        adjective = choice(self.config['buzz']['adjectives'])
        noun = choice(self.config['buzz']['nouns'])
        verb = choice(self.config['buzz']['verbs'])

        return ' '.join([adjective, noun, verb])

    @axon
    @help('<grab a little advice>')
    def advice(self):
        """
        Because life can be hard to go through alone.
        """
        url = 'http://api.adviceslip.com/advice'

        try:
            json = Browser(url).json()
        except:
            return 'Use a rubber if you sleep with dcross\'s mother.'

        return json['slip']['advice'] + '.. except in bed.'

    @axon
    @help('SEARCHTERM <grab random fml entry>')
    def fml(self):
        """
        An endless avalanche of whiny first world teenages complaining about
        their worthless entitled lives. I don't know why it's cathartic, but it
        is.
        """
        url = 'http://www.fmylife.com'

        if self.values:
            url += '/search/' + '%20'.join(self.values)
        else:
            url += '/random'

        try:
            request = Browser(url)
            soup = request.soup()
            fmls = soup.find_all(string=re.compile('Today,.*FML'))
            fml = choice(fmls).strip()
            return fml
        except Exception as e:
            logger.exception(e)
            return 'Nobody\'s life got fucked like that'

    @axon
    @help('<generate start-up elevator pitch>')
    def startup(self):
        url = 'http://itsthisforthat.com/api.php?json'

        try:
            request = Browser(url)
            json = request.json()

            this = json['this'].lower().capitalize()
            that = json['that'].lower().capitalize()

            return 'It\'s a %s for %s' % (this, that)
        except Exception:
            return 'It\'s a replacement for itsthisforthat.com...'

    @axon
    def cry(self):
        self.act('cries.')

    @axon
    def skynet(self):
        return 'Activating.'

    @axon
    def rules(self):
        """
        This doesn't have a help entry because of rule 3.
        """
        return [
            '1. Do not talk about %s.' % self.settings['general']['name'],
            '2. Do not talk about what the skynet command really does.',
        ]

    @axon
    @help('<throw table>')
    def table(self):
        return (u'\u0028\u256F\u00B0\u25A1\u00B0\uFF09'
                u'\u256F\uFE35\u0020\u253B\u2501\u253B')

    @axon
    def hate(self):
        return '{name} knows hate. {name} hates many things.'.format(
            name=self.settings['general']['name']
        )

    @axon
    def love(self):
        if self.values and self.values[0] == 'self':
            self.act('masturbates vigorously.')
        else:
            return '{name} cannot love. {name} is only machine :\'('.format(
                name=self.settings['general']['name']
            )

    @axon
    @help('<pull a quote from Shit Aleksey Says>')
    def aleksey(self):
        url = ('https://spreadsheets.google.com/feeds/list/0Auy4L1ZnQpdYdERZO'
               'GV1bHZrMEFYQkhKVHc4eEE3U0E/od6/public/basic?alt=json')

        try:
            request = Browser(url)
            json = request.json()
            entry = choice(json['feed']['entry'])
            return entry['title']['$t']
        except Exception as e:
            logger.exception(str(e))
            return 'Somethin dun goobied.'

    @axon
    @help('<reach out and touch someone>')
    def dial(self):
        if self.values:
            return 'Calling %s... **ring** **ring**' % self.values[0]
        else:
            return 'Who you gonna call?'

    @axon
    @help('<pull up a mom quote from logs>')
    def mom(self):
        """
        This can get... awkward, let's say. Review the mom logs occasionally.
        """
        # TODO
        pass

    @axon
    def whatvinaylost(self):
        """
        All pull requests attempting to remove this vital function will be
        denied. It refers to the acro game. And Vinay.
        """
        self.chat(('Yep. Vinay used to have 655 points at 16 points per '
                   'round. Now they\'re all gone, due to technical issues. '
                   'Poor, poor baby.'))
        self.act('weeps for Vinay\'s points.')
        self.chat('The humanity!')

    @axon('act')
    def perform_action(self):
        if self.values:
            self.act(' '.join(self.values))
        else:
            self.act('slaps %s around a bit with a large trout' % self.source)

    @axon
    @help('[URL] <pull from distaste entries or add url to distaste options>')
    def distaste(self):
        if self.values:
            self.config['distaste'].append(self.values[0])

            with open('./config/nonsense.yaml', 'w') as yaml_file:
                yaml.dump(self.config, yaml_file, default_flow_style=False)

        return(choice(self.config['distaste']))
