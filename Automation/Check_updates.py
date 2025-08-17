import subprocess
import json

def get_outdated_packages():
    try:
        result = subprocess.run(
            ['pip', 'list', '--outdated', '--format=json'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        outdated_packages = json.loads(result.stdout)
        return outdated_packages
    except subprocess.CalledProcessError as e:
        print("Ошибка при выполнении команды pip:", e.stderr)
        return []

def print_outdated_packages(packages):
    if not packages:
        print("Все пакеты обновлены")
        return

    print("Найдены устаревшие пакеты:\n")
    for pkg in packages:
        print(f"{pkg['name']}: {pkg['version']} --> {pkg['latest_version']} (PyPI)")

if __name__ == "__main__":
    outdated = get_outdated_packages()
    print_outdated_packages(outdated)
