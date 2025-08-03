import socket
import threading
import queue
from tqdm import tqdm
from pymongo import MongoClient
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError


#Скрипт создан в рамках практической работы Школы 21 и не предназначен для злонамеренного использования 
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

def check_mongodb(host_ip):
    try:
        client = MongoClient(host=host_ip, port=27017, serverSelectionTimeoutMS=1000)
        dbs = client.list_database_names()
        if dbs:
            print(f"[!!!] MongoDB без пароля найдена на {host_ip}:27017")
            print(f"     Доступные базы данных: {dbs}")
        else:
            print(f"[!] MongoDB найдена, но нет доступных баз данных (или доступ ограничен) на {host_ip}:27017")
    except (OperationFailure, ServerSelectionTimeoutError):
        print(f"[-] MongoDB не найдена или требует пароль на {host_ip}:27017")

def scan_port():
    while not port_queue.empty():
        port = port_queue.get()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host_ip, port))
            if result == 0:
                open_ports.append(port)
                if port == 27017:
                    check_mongodb(host_ip)
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

print("\n[✓] Сканирование завершено.")
if open_ports:
    print(f"[+] Открытые порты: {open_ports}")
else:
    print("[!] Открытых портов не найдено.")
