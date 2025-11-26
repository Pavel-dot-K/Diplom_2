import pytest
import requests
import allure
from endpoints import AUTH_LOGIN as LOGIN


class TestLogin:

    @allure.title("Вход под существующим пользователем")
    def test_existing_user_login(self, new_user_reg_login_del):
        user_data, _ = new_user_reg_login_del
        payload = {"email": user_data["email"], "password": user_data["password"]}

        with allure.step("Отправка запроса на вход"):
            resp = requests.post(LOGIN, json=payload)

        with allure.step("Проверка статуса ответа"):
            assert resp.status_code == 200, (
                f"Ожидали 200 при логине, получили {resp.status_code}: {resp.text}"
            )

        with allure.step("Проверка содержимого ответа"):
            body = resp.json()
            assert body.get("success") is True
            token = body.get("accessToken")
            assert isinstance(token, str)
            assert "Bearer" in token

    @allure.title("Вход с неверным логином или паролем")
    @pytest.mark.parametrize(
        "email,password",
        [
            ("first@icloud.com", "543216qwerty"),
            ("second@icloud.com", "ytrewq543216"),
        ],
    )
    def test_login_with_incorrect_username_or_password(self, email, password):
        payload = {"email": email, "password": password}

        with allure.step(f"Отправка запроса с email={email} и паролем={password}"):
            resp = requests.post(LOGIN, json=payload)

        with allure.step("Проверка статуса ответа"):
            assert resp.status_code == 401, (
                f"Ожидали 401 при неверных данных, получили {resp.status_code}: {resp.text}"
            )

        with allure.step("Проверка содержимого ответа"):
            body = resp.json()
            assert body.get("success") is False
            msg = body.get("message", "")
            assert "incorrect" in msg.lower() or "invalid" in msg.lower()