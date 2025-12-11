from typing import Callable, List

def apply_filter(filter_func: Callable[[str], bool], arr: List[str]) -> List[str]:
    """Применяет функцию фильтрации к массиву строк (возвращает новый массив)."""
    return list(filter(filter_func, arr))

if __name__ == "__main__":
    strings = ["hello world", "abc", "test", "apple", "banana", "aardvark", "xyz"]
    
    # Исключить строки с пробелами
    no_spaces = apply_filter(lambda s: ' ' not in s, strings)
    
    # Исключить строки, начинающиеся с "a"
    no_a = apply_filter(lambda s: not s.startswith('a'), strings)
    
    # Исключить строки длиной < 5
    long_strings = apply_filter(lambda s: len(s) >= 5, strings)