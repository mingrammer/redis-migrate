import unittest

from migrator import main


class TestMain(unittest.TestCase):

    def test_parse_uri(self):
        testcases = [
            {
                'uri': 'localhost',
                'host': 'localhost',
                'port': 6379,
                'db': 0,
                'password': None,
            },
            {
                'uri': '192.168.192.41/1',
                'host': '192.168.192.41',
                'port': 6379,
                'db': 1,
                'password': None,
            },
            {
                'uri': 'user-redis-cluster.example.com:6380',
                'host': 'user-redis-cluster.example.com',
                'port': 6380,
                'db': 0,
                'password': None,
            },
            {
                'uri': 'user-redis-cluster.example.com:6380/2',
                'host': 'user-redis-cluster.example.com',
                'port': 6380,
                'db': 2,
                'password': None,
            },
            {
                'uri': 'user-redis-cluster.example.com:6380/2/123456',
                'host': 'user-redis-cluster.example.com',
                'port': 6380,
                'db': 2,
                'password': '123456',
            },
        ]
        for tc in testcases:
            host, port, db, password = main.parse_uri(tc['uri'])
            self.assertEqual(host, tc['host'])
            self.assertEqual(port, tc['port'])
            self.assertEqual(db, tc['db'])
            self.assertEqual(password, tc['password'])


if __name__ == '__main__':
    unittest.main()
