# Эндпоинт главной страницы 
BASE_URL = "https://stellarburgers.education-services.ru"

# GET Эндпоинт получения данных об ингридиентах
INGREDIENTS = f"{BASE_URL}/api/ingredients"

# POST Эндпоинт для создания пользователя               
AUTH_REGISTER = f"{BASE_URL}/api/auth/register" 

# POST Эндпоинт для авторизации          
AUTH_LOGIN = f"{BASE_URL}/api/auth/login"

# GET Эндпоинт получения данных о пользователе           
DATA_USER = f"{BASE_URL}/api/auth/user"

# DELETE Эндпоинт удаления пользователя
DEL_USER = f"{BASE_URL}/api/auth/user"

# PATCH Эндпоинт обновления данных о пользователе
UPDATE_USER = f"{BASE_URL}/api/auth/user"

# POST Эндпоинт создание заказа      
ORDERS = f"{BASE_URL}/api/orders" 

# GET Эндпоинт для ленты всех заказов        
ORDERS_ALL = f"{BASE_URL}/api/orders/all"     