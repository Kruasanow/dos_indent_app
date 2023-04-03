import time
from collections import defaultdict

# Задаем максимальное количество запросов от одного IP адреса
MAX_REQUESTS = 100
# Задаем период времени для анализа запросов
ANALYSIS_PERIOD = 60 # в секундах
# Создаем словарь для хранения количества запросов от каждого IP адреса
ip_requests = defaultdict(int)

def detect_dos_attack(ip_address):
    """
    Функция для обнаружения DoS атаки на основе количества запросов от одного IP адреса.
    Если количество запросов от одного IP адреса превышает заданный порог в течение заданного периода времени,
    функция возвращает True, иначе - False.
    """
    ip_requests[ip_address] += 1
    if ip_requests[ip_address] > MAX_REQUESTS:
        return True
    else:
        # Удаляем IP адрес из словаря после истечения периода анализа
        time.sleep(ANALYSIS_PERIOD)
        ip_requests[ip_address] -= 1
        if ip_requests[ip_address] == 0:
            del ip_requests[ip_address]
        return False