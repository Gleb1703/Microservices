import requests
import unittest

movie_url = 'http://localhost:8000'
get_movies_url = f'{movie_url}/get_movies'
get_movie_by_id_url = f'{movie_url}/get_movie_by_id'
add_movie_url = f'{movie_url}/add_movie'
delete_movie_url = f'{movie_url}/delete_movie'

kinopoisk_url = 'http://localhost:8001'
get_kinopoisk_movie_by_id_url = f'{kinopoisk_url}/get_movie_by_id'


new_movie = {
    "id": 0,
    "movie_name": "testName",
    "creation_date": "2024-02-29T14:42:44.260037",
    "genre": "testGenre",
    "director": "testDirector"
}

test_movie = {
    "movie_name": "string",
    "creation_date": "2024-02-29T07:00:35.434044",
    "director": "string",
    "id": 2,
    "genre": "string"
}



class TestComponent(unittest.TestCase):

    def test_1_add_movie(self):
        res = requests.post(f"{add_movie_url}", json=new_movie)
        self.assertEqual(res.status_code, 200)

    def test_2_get_movies(self):
        res = requests.get(f"{get_movies_url}").json()
        self.assertTrue(test_movie in res)

    def test_3_find_get_movie_by_id(self):
        res = requests.get(f"{get_movie_by_id_url}?movie_id=2").json()
        self.assertEqual(res, test_movie)

    def test_4_delete_movie(self):
        res = requests.delete(f"{delete_movie_url}?movie_id=0").json()
        self.assertEqual(res, "Success")

    def test_5_kinopoisk_by_id(self):
        res = requests.get(f"{get_kinopoisk_movie_by_id_url}?q=500").json()
        self.assertEqual(res[0]["nameRu"], "Собачий полдень")


if __name__ == '__main__':
    unittest.main()
