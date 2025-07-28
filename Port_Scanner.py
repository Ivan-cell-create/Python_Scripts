import socket
import threading
import queue #модуль для безопасной очереди между потоками
from tqdm import tqdm #для прогресс-бара

host = input("Введите IP или домен для сканирования: ")

try:
    host_ip = socket.gethostbyname(host)
except socket.gaierror:
    print("[-] Не удалось разрешить имя хоста. Проверь IP/домен.")
    exit()

start_port = 1
end_port = 65535

port_queue = queue.Queue()
open_ports = []
port_list = list(range(start_port, end_port + 1))
progress = tqdm(total=len(port_list), desc="Сканирование", ncols=80)

def scan_port():
    while not port_queue.empty():
        port = port_queue.get()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host_ip, port))
            if result == 0:
                print(f"[+] Port {port} is OPEN")
                open_ports.append(port)
            sock.close()
        except:
            pass
        progress.update(1)
        port_queue.task_done()

for port in port_list:
    port_queue.put(port)

thread_count = 100
threads = []

for _ in range(thread_count):
    t = threading.Thread(target=scan_port)
    t.daemon = True
    t.start()
    threads.append(t)

port_queue.join()
progress.close()

with open("open_ports.txt", "w") as f:
    f.write(f"Сканирование хоста: {host} ({host_ip})\n")
    f.write("Открытые порты:\n")
    for port in open_ports:
        f.write(f"{port}\n")

print("\n[✓] Сканирование завершено.")
print(f"[+] Открытые порты сохранены в файл open_ports.txt")

port_queue.join()

print("\n[✓] Сканирование завершено.")
print(f"[+] Открытые порты: {open_ports}")  