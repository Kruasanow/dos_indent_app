import time
from collections import deque
from datetime import datetime, timedelta

# Задайте пороговые значения для факторов, указывающих на DOS-атаку
THRESHOLD_REQUEST_RATE = 100  # Максимальное количество запросов в секунду от одного IP-адреса
THRESHOLD_TOTAL_REQUESTS = 1000  # Максимальное количество запросов в секунду от всех IP-адресов
THRESHOLD_HEADER_SIZE = 2048  # Максимальный размер заголовка запроса в байтах

# Создайте очередь для отслеживания последних запросов
request_queue = deque(maxlen=THRESHOLD_REQUEST_RATE)

# Создайте словарь для отслеживания количества запросов по IP-адресу
ip_count = {}

# Создайте переменную для отслеживания общего количества запросов
total_requests = 0

while True:
    # Получите IP-адрес отправителя запроса и заголовки запроса
    ip_address, headers = get_request_info()

    # Проверьте размер заголовка запроса
    header_size = len(headers)
    if header_size > THRESHOLD_HEADER_SIZE:
        # Если размер заголовка превышает пороговое значение, заблокируйте IP-адрес
        # block_ip_address(ip_address, "Request header too large")
        print('HEADER SIZE EBAT')
        continue

    # Увеличьте счетчик запросов для этого IP-адреса
    if ip_address in ip_count:
        ip_count[ip_address] += 1
    else:
        ip_count[ip_address] = 1

    # Проверьте частоту запросов от этого IP-адреса
    request_time = datetime.now()
    request_queue.append(request_time)
    if len(request_queue) == THRESHOLD_REQUEST_RATE:
        oldest_request_time = request_queue[0]
        elapsed_time = (request_time - oldest_request_time).total_seconds()
        request_rate = len(request_queue) / elapsed_time
        if request_rate > THRESHOLD_REQUEST_RATE:
            # Если частота запросов превышает пороговое значение, заблокируйте IP-адрес
            # block_ip_address(ip_address, "Request rate too high")
            print('4ASTOTA > LIMIT EBAT')
            continue

    # Увеличьте счетчик общего количества запросов
    total_requests += 1

    # Проверьте общее количество запросов
    if total_requests > THRESHOLD_TOTAL_REQUESTS:
        # Если общее количество запросов превышает пороговое значение, заблокируйте все IP-адреса
        for ip in ip_count.keys():
            # block_ip_address(ip, "Total requests threshold exceeded")
            print('REQ > LIMIT EBAT')
        continue

    # Подождите некоторое время
    time.sleep(0.1)