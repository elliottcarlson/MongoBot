# -*- coding: utf-8 -*-
class MockPraw(object):
    def __init__(self, client_id=None, client_secret=None, user_agent=None):
        if client_id is None:
            raise Exception('No client_id specified.')

        if client_secret is None:
            raise Exception('No client_secret specified.')

        if user_agent is None:
            raise Exception('No user_agent specified.')

    def subreddit(self, subreddit):
        return MockPrawResponse(subreddit)


class MockPrawResponse(object):
    def __init__(self, subreddit):
        self.subreddit = subreddit

    def hot(self, limit=0):
        if self.subreddit is 'spacedicks':
            raise Exception('No one should see /r/spacedicks')
        return [MockPrawResponseEntry(self.subreddit)]


class MockPrawResponseEntry(object):
    def __init__(self, subreddit):
        self.subreddit = MockPrawResponseSubreddit(subreddit)
        self.title = 'This is a test entry.'
        self.shortlink = 'https://redd.it/0abcde'


class MockPrawResponseSubreddit(object):
    def __init__(self, subreddit):
        self.display_name = subreddit
