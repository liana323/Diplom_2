# Ожидаемые ответы
EXPECTED_REGISTER_USER_EXISTS = {
    "success": False,
    "message": "User already exists"
}

EXPECTED_MISSING_FIELD_RESPONSE = {
    "success": False,
    "message": "Email, password and name are required fields"
}

EXPECTED_UNAUTHORIZED_RESPONSE = {
    "success": False,
    "message": "You should be authorised"
}

# Тестовые данные
USER_DATA = {
    "email": "test-user@yandex.ru",
    "password": "password123",
    "name": "TestUser"
}


# Данные для заказа
VALID_INGREDIENTS = ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]
INVALID_INGREDIENT_HASH = ["invalid_hash"]

# Ожидаемые коды ответов
STATUS_CODE_OK = 200
STATUS_CODE_UNAUTHORIZED = 401
STATUS_CODE_BAD_REQUEST = 400
STATUS_CODE_INTERNAL_SERVER_ERROR = 500

# Ожидаемые сообщения об ошибках
ERROR_MESSAGE_UNAUTHORIZED = "You should be authorised"
ERROR_MESSAGE_MISSING_INGREDIENTS = "Ingredient ids must be provided"