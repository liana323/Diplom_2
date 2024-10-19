import requests
import allure
from urls import ORDER_URL, ALL_ORDERS_URL
from data import STATUS_CODE_OK, STATUS_CODE_UNAUTHORIZED

@allure.feature("Получение заказов")
class TestGetOrders:
    @allure.title("Получение заказов c авторизации")
    def test_get_all_orders_with_authorization(self, order_user_token, valid_ingredients):
        access_token = order_user_token
        headers = {
            "Authorization": "{access_token}",
            "Content-Type": "application/json"
        }
        data = {"ingredients": valid_ingredients[:1]}
        response = requests.post(ORDER_URL, headers=headers, json=data)
        # Делаем запрос на получение заказов
        response = requests.get(ALL_ORDERS_URL)
        # Проверяем успешность запроса
        assert response.status_code == STATUS_CODE_OK, (f"Ожидался код {STATUS_CODE_OK}, но получен {response.status_code}")

        # Проверяем, что в ответе содержатся заказы
        response_data = response.json()
        assert response_data.get("success"), "Запрос завершился неудачно"
        assert len(response_data.get("orders", [])) > 0, "Ожидался хотя бы один заказ"

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized_user(self):
        headers = {"Content-Type": "application/json"}
        response = requests.get(ORDER_URL, headers=headers)
        assert response.status_code == STATUS_CODE_UNAUTHORIZED, (
            f"Ожидался код {STATUS_CODE_UNAUTHORIZED}, но получен {response.status_code}")
        assert response.json().get("message") == "You should be authorised"
