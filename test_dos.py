import socket
import time
from real_ident_ddos import get_file, get_dname_from_db
import datetime
import matplotlib.pyplot as plt
import pyshark

# a = get_file(get_dname_from_db())


a = pyshark.FileCapture('petr.pcapng')
print(a)

def get_time(dump):
    # Инициализируем переменные min_time и max_time значением None
    min_time = 0
    max_time = 0

    # Проходим по всем пакетам в файле
    for packet in a:
        # Получаем значение поля "frame.time_epoch" для текущего пакета
        time_epoch = float(packet.frame_info.time_epoch)
        
        # Обновляем переменные min_time и max_time, если это необходимо
        if min_time == 0 or time_epoch < min_time:
            min_time = time_epoch
        if max_time == 0 or time_epoch > max_time:
            max_time = time_epoch

    # Вычисляем разницу между максимальным и минимальным временем в секундах
    time_diff = max_time - min_time
    print(time_diff)
    # Выводим результат
    print(f"Время между первым и последним пакетом в файле: {time_diff:.6f} секунд")
    return time_diff

get_time(a)