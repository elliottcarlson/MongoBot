import unittest

from service import SQLService

class DBMock(object):
    def __init__(self, cursor):
        self.cursor = cursor

    def cursor(self):
        return self.cursor

class DBCursorMock(object):
    def __init__(self, data, error=None):
        self.data = data
        self.error = error

    def executescript(self, sql):
        if error is not None:
            raise error

    def execute(self, sql):
        if error is not None:
            raise error

    def fetchall(self):
        if error is not None:
            raise error
        return self.data

class SQLServiceTest(unittest.TestCase):
    def test_execute(self):
        cursor = DBCursorMock([])
        db = DBMock(cursor)
        service = SQLService(db)
        output = service.execute("fixtures", "code", "tests")
        expected = {
            "failures": [],
            "errors": [],
            "success": True
        }

        self.assertEqual(output, expected)
