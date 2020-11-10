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
                'pswd': None
            },
            {
                'uri': '192.168.192.41/1',
                'host': '192.168.192.41',
                'port': 6379,
                'db': 1,
                'pswd': None
            },
            {
                'uri': 'user-redis-cluster.example.com:6380',
                'host': 'user-redis-cluster.example.com',
                'port': 6380,
                'db': 0,
                'pswd': None
            },
            {
                'uri': ':123123@user-redis-cluster.example.com:6380/2',
                'host': 'user-redis-cluster.example.com',
                'port': 6380,
                'db': 2,
                'pswd': '123123'
            },
        ]
        for tc in testcases:
            host, port, db, pswd = main.parse_uri(tc['uri'])
            self.assertEqual(host, tc['host'])
            self.assertEqual(port, tc['port'])
            self.assertEqual(db, tc['db'])
            self.assertEqual(pswd, tc['pswd'])


if __name__ == '__main__':
    unittest.main()
