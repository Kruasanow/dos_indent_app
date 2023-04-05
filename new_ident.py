import time
from collections import defaultdict
from scapy.all import *

# Задаем максимальное количество запросов от одного IP адреса
MAX_REQUESTS = 10
# Задаем период времени для анализа запросов
ANALYSIS_PERIOD = 30 # в секундах
# Создаем словарь для хранения количества запросов от каждого IP адреса
ip_requests = defaultdict(int)

def detect_dos_attack(ip_address):
    """
    Функция для обнаружения DoS атаки на основе количества запросов от одного IP адреса.
    Если количество запросов от одного IP адреса превышает заданный порог в течение заданного периода времени,
    функция возвращает True, иначе - False.
    """
    ip_requests[ip_address] += 1
    print(ip_requests[ip_address])
    if ip_requests[ip_address] > MAX_REQUESTS:
        return True
    else:
        # Удаляем IP адрес из словаря после истечения периода анализа
        time.sleep(ANALYSIS_PERIOD)
        ip_requests[ip_address] -= 1
        if ip_requests[ip_address] == 0:
            del ip_requests[ip_address]
        return False

def packet_handler(pkt):
    """
    Функция-обработчик пакетов, перехваченных Scapy.
    """
    if IP in pkt:
        ip_address = pkt[IP].src
        print(ip_address)
        if detect_dos_attack(ip_address):
            print(detect_dos_attack(ip_address))
            print(f"Possible DoS attack from {ip_address}")

sniff(prn=packet_handler)