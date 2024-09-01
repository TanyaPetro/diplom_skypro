import requests
import allure
import json


class Api:
    def __init__(self, url: str):
        self.url = url

    @allure.step("Получить токен")
    def get_token(self) -> str:
        with open('creds.json', 'r') as creds_file:
            creds = json.load(creds_file)
            token = creds['token']
        return token

    @allure.step("API. Поиск фильма по id")
    def get_film_by_id(self, id: int) -> dict:
        headers = {}
        headers["X-API-KEY"] = self.get_token()
        resp = requests.get(
            self.url + f'/v1.4/movie/{id}', headers=headers)
        return resp.json()

    @allure.step("API. Поиск по году и типу контента")
    def get_content_by_params(self, page: int, limit: int,
                              content_type: str, year: int) -> dict:
        headers = {}
        headers["X-API-KEY"] = self.get_token()
        resp = requests.get(
            self.url + f'/v1.4/movie?page={page}&limit={limit}\
                &type={content_type}&year={year}', headers=headers)
        return resp.json()

    @allure.step("API. Поиск случайного тайтла из базы")
    def get_random_movie(self) -> dict:
        headers = {}
        headers["X-API-KEY"] = self.get_token()
        resp = requests.get(
            self.url + '/v1.4/movie/random', headers=headers)
        return resp.json()

    @allure.step("API. Поиск фильма с некорректными параметрами")
    def get_movie_with_wrong_year(self, year: int) -> dict:
        headers = {}
        headers["X-API-KEY"] = self.get_token()
        resp = requests.get(
            self.url + f'/v1.4/movie?year={year}', headers=headers)
        return resp.json()

    @allure.step("API. Поиск фильма без авторизации")
    def get_movie_without_token(self, id: int) -> dict:
        headers = {}
        resp = requests.get(
            self.url + f'/v1.4/movie/{id}', headers=headers)
        return resp.json()
