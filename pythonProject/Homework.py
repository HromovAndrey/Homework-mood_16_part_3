# Завдання: Створення Простої Системи Чату з
# Використанням Мікросервісів server.py та client.py.
# Опис:
# Розробіть просту систему чату, яка складається з двох
# мікросервісів: сервера (`server.py`) та клієнта (`client.py`).
# Використовуйте Redis для зберігання повідомлень і статусів
# користувачів.
# Функціональність:
# 1. Сервер (server.py):
# - Встановлення з'єднання з Redis.
# - Очікування повідомлень від клієнтів.
# - Зберігання повідомлень у Redis.
# - Відправлення повідомлень іншим клієнтам.
# 2. Клієнт (client.py):
# - Підключення до сервера.
# - Відправлення повідомлень через сервер.
# - Отримання повідомлень від сервера.
# 1
# Домашнє завдання
# Технічні Вимоги:
# 1. Python:
# - Використання Python для написання server.py та client.py.
# - Використання бібліотеки redis-py для взаємодії з Redis.
# 2. Redis:
# - Використання Redis як брокера повідомлень.
# 3. Комунікація:
# - Використання TCP/IP для комунікації між сервером та
# клієнтами.
# Реалізація:
# 1. server.py:
# - Відкриття серверного сокета.
# - Прийняття вхідних підключень від клієнтів.
# - Читання повідомлень від клієнтів та зберігання їх у Redis.
# - Розсилка повідомлень від одного клієнта іншим
# підключеним клієнтам.
# 2. client.py:
# - Підключення до сервера.
# - Відправлення повідомлень до сервера.
# - Отримання та відображення повідомлень від сервера.
# 2
# Домашнє завдання
# Інструкції:
# - Слід зосередитись на основній логіці комунікації та
# обміну повідомленнями.
# - Важливо протестувати взаємодію між клієнтом та
# сервером, а також відповідне зберігання повідомлень у
# Redis.
# Результат:
# Це завдання дозволить вам розібратися з основами
# мережевого програмування, взаємодією з Redis, та
# розробкою простих мікросервісів на Python.
import socket
import threading
import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)

clients = []

def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received message from {address}: {message}")
                r.rpush('chat_messages', message)
                broadcast(message, client_socket)
        except Exception as e:
            print(f"Error: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)
                client.close()

def start_server():
    print("Server is listening on port 12345...")
    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        print(f"Accepted connection from {address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
