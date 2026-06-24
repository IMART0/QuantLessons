import socket
import threading

# Настройки сервера
HOST = '0.0.0.0'  # Слушаем на всех сетевых интерфейсах компьютера
PORT = 9000
clients = []

def handle_client(client_socket, client_address):
    print(f"[+] Новое подключение: {client_address}")
    client_socket.sendall("Добро пожаловать в чат ЛФМШ 'Квант'!\nВведите ваше имя: ".encode('utf-8'))
    try:
        # Первое сообщение от клиента - его имя
        username = client_socket.recv(1024).decode('utf-8').strip()
        welcome_msg = f"\n*** {username} присоединился к чату! ***\n"
        broadcast(welcome_msg, client_socket)
        
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8').strip()
            formatted_msg = f"[{username}]: {message}\n"
            print(f"{client_address} {formatted_msg}", end="")
            broadcast(formatted_msg, client_socket)
    except Exception as e:
        print(f"[-] Ошибка с {client_address}: {e}")
    finally:
        print(f"[-] Отключение: {client_address}")
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode('utf-8'))
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Позволяем повторно использовать порт сразу после перезапуска сервера
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Сервер чата запущен на {HOST}:{PORT}")
    print("[*] Узнайте свой локальный IP-адрес с помощью ipconfig (Windows) или ifconfig (Linux/macOS).")
    print("[*] Сообщите этот IP-адрес ребятам для подключения в их файлах chat.py.")
    
    while True:
        client_sock, client_addr = server.accept()
        clients.append(client_sock)
        thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()