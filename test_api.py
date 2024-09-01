from Kinopoisk_API import Api
import allure


url = "https://api.kinopoisk.dev"
api = Api(url)


@allure.title("Поиск фильма по id")
@allure.description("Проверка поиска фильма по id с помощью api")
@allure.feature("search")
@allure.severity("blocker")
def test_search_film_by_id():
    with allure.step("Получение фильма по id"):
        film = api.get_film_by_id(12258)
    with allure.step("Проверка, что получен фильм, соответсвующий id"):
        assert film["name"] == "Игры дьявола"


@allure.title("Расширенный поиск по параметрам")
@allure.description("Проверка поиска контента с различными фильтрами")
@allure.feature("search")
@allure.severity("blocker")
def test_search_content_by_params():
    with allure.step("Поиск по году и типу контента"):
        content = api.get_content_by_params(1, 10, "movie", 2020)
        print(content)
    with allure.step("Проверка, что получен корректный список фильмов"):
        assert content["page"] == 1
        assert content["limit"] == 10
        assert len(content["docs"]) == 10
        for elem in content["docs"]:
            assert (elem["year"]) == 2020
            assert (elem["type"]) == "movie"


@allure.title("Поиск случайного тайтла из базы")
@allure.description("Проверка поиска случайного фильма")
@allure.feature("search")
@allure.severity("blocker")
def test_random_search():
    with allure.step("Получение случайного фильма"):
        random_movie = api.get_random_movie()
    with allure.step("Проверка, что получен фильм"):
        assert len(random_movie) > 1
        assert random_movie["id"] > 0
        assert random_movie["name"] != ""


@allure.title("Поиск фильма с некорректными параметрами")
@allure.description("Проверка поиска фильма с невозможным годом создания")
@allure.feature("search")
@allure.severity("blocker")
def test_search_with_wrong_year():
    with allure.step("Получение фильма с годом, ранее 1874"):
        result = api.get_movie_with_wrong_year(1242)
    with allure.step("Проверка, что возвращается корректная ошибка"):
        assert result["statusCode"] == 400
        assert result["message"][0] == "Значение поля year \
должно быть в диапазоне от 1874 до 2050!"


@allure.title("Поиск фильма по id без авторизации")
@allure.description("Проверка поиска фильма без указания токена")
@allure.feature("search")
@allure.severity("blocker")
def test_search_movie_without_token():
    with allure.step("Получение фильма по id без токена"):
        result = api.get_movie_without_token(12258)
    with allure.step("Проверка, что возвращается корректная ошибка"):
        assert result["statusCode"] == 401
        assert result["message"] == "В запросе не указан токен!"
