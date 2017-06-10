# -*- coding: utf-8 -*-

import logging
from pyparsing import alphanums, printables, Dict, Group, LineEnd, Literal, \
        OneOrMore, Optional, ParseException, Suppress, Word, WordEnd

logger = logging.getLogger(__name__)


class Wernicke(object):
    """
    Wernicke's area is one of the two parts of the cerebral cortex linked to
    speech.It is involved in the comprehension or understanding of written and
    spoken language.

    Wernicke is responsible for parsing input received from the Thalamus and
    break it down in to comprehensible commands that Mongo can understand.
    """

    def __init__(self):
        """
        Mongo EBNF for command comprehension and sequencing

        Allows syntax of:

            .command [...]
            :command [...]
            .command [...] | :command [...] | .command [...]
        """
        point = Literal('.')
        colon = Literal(':')
        prefix = point | colon
        pipe = Suppress(Optional(Literal('|')))
        eoc = WordEnd() | LineEnd()
        command = Group(prefix + Word(alphanums)) + eoc
        parameter = Word(printables, excludeChars='|')
        parameters = Optional(Group(OneOrMore(parameter)))
        command_group = Group(command + parameters) + pipe
        command_line = Dict(OneOrMore(command_group))

        self.EBNF = command_line

    def parse(self, line):

        try:
            parsed = self.EBNF.parseString(line)

            logger.debug('Parsed incoming:')
            logger.debug('  In: %s', line)
            logger.debug('  Out: %s', parsed.asList())

            return parsed.asList()

        except ParseException:

            return