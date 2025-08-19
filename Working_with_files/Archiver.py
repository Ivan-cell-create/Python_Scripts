import os
import shutil

def get_user_paths():
    print('Введите пути к файлам/папкам (по одному на строку).')
    print('Когда закончите — введите "ок".')
    
    paths = []
    while True:
        path = input("Путь: ").strip(' "\'')
        if path.lower() == 'ок':
            break
        if not os.path.exists(path):
            print(f"Путь не найден: {path}")
        else:
            paths.append(path)
    return paths

def choose_archive_format():
    formats = ['zip', 'tar', 'gztar', 'bztar', 'xztar']
    print("\nВыберите формат архива:")
    for i, fmt in enumerate(formats, start=1):
        print(f"{i}. {fmt}")
    
    while True:
        choice = input("Введите номер формата: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(formats):
            return formats[int(choice) - 1]
        else:
            print("Неверный выбор. Попробуйте ещё раз.")

def create_archive(paths, archive_format, archive_name="archive"):
    temp_folder = "temp_archive_folder"
    os.makedirs(temp_folder, exist_ok=True)

    for path in paths:
        dest_path = os.path.join(temp_folder, os.path.basename(path))
        try:
            if os.path.isdir(path):
                shutil.copytree(path, dest_path)
            else:
                shutil.copy2(path, temp_folder)
        except Exception as e:
            print(f"Ошибка при копировании {path}: {e}")

    shutil.make_archive(archive_name, archive_format, temp_folder)
    print(f"\nАрхив создан: {archive_name}.{get_extension(archive_format)}")

    shutil.rmtree(temp_folder)

def get_extension(fmt):
    """Возвращает подходящее расширение для типа архива."""
    return {
        "zip": "zip",
        "tar": "tar",
        "gztar": "tar.gz",
        "bztar": "tar.bz2",
        "xztar": "tar.xz"
    }.get(fmt, fmt)

def main():
    print("Архиватор файлов и папок\n")
    
    paths = get_user_paths()
    if not paths:
        print("Нет валидных путей. Завершение.")
        return

    archive_format = choose_archive_format()

    archive_name = input("\nВведите имя архива (без расширения): ").strip()
    if not archive_name:
        archive_name = "archive"

    create_archive(paths, archive_format, archive_name)

if __name__ == "__main__":
    main()
