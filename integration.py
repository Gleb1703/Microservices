import unittest
import psycopg2
from pathlib import Path
import asyncio
import sys

BASE_DIR = Path(__file__).resolve().parent

sys.path.append(str(BASE_DIR / 'movie_service/app'))
sys.path.append(str(BASE_DIR / 'kinopoisk_service/app'))

from movie_service.app.main import service_alive as movie_status
from kinopoisk_service.app.main import service_alive as kinopoisk_status

class TestIntegration(unittest.TestCase):

    def test_database(self):
        try:
            conn = psycopg2.connect(
                dbname='Klyukoyt',
                user='postgres',
                password='password',
                host='localhost',
                port='5432'
            )
            conn.close()
            check = True
        except Exception as e:
            check = False
        self.assertEqual(check, True)

    def test_movie_service_connection(self):
        r = asyncio.run(movie_status())
        self.assertEqual(r, {'message': 'service alive'})

    def test_kinopoisk_service_connection(self):
        r = asyncio.run(kinopoisk_status())
        self.assertEqual(r, {'message': 'service alive'})


if __name__ == '__main__':
    unittest.main()
