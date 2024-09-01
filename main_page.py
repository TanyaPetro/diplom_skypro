from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import json


class MainPage:
    url = 'https://www.kinopoisk.ru/'

    def __init__(self, driver: object):
        self.driver = driver

    @allure.step("Открытие страницы в Chrome")
    def open(self):
        self.driver.get(self.url)

    @allure.step("Получить логин и пароль")
    def get_creds(self) -> dict:
        with open('creds.json', 'r') as creds_file:
            creds = json.load(creds_file)
        return creds

    @allure.step("Логин")
    def login(self, positive: bool):

        show = WebDriverWait(self.driver, 10)
        login = self.get_creds()["login"]
        if positive:
            password = self.get_creds()["password"]
        else:
            password = 'WrongPassword'

        show.until(
            EC.element_to_be_clickable((
            By.XPATH, "//button[text()='Войти']"))
            ).click()

        show.until(
            EC.element_to_be_clickable((
                By.XPATH, "//input[contains(@id, 'passp-field-login')]"))
            ).send_keys(login)

        self.driver.find_element(
            By.XPATH, "//button[contains(@id, 'passp:sign-in')]"
            ).click()

        show.until(
            EC.element_to_be_clickable((
                By.XPATH, "//input[contains(@id, 'passp-field-passwd')]"))
            ).send_keys(password)

        self.driver.find_element(
            By.XPATH, "//button[contains(@id, 'passp:sign-in')]"
            ).click()

        if positive:
            show.until(EC.presence_of_element_located((
                By.XPATH, "//*[@id='__next']/div[1]/div[1]/header/div/div[3]\
/div/div[3]/nav/div[2]/div/a/div/p[1]")))
        else:
            show.until(EC.presence_of_element_located((
                By.XPATH, "//div[contains(@id, 'field:input-passwd:hint')]")))

    @allure.step("Получение имени пользователя")
    def get_user_name(self) -> str:
        return self.driver.find_element(
            By.XPATH, "//*[@id='__next']/div[1]/div[1]/header/div/div[3]/div/\
div[3]/nav/div[2]/div/a/div/p[1]").get_attribute("textContent")

    @allure.step("Поиск по названию")
    def search_by_name(self):
        show = WebDriverWait(self.driver, 10)

        show.until(
            EC.element_to_be_clickable((
                By.XPATH, "//input[contains(@name, 'kp_query')]"))
            ).send_keys('Гарри Поттер и философский камень')

        self.driver.find_element(
            By.XPATH, "//button[contains(@aria-label, 'Найти')]"
            ).click()

    @allure.step("Получение названия фильма")
    def get_film_name(self) -> str:
        return self.driver.find_element(
            By.XPATH,
            "//*[@itemprop='name']/span").get_attribute("textContent")

    @allure.step("Расширенный поиск")
    def full_search(self):
        show = WebDriverWait(self.driver, 10)

        show.until(
            EC.element_to_be_clickable((
                By.XPATH, "//a[contains(@aria-label, 'Расширенный поиск')]"))
            ).click()

        show.until(
            EC.element_to_be_clickable((
                By.XPATH, "//input[contains(@id, 'find_film')]"))
            ).send_keys('Гарри Поттер')

        self.driver.find_element(
            By.XPATH, "//input[contains(@id, 'year')]"
            ).send_keys('2004')

        self.driver.find_element(
            By.XPATH, "//input[contains(@value, 'поиск')]"
            ).click()

    @allure.step("Поиск случайного фильма")
    def random_search(self):
        show = WebDriverWait(self.driver, 10)

        show.until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@aria-label, 'Найти')]"))
            ).click()

        show.until(
            EC.element_to_be_clickable((
                By.XPATH, "//div[contains(@id, 'genreListTitle')]"))
            ).click()

        show.until(
            EC.element_to_be_clickable((
                By.XPATH, "//input[contains(@data-name, 'аниме')]"))
            ).click()

        self.driver.find_element(
            By.XPATH, "//div[contains(@id, 'countryListTitle')]"
            ).click()

        show.until(
            EC.element_to_be_clickable((
                By.XPATH, "//input[contains(@data-name, 'Япония')]"))
            ).click()

        show.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#search"))
            ).click()
        self.driver.find_element(By.CSS_SELECTOR, "#search").send_keys("\n")

        show.until(
            EC.element_to_be_clickable((
                By.XPATH, "//div[contains(@class, 'filmName')]/a"))
            ).click()

        show.until(
            EC.visibility_of_element_located((
                By.XPATH, "//div[contains(@data-test-id, \
'encyclopedic-table')]"))
            )

    @allure.step("Получение страны фильма")
    def get_film_country(self) -> str:
        return (self.driver.find_element(
            By.XPATH, "//div[contains(@data-test-id, \
'encyclopedic-table')]/div[2]/div[2]/a"
            ).get_attribute("textContent"))

    @allure.step("Получение жанра фильма")
    def get_film_genre(self) -> str:
        if self.driver.find_element(
            By.XPATH, "//div[contains(@data-test-id, \
'encyclopedic-table')]/div[3]/div[2]/a[1]"
        ).get_attribute("textContent") == 'слова':
            return (self.driver.find_element(
                By.XPATH, "//div[contains(@data-test-id, \
'encyclopedic-table')]/div[3]/div[2]/div/a[1]"
                ).get_attribute("textContent"))
        else:
            return (self.driver.find_element(
                By.XPATH, "//div[contains(@data-test-id, \
'encyclopedic-table')]/div[3]/div[2]/a[1]"
                ).get_attribute("textContent"))

    @allure.step("Получение текста ошибки")
    def get_warning_text(self) -> str:
        return (self.driver.find_element(
            By.XPATH, "//div[contains(@id, 'field:input-passwd:hint')]"
            ).get_attribute("textContent"))

    @allure.step("Получение цвета текста ошибки")
    def get_warning_text_color(self) -> str:
        return (self.driver.find_element(
            By.XPATH, "//div[contains(@id, 'field:input-passwd:hint')]"
            ).value_of_css_property("color"))
