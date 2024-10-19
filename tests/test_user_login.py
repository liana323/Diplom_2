import requests
import allure
from urls import LOGIN_URL

@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Успешный логин под существующим пользователем")
    def test_login_with_valid_credentials(self, register_new_user_and_return_login_password):
        user_data = register_new_user_and_return_login_password
        response = requests.post(LOGIN_URL, json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"
        assert "accessToken" in response.json(), "Токен доступа отсутствует в ответе"

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_invalid_credentials(self):
        payload = {
            "email": "invalid_user@yandex.ru",
            "password": "wrongpassword"
        }
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 401, f"Ожидался код 401, но получен {response.status_code}"
        assert response.json().get("message") == "email or password are incorrect"
