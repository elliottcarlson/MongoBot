# -*- coding: utf-8 -*-
import imp
import inspect
import logging
import os
import pyinotify
import sys
import time

from glob import glob

logger = logging.getLogger(__name__)


class Neuroplasticity(pyinotify.ProcessEvent):
    """
    Neuroplasticity, also known as brain plasticity or neural plasticity, is an
    umbrella term that describes lasting change to the brain throughout an
    individual's life course. Neuroplasticity can be observed at multiple
    scales, from microscopic changes in individual neurons to larger-scale
    changes such as cortical remapping in response to injury.

    In MongoBot, Neuroplasticity handles mapping and hot reloading of the
    brainmeats.
    """

    def __init__(self):
        self.watcher = pyinotify.WatchManager()
        self.notifier = None
        self.modules = {}
        self.meatpath = None
        self.modules_path = 'MongoBot.brainmeats'

        self.brainmeats = {
            'regex': {},
            'named': {}
        }

    def _watch_brainmeat(self, brainmeat, module):
        """
        Monitor the loaded brainmeats for modifications and deletions so we can
        hotswap them meats
        """
        file_name = os.path.realpath(brainmeat)
        self.modules[file_name] = module
        mask = pyinotify.IN_MODIFY | pyinotify.IN_DELETE_SELF
        self.watcher.add_watch(file_name, mask)
        logger.debug('Watching %s', brainmeat)

    def initialize(self):
        """
        Find all the available brainmeats for Mongo.
        """
        fd = None
        path_name = None
        description = None
        modules = []

        for mod in self.modules_path.split('.'):
            if path_name is not None:
                path_name = [path_name]
            (fd, path_name, description) = imp.find_module(mod, path_name)

        self.watcher.add_watch(path_name, pyinotify.IN_CREATE)

        if not path_name.endswith('.py'):
            modules = glob('{}/[!_]*.py'.format(path_name))
            modules = [os.path.split(f)[-1][:-3] for f in modules]

        self.meatpath = path_name

        for module in modules:
            self.load(module)

        self.load_axon()
        self.start()

    def load(self, name):
        """
        Load a brainmeat in to Mongo's brain, and let the neuroplasticity do
        its thing
        """
        if imp.is_builtin(name) != 0:
            return

        (fd, path_name, description) = imp.find_module(name, [self.meatpath])

        try:
            mod = imp.load_module(name, fd, path_name, description)
            if fd:
                self._watch_brainmeat(fd.name, (name, mod))
            else:
                for root, dirs, files in os.walk(path_name):
                    for filename in files:
                        fpath = os.path.join(root, filename)
                        if fpath.endswith('.py'):
                            self._watch_brainmeat(fpath, (name, mod))
        except Exception as e:
            logger.debug('Skipping loading of "%s": %s', name, e)
        finally:
            if fd:
                fd.close()

    def load_axon(self):
        """
        Discover the axon's of the brainmeats so we can live reload the
        available commands that Mongo understands.
        """
        self.brainmeats = {
            'regex': {},
            'named': {}
        }

        for key in self.modules:
            try:
                module_name = self.modules[key][0]
                module = self.modules[key][1]
                logger.info('Loading brainmeat "%s"', module_name)

                cls = getattr(module, module_name.capitalize())
                instance = cls()
                methods = inspect.getmembers(instance)

                for name, m in methods:
                    if not hasattr(m, 'axon'):
                        continue

                    self.brainmeats[m.axon_type][m.axon] = (cls, m.__name__)
            except Exception as e:
                logger.exception('Failed to import "%s": %s', module, e)

    def get(self, command):
        """
        Get a brainmeats axon based on the command passed in
        """
        if command in self.brainmeats['named']:
            return self.brainmeats['named'][command]

        for matcher in self.brainmeats['regex']:
            if matcher.search(command):
                return self.brainmeats['regex'][matcher]

        return None

    def start(self):
        """
        Start watching the brainmeats for changes
        """
        if self.notifier is None:
            self.notifier = pyinotify.ThreadedNotifier(self.watcher, self)
        self.notifier.start()

    def stop(self):
        """
        Stop watching the brainmeats for changes
        """
        if self.notifier is not None:
            self.notifier.stop()

    def process_IN_MODIFY(self, event):
        """
        A brainmeat has been modified - let's do this thang!
        """
        if event.path not in self.modules:
            return

        module = self.modules[event.path]
        self.reload(module)

    def process_IN_CREATE(self, event):
        """
        OMG, new brainmeats!!!
        """
        if not event.name.endswith('.py'):
            return

        module = event.name[:-3]
        self.load(module)
        self.load_axon()

    def process_IN_DELETE_SELF(self, event):
        """
        Drain bamage - repair thyself!
        """
        if event.path not in self.modules:
            return

        del self.modules[event.path]

    def reload(self, module):
        """
        Why doesn't this just use reload()? I'll tell you why. pyinotify and
        reload() have a race condition that will actually corrupt the .pyc
        bytecode output, and then it just fails miserably. You actually have to
        delete the .pyc file if you want the module to work at all after that.
        So yeah - that's why it works this way.
        """
        module_name = module[0]
        module = module[1]

        try:
            del sys.modules[module_name]
        except:
            pass
        time.sleep(1)

        self.load(module_name)
        self.load_axon()
