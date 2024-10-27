import requests
import allure
import time
from urls import USER_URL

@allure.feature("Изменение данных пользователя")
class TestUserUpdate:

    @allure.title("Создание и изменение данных пользователя")
    def test_create_and_update_user_data(self, register_new_user_and_return_login_password):
        # Получаем данные пользователя и токен из фикстуры
        user_data = register_new_user_and_return_login_password
        access_token = user_data["access_token"]

        # Настраиваем заголовки для авторизации
        headers = {
            "Authorization": access_token,  # Токен уже включает "Bearer"
            "Content-Type": "application/json"
        }

        # Небольшая пауза для синхронизации (если требуется)
        time.sleep(1)

        # Обновляем данные пользователя
        update_payload = {"name": "UpdatedName"}
        update_response = requests.patch(USER_URL, headers=headers, json=update_payload)

        # Проверяем успешность обновления данных
        assert update_response.status_code == 200, (
            f"Ожидался код 200, но получен {update_response.status_code}"
        )
        assert update_response.json().get("user")["name"] == "UpdatedName", "Имя пользователя не обновилось"

    @allure.title("Попытка изменить данные без авторизации")
    def test_update_user_data_without_authorization(self):
        # Пытаемся обновить данные без авторизации
        payload = {"name": "NewName"}
        response = requests.patch(USER_URL, json=payload)

        # Проверяем, что запрос не удался без авторизации
        assert response.status_code == 401, f"Ожидался код 401, но получен {response.status_code}"
        assert response.json().get("message") == "You should be authorised", "Сообщение об ошибке некорректное"
