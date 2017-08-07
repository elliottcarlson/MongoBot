# -*- coding: utf-8 -*-
import threading
import time


class Butler(object):
    """
    Because where would Batman be without Alfred? Without tea, that's fucking
    where.

    Here, the butler handles threading of all incoming parsing.
    """
    maxtasks = 8
    semaphore = False

    def __init__(self):
        self.semaphore = threading.BoundedSemaphore(self.maxtasks)

    def wrap(self, func, args, semaphore, note, pid):
        func(args)
        semaphore.release()

    def do(self, func, args, note=False):
        pid = 'task-%s' % time.time()
        self.semaphore.acquire()
        thread = threading.Thread(
            target=self.wrap,
            args=(func, args, self.semaphore, note, pid)
        )
        thread.start()
