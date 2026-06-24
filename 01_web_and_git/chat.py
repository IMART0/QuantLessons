import socket
import threading

# IP-адрес ноутбука преподавателя (выдается преподавателем на доске)
SERVER_IP = 'localhost'  
PORT = 9000

def receive_messages(client_socket):
    """Функция для постоянного чтения сообщений от сервера в фоновом потоке"""
    while True:
        try:
            # Читаем данные из сокета
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message, end="")
        except Exception as e:
            print(f"\n[-] Ошибка получения данных: {e}")
            break
    print("\n[-] Соединение с сервером разорвано.")

def start_client():
    # 1. Создаем TCP-сокет
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Подключаемся к серверу чата
        client.connect((SERVER_IP, PORT))
        print(f"[+] Успешно подключено к чату {SERVER_IP}:{PORT}")
    except Exception as e:
        print(f"[-] Не удалось подключиться к серверу: {e}")
        return

    # 2. Запускаем фоновый поток для прослушивания входящих сообщений
    # Передаем сокет в качестве аргумента функции receive_messages
    listen_thread = threading.Thread(target=receive_messages, args=(client,))
    listen_thread.daemon = True
    listen_thread.start()

    # 3. Основной цикл программы: считываем ввод пользователя и отправляем на сервер
    print("[+] Вы можете писать сообщения. Для выхода нажмите Ctrl+C.")
    while True:
        try:
            msg = input()
            # Отправляем сообщение на сервер
            client.sendall(msg.encode('utf-8'))
        except (KeyboardInterrupt, EOFError):
            print("\n[+] Выход из чата.")
            break

    # Закрываем соединение
    client.close()

if __name__ == "__main__":
    start_client()