# -*- coding: utf-8 -*-
import gevent
import threading
import time

import multiprocessing as mp
# from multiprocessing import Process
from MongoBot.cortex import Cortex
from MongoBot.dendrite import Dendrite


class Butler(object):
    """
    Because where would Batman be without Alfred? Without tea, that's fucking
    where.

    Here, the butler handles threading of all incoming parsing.
    """
    maxtasks = 8
    semaphore = False

    procs = []

    def __init__(self):
        self.semaphore = threading.BoundedSemaphore(self.maxtasks)

    def wrap(self, func, args, semaphore, note, pid):
        func(args)
        semaphore.release()

    def do(self, func, args, note=False):
        pid = 'task=%s' % time.time()
        self.semaphore.acquire()
        thread = threading.Thread(
            target=self.wrap,
            args=(func, args, self.semaphore, note, pid)
        )
        thread.start()

    def do_fail(self, func, args, note=False):
        pool = mp.Pool(processes=1)

        def run(args):
            func(args)

        result = pool.apply_async(run, args=(args, ))
        try:
            result.get(timeout=10)
        except mp.TimeoutError:
            env = Dendrite(args, [], Cortex.thalamus)
            env.chat('`%s` make head hurt... giving up.' % args.get('data'))
            pool.terminate()
            return
        else:
            pool.close()
            pool.join()
            return

    def do_blah(self, func, args, note=False):
        result = gevent.spawn(func, args)

        try:
            result.get(timeout=10)
        except:
            env = Dendrite(args, [], Cortex.thalamus)
            env.chat('`%s` make head hurt... giving up.' % args.get('data'))
        else:
            result.terminate()
            result.join()

    def do_test(self, func, args, note=False):
        print(args)
        timeout = 10
        start = time.time()
        proc = mp.Process(target=func, args=(args,))
        proc.start()

        while time.time() - start <= timeout:
            if proc.is_alive():
                gevent.sleep(.1)
            else:
                break
        else:
            env = Dendrite(args, [], Cortex.thalamus)
            print(env)
            env.chat('`%s` make head hurt... giving up.' % args.get('data'))
            print('timed out, killing process')
            proc.terminate()
            proc.join()

        # pid = 'task-%s' % time.time()
        # self.semaphore.acquire()
        # thread = threading.Thread(
        #    target=self.wrap,
        #    args=(func, args, self.semaphore, note, pid)
        # )
        # thread.start()
