import pytest
import requests
import allure
from typing import Dict, Tuple, Optional

from endpoints import AUTH_REGISTER as REGISTER


class TestRegistration:

    @allure.title("Регистрация уникального пользователя")
    def test_register_unique_user(self, new_user_reg_login_del: Tuple[Dict[str, str], Optional[str]]):
        user_data, _ = new_user_reg_login_del
        with allure.step("Отправка запроса на регистрацию нового пользователя"):
            resp = requests.post(REGISTER, json=user_data)

        with allure.step("Проверка, что повторная регистрация возвращает 403"):
            assert resp.status_code == 403, (
                f"Ожидали 403 при повторной регистрации, получили {resp.status_code}: {resp.text}"
            )

        with allure.step("Проверка ответа: status=False и сообщение о том, что пользователь уже существует"):
            body = resp.json()
            assert body.get("success") is False
            assert "already" in body.get("message", "").lower()

    @allure.title("Регистрация существующего пользователя")
    def test_register_existing_user(self, new_user_reg_login_del: Tuple[Dict[str, str], Optional[str]]):
        user_data, _ = new_user_reg_login_del
        with allure.step("Отправка запроса на регистрацию существующего пользователя"):
            resp = requests.post(REGISTER, json=user_data)

        with allure.step("Проверка: повторная регистрация возвращает 403 и сообщение о существующем пользователе"):
            assert resp.status_code == 403, (
                f"Ожидали 403 при повторной регистрации, получили {resp.status_code}: {resp.text}"
            )

        with allure.step("Проверка ответа: status=False и сообщение о уже существующем пользователе"):
            body = resp.json()
            assert body.get("success") is False
            assert "already" in body.get("message", "").lower()

    @allure.title("Регистрация незаполненным обязательным полем")
    @pytest.mark.parametrize("missing", ["email", "password", "name"])
    def test_register_missing_required_field(self, missing: str):
        payload: Dict[str, str] = {
            "email": "test@example.com",
            "password": "qwerty543216",
            "name": "TestName"
        }
        payload.pop(missing)

        with allure.step(f"Отправка запроса на регистрацию без поля: {missing}"):
            resp = requests.post(REGISTER, json=payload)

        with allure.step("Проверка: возвращается 403 и сообщение о требуемом поле"):
            assert resp.status_code == 403, (
                f"Ожидали 403 при пропуске поля {missing}, получили {resp.status_code}: {resp.text}"
            )

        with allure.step("Проверка ответа: status=False и сообщение о необходимости поля"):
            body = resp.json()
            assert body.get("success") is False
            assert "required" in body.get("message", "").lower()