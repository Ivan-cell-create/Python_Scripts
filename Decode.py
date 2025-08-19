import os 
import chardet

def convert_encoding():
    file_path = input("Введите путь к текстовому файлу: ").strip(' "\'')
    
    if not os.path.isfile(file_path):
        print("Файл не найден. Проверьте путь и попробуйте снова.")
        return
    
    source_enc = input("Введите текущую кодировку файла (оставьте пустым для автоопределения): ").strip()
    
    if not source_enc:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            source_enc = detected['encoding']
            confidence = detected['confidence']
            print(f"Определена кодировка: {source_enc} с уверенностью {confidence*100:.2f}%")

    target_enc = input("Введите желаемую кодировку для сохранения (например, utf-8): ").strip()
    
    try:
        with open(file_path, 'r', encoding=source_enc) as f:
            content = f.read()
    except (UnicodeDecodeError, LookupError) as e:
        print(f"Ошибка чтения файла с кодировкой '{source_enc}': {e}")
        return

    new_file_path = file_path + f".converted_to_{target_enc}.txt"

    try:
        with open(new_file_path, 'w', encoding=target_enc) as f:
            f.write(content)
    except LookupError as e:
        print(f"Ошибка при сохранении файла с кодировкой '{target_enc}': {e}")
        return

    print(f"Файл успешно конвертирован и сохранён как: {new_file_path}")

if __name__ == "__main__":
    convert_encoding()