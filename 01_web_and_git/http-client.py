import socket

# Настройки подключения
HOST = 'www.wildberries.ru'
PORT = 80
PATH = ''

# 1. Создаем TCP-сокет
# AF_INET означает IPv4, SOCK_STREAM означает TCP протокол
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Подключаемся к серверу
    client_socket.connect((HOST, PORT))
    print(f"[+] Успешно подключено к {HOST}:{PORT}")

    # 2. Формируем сырой HTTP-запрос по правилам протокола
    # Каждая строка обязательно заканчивается \r\n (CRLF)
    # Запрос обязательно завершается пустой строкой \r\n\r\n
    request = (
        f"GET {PATH} HTTP/1.1\r\n"
        f"Host: {HOST}\r\n"
        f"Connection: close\r\n"
        f"User-Agent: CustomPythonSocketClient/1.0\r\n"
        f"\r\n"
    )

    # 3. Отправляем запрос серверу в байтовом виде
    client_socket.sendall(request.encode('utf-8'))
    print("[+] Запрос успешно отправлен.")

    # 4. Получаем ответ порциями (буфером)
    response = b""
    while True:
        chunk = client_socket.recv(4096)
        if not chunk:
            break  # Сервер закрыл соединение
        response += chunk

    # Декодируем и выводим ответ
    print("\n--- ОТВЕТ СЕРВЕРА ---")
    print(response.decode('utf-8'))

finally:
    # Всегда закрываем сокет после завершения работы
    client_socket.close()
    print("[+] Соединение закрыто.")