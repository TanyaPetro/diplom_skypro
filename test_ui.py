from selenium import webdriver
from main_page import MainPage
import allure


@allure.title("Логин по email")
@allure.description("Проверка входа по email с корректными данными")
@allure.feature("login")
@allure.severity("blocker")
def test_login():
    with allure.step("Открытие главной страницы"):
        driver = webdriver.Chrome()
        main_page = MainPage(driver)
        main_page.open()

    with allure.step("Логин"):
        main_page.login(True)

    with allure.step("Проверка имени пользователя"):
        assert main_page.get_user_name() == 'Гарри Поттер'

    with allure.step("Закрытие страницы"):
        driver.quit()


@allure.title("Поиск фильма по названию")
@allure.description("Проверка поиска фильма по названию с главной страницы")
@allure.feature("search")
@allure.severity("blocker")
def test_search_by_name():
    with allure.step("Открытие главной страницы"):
        driver = webdriver.Chrome()
        main_page = MainPage(driver)
        main_page.open()

    with allure.step("Ввод навзвания в строку поиска"):
        main_page.search_by_name()

    with allure.step("Проверка названия найденного фильма"):
        assert main_page.get_film_name() == 'Гарри Поттер \
и философский камень (2001)'

    with allure.step("Закрытие страницы"):
        driver.quit()


@allure.title("Поиск фильма в расширенном поиске")
@allure.description("Проверка поиска фильма по нескольким параметрам")
@allure.feature("search")
@allure.severity("blocker")
def test_full_search():
    with allure.step("Открытие главной страницы"):
        driver = webdriver.Chrome()
        main_page = MainPage(driver)
        main_page.open()

    with allure.step(
        "Переход на вкладку расширенного поиска и ввод параметров поиска"
    ):
        main_page.full_search()

    with allure.step("Проверка названия найденного фильма"):
        assert main_page.get_film_name() == 'Гарри Поттер \
и узник Азкабана (2004)'

    with allure.step("Закрытие страницы"):
        driver.quit()


@allure.title("Поиск случайного фильма")
@allure.description("Проверка поиска случайного фильма по стране и жанру")
@allure.feature("search")
@allure.severity("blocker")
def test_random_search():
    with allure.step("Открытие главной страницы"):
        driver = webdriver.Chrome()
        main_page = MainPage(driver)
        main_page.open()

    with allure.step(
        "Переход на вкладку случайного поиска и ввод параметров поиска"
    ):
        main_page.random_search()

    with allure.step("Проверка параметров найденного фильма"):
        assert main_page.get_film_genre() == 'аниме'
        assert main_page.get_film_country() == 'Япония'

    with allure.step("Закрытие страницы"):
        driver.quit()


@allure.title("Логин с некорректными данными")
@allure.description("Проверка отображения ошибки при \
вводе некорректного пароля")
@allure.feature("login")
@allure.severity("blocker")
def test_login_with_wrong_password():
    with allure.step("Открытие главной страницы"):
        driver = webdriver.Chrome()
        main_page = MainPage(driver)
        main_page.open()

    with allure.step("Логин"):
        main_page.login(False)

    with allure.step("Проверка текста ошибки"):
        assert main_page.get_warning_text() == 'Неверный пароль'

    with allure.step("Проверка цвета текста ошибки"):
        assert main_page.get_warning_text_color() == 'rgba(255, 0, 0, 1)'

    with allure.step("Закрытие страницы"):
        driver.quit()
