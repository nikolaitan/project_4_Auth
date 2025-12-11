import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Время выполнения {func.__name__}: {end - start:.6f} сек")
        return result
    return wrapper

@timing_decorator
def add_and_print(a: float, b: float):
    result = a + b
    print(f"Результат: {result}")
    return result

@timing_decorator
def process_files(input_file="input.txt", output_file="output.txt"):
    try:
        with open(input_file, 'r') as f:
            a, b = map(float, f.read().split())
        result = a + b
        with open(output_file, 'w') as f:
            f.write(str(result))
        return result
    except Exception as e:
        print(f"Ошибка: {e}")
        return None