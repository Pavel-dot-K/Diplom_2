import time
import string
import secrets
import allure


@allure.step("Создание уникального Email")
def random_email(length: int = 6, domain: str = "icloud.com", prefix: str = "test") -> str:
    assert length > 0, "length должен быть >= 1"
    assert domain, "domain не может быть пустым"
    alphabet = string.ascii_lowercase + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(length))
    timestamp_ms = int(time.time() * 1000)
    return f"{prefix}_{timestamp_ms}_{random_part}@{domain}"