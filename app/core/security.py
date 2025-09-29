def verify_password(plain: str, stored: str) -> bool:
    """Простая проверка пароля без хеширования"""
    return plain == stored