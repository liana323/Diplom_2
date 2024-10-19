import requests
import allure
import time
from urls import USER_URL, REGISTER_URL, LOGIN_URL

@allure.feature("Изменение данных пользователя")
class TestUserUpdate:
    @allure.title("Создание и изменение данных пользователя")
    def test_create_and_update_user_data(self):
        # 1. Создаём нового пользователя
        email = f"user_{self.generate_random_string(8)}@yandex.ru"
        password = self.generate_random_string(10)
        name = self.generate_random_string(6)
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 200, f"Ошибка регистрации: {response.text}"

        # 2. Логинимся и получаем токены
        login_response = requests.post(LOGIN_URL, json={
            "email": email,
            "password": password
        })
        assert login_response.status_code == 200, f"Ошибка авторизации: {login_response.text}"
        access_token = login_response.json().get("accessToken")
        refresh_token = login_response.json().get("refreshToken")
        assert access_token, "Токен доступа не получен"
        assert refresh_token, "Refresh токен не получен"
        headers = {
            "Authorization": f"{access_token}",
            "Content-Type": "application/json"
        }
        # 3. Делаем небольшую паузу для синхронизации
        time.sleep(1)

        # 4. Обновляем данные пользователя
        update_payload = {"name": "UpdatedName"}
        update_response = requests.patch(USER_URL, headers=headers, json=update_payload)
        assert update_response.status_code == 200, f"Ожидался код 200, но получен {update_response.status_code}"
        assert update_response.json().get("user")["name"] == "UpdatedName", "Имя пользователя не обновилось"
    @allure.title("Попытка изменить данные без авторизации")
    def test_update_user_data_without_authorization(self):
        payload = {"name": "NewName"}
        response = requests.patch(USER_URL, json=payload)
        assert response.status_code == 401, f"Ожидался код 401, но получен {response.status_code}"
        assert response.json().get("message") == "You should be authorised", "Сообщение об ошибке некорректное"
    def generate_random_string(self, length=10):
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))