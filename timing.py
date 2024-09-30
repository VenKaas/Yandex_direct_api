import time  # для задержки запросов
def timing(timing_func):
    """Подсчет времени выполнения функции get_report"""
    def time_wrapper(*args, **kwargs):
        start_time = time.time()
        result = timing_func(*args, **kwargs)
        end_time = time.time()
        print(f"Время выполнения функции {timing_func.__name__}: {end_time - start_time} секунд")
        return result
    return time_wrapper