import requests
import allure
from urls import ORDER_URL
from data import STATUS_CODE_OK, STATUS_CODE_BAD_REQUEST

@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_authorization(self, order_user_token, valid_ingredients):
        access_token = order_user_token
        headers = {
            "Authorization":"{access_token}",
            "Content-Type": "application/json"
        }
        data = {"ingredients": valid_ingredients[:1]}
        response = requests.post(ORDER_URL, headers=headers, json=data)
        assert response.status_code == STATUS_CODE_OK, f"Ожидался код {STATUS_CODE_OK}, но получен {response.status_code}"
        assert response.json().get("success"), "Не удалось создать заказ"

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, order_user_token):
        access_token = order_user_token
        headers = {
            "Authorization":"{access_token}",
            "Content-Type": "application/json"
        }
        data = {"ingredients": []}
        response = requests.post(ORDER_URL, headers=headers, json=data)
        assert response.status_code == STATUS_CODE_BAD_REQUEST, f"Ожидался код {STATUS_CODE_BAD_REQUEST}, но получен {response.status_code}"

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self, valid_ingredients):
        headers = {"Content-Type": "application/json"}
        data = {"ingredients": valid_ingredients[:1]}
        response = requests.post(ORDER_URL, headers=headers, json=data)
        assert response.status_code == STATUS_CODE_OK

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self, order_user_token):
        access_token = order_user_token
        headers = {
            "Authorization":"{access_token}",
            "Content-Type": "application/json"
        }
        data = {"ingredients": ["invalid_hash"]}  # Используем невалидный хеш
        response = requests.post(ORDER_URL, headers=headers, json=data)
        assert response.status_code == STATUS_CODE_BAD_REQUEST