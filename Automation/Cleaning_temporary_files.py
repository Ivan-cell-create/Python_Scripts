import os
import shutil
import time
import platform
from pathlib import Path

def get_os_and_temp_paths():
    """
    Определяет операционную систему и возвращает список путей к временным директориям, характерным для этой ОС.

    Возвращает:
    - os_name (str): Название операционной системы, например "Windows", "Linux", "Darwin".
    - temp_paths (list of Path): Список объектов Path, указывающих на директории с временными файлами.

    Логика:
    - Для Windows берутся системные переменные TEMP и TMP, а также стандартные папки временных файлов.
    - Для Linux и macOS (Darwin) задаются стандартные пути к временным директориям.
    """
    os_name = platform.system()  # Получаем название ОС
    temp_paths = []  # Список для хранения путей к временным папкам

    if os_name == "Windows":
        # Получаем значение переменных окружения TEMP или TMP
        temp_env = os.getenv("TEMP") or os.getenv("TMP")
        # Получаем путь к профилю пользователя
        user_profile = os.getenv("USERPROFILE")
        temp_paths = [
            Path(temp_env) if temp_env else None,  # %TEMP% или %TMP%
            Path("C:/Windows/Temp"),                # стандартная системная папка временных файлов
            Path(user_profile) / "AppData/Local/Temp" if user_profile else None  # папка Temp в профиле пользователя
        ]

    elif os_name == "Linux":
        # Стандартные временные директории в Linux
        temp_paths = [
            Path("/tmp"),
            Path("/var/tmp"),
            Path.home() / ".cache"  # кэш пользователя
        ]

    elif os_name == "Darwin":  # macOS
        # Стандартные временные директории macOS
        temp_paths = [
            Path("/tmp"),
            Path("/var/folders"),
            Path.home() / "Library/Caches"
        ]

    # Убираем None из списка, если переменные окружения не заданы
    temp_paths = [p for p in temp_paths if p is not None]

    return os_name, temp_paths


def find_old_items(path: Path, older_than_days=7):
    """
    Поиск файлов и папок в директории `path`, которые старше `older_than_days`.
    
    Параметры:
    - path (Path): Путь к директории для поиска.
    - older_than_days (int): Возраст файла/папки в днях, старше которого будет выбран объект.
    
    Возвращает:
    - items_to_delete (list): Список путей (Path) файлов и папок, подходящих под условие.
    """
    if not path.exists() or not path.is_dir():
        print(f"Путь не найден или не является директорией: {path}")
        return []

    now = time.time()  # текущее время в секундах с эпохи
    items_to_delete = []  # список для хранения файлов и папок, подходящих под условие удаления

    # Рекурсивный обход всех файлов и папок внутри `path`
    for item in path.rglob("*"):
        try:
            # Время последнего изменения файла/папки
            item_age = now - item.stat().st_mtime  
            # Если объект старше заданного количества дней, добавляем в список
            if item_age >= older_than_days * 86400:  
                items_to_delete.append(item)
        except Exception as e:
            print(f"Ошибка при проверке {item}: {e}")

    return items_to_delete


def clean_items(items, dry_run=False):
    """
    Удаление файлов и папок из списка `items`.
    
    Параметры:
    - items (list): Список путей (Path) для удаления.
    - dry_run (bool): Если True, объекты не удаляются, только выводится информация.
    """
    deleted_files = 0  # счетчик удалённых файлов
    deleted_dirs = 0   # счетчик удалённых папок

    for item in items:
        try:
            if item.is_file():
                if not dry_run:
                    item.unlink()  # удаляем файл
                deleted_files += 1
                print(f"Удалён файл: {item}")

            elif item.is_dir():
                if not dry_run:
                    shutil.rmtree(item)  # удаляем папку и все вложенные файлы
                deleted_dirs += 1
                print(f"Удалена папка: {item}")

        except Exception as e:
            print(f"Ошибка при удалении {item}: {e}")

    print(f"Всего удалено файлов: {deleted_files}, папок: {deleted_dirs}")


def ask_confirmation():
    """
    Запрашивает у пользователя подтверждение для продолжения удаления.
    
    Возвращает:
    - True, если пользователь ввел 'y' (да).
    - False во всех остальных случаях.
    """
    answer = input("Удалить перечисленные файлы и папки? (y/n): ").strip().lower()
    return answer == 'y'


if __name__ == "__main__":
    os_name, temp_dirs = get_os_and_temp_paths()  # определяем ОС и пути временных папок
    print(f"Операционная система: {os_name}")

    all_items_to_delete = []  # общий список для всех найденных файлов/папок

    for temp_dir in temp_dirs:
        print(f"\nПоиск старых файлов и папок в: {temp_dir}")
        items = find_old_items(temp_dir, older_than_days=7)  # поиск старых файлов/папок
        if items:
            print(f"Найдено {len(items)} объектов для удаления:")
            for i in items:
                print(f" - {i}")
            all_items_to_delete.extend(items)
        else:
            print("Нет файлов или папок для удаления в данной директории.")

    if all_items_to_delete:
        if ask_confirmation():
            clean_items(all_items_to_delete, dry_run=False)  # удаление
        else:
            print("Удаление отменено пользователем.")
    else:
        print("Нет файлов для удаления.")
