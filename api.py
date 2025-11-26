import requests
import allure
from typing import Optional, List
from endpoints import REGISTER, LOGIN, USER, ORDERS
from data import PASSWORD_DATA, NAME_DATA
from helpers import random_email


class StellarApi:


    @allure.step("Инициализируем класс StellarApi")
    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()
        self.token: Optional[str] = None


    @allure.step("Регистрация нового пользователя")
    def register(self, email: Optional[str] = None, password: Optional[str] = None, name: Optional[str] = None) -> requests.Response:
        email = random_email() if email is None else email
        password = PASSWORD_DATA if password is None else password
        name = NAME_DATA if name is None else name
        payload = {"email": email, "password": password, "name": name}
        response = self.session.post(REGISTER, json=payload)
        try:
            data = response.json()
            self.token = data.get("accessToken")
        except ValueError:
            self.token = None
        return response


    @allure.step("Авторизация пользователя")
    def login(self, email: str, password: str) -> requests.Response:
        response = self.session.post(LOGIN, json={"email": email, "password": password})
        try:
            data = response.json()
            self.token = data.get("accessToken")
        except ValueError:
            self.token = None
        return response


    @allure.step("Получение данных авторизованного пользователя")
    def get_user(self) -> requests.Response:
        headers = {"Authorization": self.token} if self.token else {}
        return self.session.get(USER, headers=headers)


    @allure.step("Создаем новый заказа")
    def create_order(self, ingredients: List[str]) -> requests.Response:
        headers = {"Authorization": self.token} if self.token else {}
        payload = {"ingredients": ingredients}
        return self.session.post(ORDERS, headers=headers, json=payload)