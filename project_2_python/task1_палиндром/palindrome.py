def is_palindrome(s: str) -> bool:
    """Проверяет, является ли строка палиндромом (игнорирует регистр и неалфавитно-цифровые символы)."""
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]