import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

client_address = '127.0.0.1'

# Отправляем несколько запросов с большой частотой
for i in range(10):
    client_socket.send(b'GET / HTTP/1.1\nHost: localhost\n\n')
    print(f"Request {i} sent from {client_address}")
    time.sleep(0.5)

client_socket.close()