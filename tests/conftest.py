import pytest
import requests
from typing import Optional, Tuple, Dict
import allure
from helpers import random_email
from endpoints import AUTH_REGISTER as REGISTER, AUTH_LOGIN as LOGIN, DEL_USER, INGREDIENTS


@pytest.fixture(scope="function")
def new_user_reg_login_del() -> Tuple[Dict[str, str], Optional[str]]:
    email = random_email()
    user_data: Dict[str, str] = {
        "email": email,
        "password": "qwerty543216",
        "name": "TestTestOFF"
    }

    with allure.step("Регистрация нового пользователя"):
        resp = requests.post(REGISTER, json=user_data)
        assert resp.status_code in (200, 201, 403), (
            f"Ошибка регистрации: {resp.status_code} {resp.text}"
        )

    with allure.step("Авторизация нового пользователя"):
        login_resp = requests.post(LOGIN, json={"email": email, "password": user_data["password"]})
        token: Optional[str] = None
        if login_resp.status_code == 200:
            token = login_resp.json().get("accessToken")
            if token:
                token = token if token.startswith("Bearer ") else f"Bearer {token}"
    yield user_data, token
    
    with allure.step("Удаление тестового пользователя"):
        if token:
            try:
                requests.delete(DEL_USER, headers={"Authorization": token})
            except Exception:
                pass


@pytest.fixture
def header_auth(new_user_reg_login_del: Tuple[Dict[str, str], Optional[str]]):
    with allure.step("Формирование заголовков авторизации"):
        _, token = new_user_reg_login_del
        return {"Authorization": token} if token else {}


@pytest.fixture(scope="session")
def ingredient_ids():
    with allure.step("Получение id ингредиентов"):
        resp = requests.get(INGREDIENTS)
        assert resp.status_code == 200, f"/ingredients вернул {resp.status_code}: {resp.text}"
        data = resp.json()
        ids = [item.get("_id") for item in data.get("data", []) if item.get("_id")]
        assert len(ids) >= 2, "Сервис вернул недостаточно ингредиентов (ожидали >= 2)"
        return ids