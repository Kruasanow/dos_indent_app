import socket
import select
import time

def ident_dos(max_conn, req_rate, header_size, total_req, host='localhost', port='8080'):

    res_arr = []
    new_arr = []
    # Максимальное количество соединений, которые можно обработать одновременно
    MAX_CONNECTIONS = max_conn

    # Максимальное количество запросов в секунду от одного IP-адреса
    THRESHOLD_REQUEST_RATE = req_rate

    # Максимальный размер заголовка запроса в байтах
    THRESHOLD_HEADER_SIZE = header_size

    # Максимальное количество запросов в секунду от всех IP-адресов
    THRESHOLD_TOTAL_REQUESTS = total_req

    # Хранилище информации о подключенных клиентах
    connections = {}

    # Хранилище информации о частоте запросов от каждого IP-адреса
    ip_count = {}

    # Счетчик общего количества запросов
    total_requests = 0

    # Очередь для отслеживания последних запросов
    request_queue = []

    # Создаем серверный сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(MAX_CONNECTIONS)

    # Устанавливаем серверный сокет в неблокирующий режим
    server_socket.setblocking(0)

    while len(res_arr) < 1:
        # Получаем список сокетов, готовых к чтению
        read_sockets, _, _ = select.select([server_socket] + list(connections.keys()), [], [])

        for sock in read_sockets:
            # Если серверный сокет готов к чтению, это означает, что поступил новый запрос на подключение
            if sock == server_socket:
                # Принимаем новое подключение
                client_socket, client_address = server_socket.accept()
                new_arr.append(f"Соединение установлено с  {client_address}")
                print(f"New connection from {client_address}")
                
                # Добавляем новое подключение в список активных соединений
                connections[client_socket] = client_address
                
                # Устанавливаем клиентский сокет в неблокирующий режим
                client_socket.setblocking(0)

            # Если клиентский сокет готов к чтению, это означает, что поступил новый запрос на чтение
            else:
                try:
                    # Получаем данные из клиентского сокета
                    data = sock.recv(1024)
                    if data:
                        # Получаем IP-адрес клиента
                        client_address = connections[sock][0]
                        
                        # Обновляем информацию о частоте запросов от этого IP-адреса
                        if client_address in ip_count:
                            ip_count[client_address] += 1
                        else:
                            ip_count[client_address] = 1
                        
                        # Проверяем размер заголовка запроса
                        if len(data) > THRESHOLD_HEADER_SIZE:
                            # Если размер заголовка превышает пороговое значение, заблокируем IP-адрес
                            res_arr.append(f"Blocking {client_address} - Request")
                            print(f"Blocking {client_address} - Request")
                            # Проверяем количество запросов от этого IP-адреса за последнюю секунду
                        current_time = time.time()
                        request_queue.append((client_address, current_time))
                        while request_queue and current_time - request_queue[0][1] > 1:
                            ip_count[request_queue[0][0]] -= 1
                            request_queue.pop(0)
                        
                        # if ip_count[client_address] > THRESHOLD_REQUEST_RATE:
                        #     # Если частота запросов превышает пороговое значение, заблокируем IP-адрес
                        #     print(f"Blocking {client_address} - Request rate too high")
                        if ip_count[client_address] > THRESHOLD_REQUEST_RATE:
                            # Если частота запросов превышает пороговое значение, заблокируем IP-адрес
                            res_arr.append(f"Blocking {client_address} - Request rate too high")
                            print(f"Blocking {client_address} - Request rate too high")
                            sock.send(b"HTTP/1.1 429 Too Many Requests\nContent-Type: text/html\n\n")
                            sock.close()
                            del connections[sock]
                            continue
                        
                            
                        else:
                            # Увеличиваем счетчик общего количества запросов
                            total_requests += 1
                            
                            # Проверяем общее количество запросов в секунду
                            if total_requests > THRESHOLD_TOTAL_REQUESTS:
                                # Если количество запросов превышает пороговое значение, заблокируем все IP-адреса
                                res_arr.append("Blocking all connections - Too many requests")
                                print("Blocking all connections - Too many requests")
                                for conn in connections.keys():
                                    conn.close()
                                    del connections[conn]
                                
                                total_requests = 0
                            
                            else:
                                # Отправляем ответ клиенту
                                sock.send(b"HTTP/1.1 200 OK\nContent-Type: text/html\n\nHello, world!")
                                
                except socket.error:
                    # Если возникает ошибка чтения данных из клиентского сокета, закрываем соединение
                    res_arr.append(f"Соединение закрыто [атака с хоста] -  {connections[sock]}")
                    print(f"Соединение закрыто [атака с хоста] -  {connections[sock]}")
                    sock.close()
                    del connections[sock]
                    continue

    return [new_arr, res_arr]