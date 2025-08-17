import psutil
import subprocess
import time

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Ошибка: ввод не должен быть пустым. Попробуйте ещё раз.")

def get_int_input(prompt, default):
    while True:
        value = input(prompt).strip()
        if not value:
            return default
        if value.isdigit() and int(value) > 0:
            return int(value)
        else:
            print("Ошибка: введите положительное целое число или оставьте пустым для значения по умолчанию.")

def is_process_running(name):
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if name in proc.info['name'] or (proc.info['cmdline'] and name in proc.info['cmdline'][0]):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def start_process(cmd):
    print(f"Запуск процесса: {' '.join(cmd)}")
    subprocess.Popen(cmd)

def main():
    process_name = get_non_empty_input("Введите имя процесса для мониторинга: ")

    start_command_input = input(
        "Введите команду запуска процесса (через пробел, например: python my_script.py), или оставьте пустым, если не хотите запускать процесс автоматически: "
    ).strip()

    if start_command_input:
        start_command = start_command_input.split()
    else:
        start_command = None

    check_interval = get_int_input("Введите интервал проверки в секундах (по умолчанию 30): ", 30)

    print(f"\nМониторим процесс '{process_name}' каждые {check_interval} секунд...")

    while True:
        running = is_process_running(process_name)
        if not running:
            print(f"Процесс '{process_name}' не найден.")
            if start_command:
                print("Запускаем процесс заново.")
                start_process(start_command)
            else:
                print("Команда запуска не задана, пропускаем запуск.")
        else:
            print(f"Процесс '{process_name}' запущен.")
        time.sleep(check_interval)

if __name__ == "__main__":
    main()
