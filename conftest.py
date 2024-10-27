import pytest
import requests
import random
import string
from urls import LOGIN_URL, REGISTER_URL, LOGOUT_URL, INGREDIENTS_URL
def generate_random_string(length=10):
    """Генерация случайной строки указанной длины."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
@pytest.fixture
def register_new_user_and_return_login_password():
    """Регистрация нового пользователя и получение токенов."""
    email = f"user_{generate_random_string(8)}@yandex.ru"
    password = generate_random_string(10)
    name = generate_random_string(6)

    # Регистрация пользователя
    payload = {"email": email, "password": password, "name": name}
    response = requests.post(REGISTER_URL, json=payload)
    assert response.status_code == 200, f"Ошибка регистрации: {response.text}"

    # Логин и получение токенов
    login_response = requests.post(LOGIN_URL, json={"email": email, "password": password})
    assert login_response.status_code == 200, f"Ошибка авторизации: {login_response.text}"
    tokens = login_response.json()
    access_token = tokens["accessToken"]
    refresh_token = tokens["refreshToken"]

    # Возвращаем данные пользователя и токены
    yield {"email": email, "password": password, "name": name,
           "access_token": access_token, "refresh_token": refresh_token}

    # Логаут после завершения тестов
    headers = {"Content-Type": "application/json"}
    logout_response = requests.post(LOGOUT_URL, headers=headers, json={"token": refresh_token})
    assert logout_response.status_code == 200, f"Ошибка выхода: {logout_response.text}"

@pytest.fixture
def auth_token(register_new_user_and_return_login_password):
    """Получение токенов для зарегистрированного пользователя."""
    user_data = register_new_user_and_return_login_password

    # Выполняем логин и получаем accessToken и refreshToken
    response = requests.post(LOGIN_URL, json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert response.status_code == 200, f"Ошибка авторизации: {response.text}"

    tokens = response.json()
    return tokens["accessToken"], tokens["refreshToken"]

@pytest.fixture
def order_user_token(register_new_user_and_return_login_password):
    """Получение access_token для заказов."""
    return register_new_user_and_return_login_password["access_token"]

@pytest.fixture
def valid_ingredients():
    """Получение валидных ингредиентов."""
    headers = {"Accept": "application/json"}
    response = requests.get(INGREDIENTS_URL, headers=headers)
    assert response.status_code == 200, f"Ошибка получения ингредиентов: {response.status_code}"
    data = response.json()
    assert "data" in data, "Ответ не содержит данных об ингредиентах"
    ingredients = [item["_id"] for item in data["data"]]
    return ingredients
