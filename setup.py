from os.path import join, dirname
from setuptools import setup, find_packages

__version__ = open(join(dirname(__file__), 'MongoBot/VERSION')).read().strip()

install_requires = (
) # yapf: disable

excludes = (
    '*test*',
    '*local_settings*',
) # yapf: disable

setup(name='MongoBot',
      version=__version__,
      license='MIT',
      description=('IRC bot for screwing around. Named not for MongoDB, but '
          'after Mongo from Blazing Saddles.'),
      author='Hunt Welch',
      url='https://github.com/huntwelch/MongoBot/',
      platforms=['Any'],
      packages=fund_packages(exclude=excludes),
      install_requires=install_requires,
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: MIT License',
                   'Operating Sytem :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'])

