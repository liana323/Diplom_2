import requests
import allure
from urls import REGISTER_URL

@allure.feature("Создание пользователя")
class TestUserRegistration:
    @allure.title("Успешное создание пользователя")
    def test_create_unique_user(self, register_new_user_and_return_login_password):
        user_data = register_new_user_and_return_login_password
        assert user_data["email"] is not None, "Email отсутствует"
        assert user_data["password"] is not None, "Пароль отсутствует"
        assert user_data["name"] is not None, "Имя отсутствует"

    @allure.title("Создание пользователя с существующим email")
    def test_create_existing_user(self, register_new_user_and_return_login_password):
        user_data = register_new_user_and_return_login_password
        response = requests.post(REGISTER_URL, json={
            "email": user_data["email"],
            "password": user_data["password"],
            "name": user_data["name"]
        })
        assert response.status_code == 403, f"Ожидался код 403, но получен {response.status_code}"
        assert response.json().get("message") == "User already exists"

    @allure.title("Создание пользователя без одного обязательного поля")
    def test_create_user_without_required_field(self):
        payload = {
            "password": "password123",
            "name": "TestUser"
        }
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403, f"Ожидался код 403, но получен {response.status_code}"
        assert response.json().get("message") == "Email, password and name are required fields"
