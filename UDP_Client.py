import socket

target_host = "127.0.0.1"
target_port = 9997

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # AF_INET - IPv4, SOCK_DGRAM - UDP

client.sendto(b"AAABBBCCC", (target_host, target_port))  # Отправка данных на сервер

try:
    data, addr = client.recvfrom(4096)
    print(data.decode())
except ConnectionResetError as e:
    print("Соединение сброшено:", e)
client.close()  # Закрытие сокета