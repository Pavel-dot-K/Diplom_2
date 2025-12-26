import pytest
import requests
import allure
from endpoints import ORDERS
from typing import List, Dict

class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_order_with_auth_and_ingredients(self, header_auth: Dict[str, str], ingredient_ids: List[str]):
        payload = {"ingredients": ingredient_ids[:2]}
        with allure.step("Отправка POST-запроса на создание заказа"):
            resp = requests.post(ORDERS, json=payload, headers=header_auth)

        with allure.step("Проверка статуса ответа"):
            assert resp.status_code == 200, (
                f"Ожидали 200, получили {resp.status_code}: {resp.text}"
            )

        with allure.step("Проверка успешности ответа и номера заказа"):
            body = resp.json()
            assert body.get("success") is True
            order = body.get("order")
            assert isinstance(order, dict)
            assert order.get("number") is not None

    @allure.title("Создание заказа с ингредиентами без авторизации")
    def test_order_without_auth_with_ingredients(self, ingredient_ids: List[str]):
        payload = {"ingredients": ingredient_ids[:2]}
        with allure.step("Отправка POST-запроса на создание заказа без авторизации"):
            resp = requests.post(ORDERS, json=payload)

        with allure.step("Проверка статуса ответа - ожидаем 401 Unauthorized"):
            assert resp.status_code == 401, (
                f"Ожидали 401, получили {resp.status_code}: {resp.text}" # Правка по комментарию №1
            )

        with allure.step("Проверка сообщения об ошибке авторизации"):
            msg = resp.json().get("message", "").lower()
            assert "author" in msg or "auth" in msg

    @allure.title("Создание заказа без ингредиентов")
    def test_order_with_no_ingredients(self, header_auth: Dict[str, str]):
        payload = {"ingredients": []}
        with allure.step("Отправка POST-запроса с пустым списком ингредиентов"):
            resp = requests.post(ORDERS, json=payload, headers=header_auth)

        with allure.step("Проверка статуса ответа - ожидаем 400 Bad Request"):
            assert resp.status_code == 400, (
                f"Ожидали 400, получили {resp.status_code}: {resp.text}"
            )

        with allure.step("Проверка сообщения об ошибке о необходимости ингредиентов"):
            msg = resp.json().get("message", "").lower()
            assert ("ingredient" in msg and "must" in msg) or "ingredient ids" in msg

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_order_with_invalid_ingredient_hash(self, header_auth: Dict[str, str]):
        payload = {"ingredients": ["NOT_A_VALID_ID"]}
        with allure.step("Отправка POST-запроса с неверным хешем ингредиента"):
            resp = requests.post(ORDERS, json=payload, headers=header_auth)

        with allure.step("Проверка статуса ответа - ожидается 500"):
            assert resp.status_code == 500, (
                f"Ожидали 500, получили {resp.status_code}: {resp.text}" # Правка по комментарию №1
            )

    @allure.title("Создание заказа с неверным токеном")
    def test_order_with_invalid_token(self, ingredient_ids: List[str]):
        payload = {"ingredients": ingredient_ids[:2]}
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        with allure.step("Отправка POST-запроса с неверным токеном"): # Правка по комментарию №2
            resp = requests.post(ORDERS, json=payload, headers=invalid_headers)

        with allure.step("Проверка статуса ответа"):
            assert resp.status_code == 403, (
                f"Ожидали 403, получили {resp.status_code}: {resp.text}" # Правка по комментарию №1
            )