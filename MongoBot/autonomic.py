# -*- coding: utf-8 -*-

import logging
import re
from MongoBot.utils import yo_dawg
from MongoBot.corpuscallosum import CorpusCallosum

logger = logging.getLogger(__name__)


@yo_dawg
def axon(func, *args, **kwargs):

    func.create_command = True

    cmd = func.__name__
    if args:
        cmd = re.compile(*args)

    logger.info('Registered axon on "%s" as "%s"', func.__name__,
                cmd.pattern if isinstance(cmd, re._pattern_type) else cmd)

    CorpusCallosum.commands[cmd] = func

    return func
