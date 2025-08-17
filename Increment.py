from pathlib import Path

def main():
    print("Введи путь до папки с файлами: ")
    folder_path = input().strip().strip('"').strip("'")
    print("Введи дефолтное имя: ")
    base_name = input().strip()

    path = Path(folder_path)
    
    if not path.exists() or not path.is_dir():
        print("Папка не найдена или путь не корректен")
        return
    
    files = sorted([f for f in path.iterdir() if f.is_file()])
    
    if not files:
        print("В папке нет файлов.")
        return
    
    temp_names = []
    for i, file in enumerate(files, start=1):
        temp_name = path / f"temp_rename_{i}{file.suffix}"
        file.rename(temp_name)
        temp_names.append(temp_name)

    for i, temp_file in enumerate(temp_names, start=1):
        new_name = path / f"{base_name}_{i}{temp_file.suffix}"
        temp_file.rename(new_name)

    print("Все файлы успешно переименованы")
    
if __name__ == "__main__":
    main()